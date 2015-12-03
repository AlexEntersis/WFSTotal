# coding=utf-8

# from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from grab import Grab
from grab.spider import Spider
from basic_parser import db, grab_spider
from basic_parser.models import Profile

def basic(request):
    return render_to_response('main.html', {'user': auth.get_user(request)})

def parser(request):
    return render_to_response('parse.html', {'user': auth.get_user(request)})

def statistics(request):
    args = {}
    args['total'] = Profile.objects.count()
    args['user'] = auth.get_user(request)
    return  render_to_response('statistics.html', args)

def make_new_link(url):
    new_grab = Grab()
    new_link = ''
    if 'linkedin.com/in/' in url:
        return  url
    if 'linkedin.com/profile/'in url:
        return  url
    else:
        try:
            new_grab.go(url)
            head = str(new_grab.response.head).split('\\r\\')
            for x in head:
                if 'https' in x:
                    new_link = x.replace('https://ua.', 'https://www.').replace(" ", "")\
                        .replace('nLocation:', '').strip(" ")\
                        .replace('https://pl.', 'https://www.')
        except:
            new_link = url
        return new_link


def upload(request):
    args = dict()
    args['user'] = auth.get_user(request)

    class SimpleSpider(Spider):
        grab = grab_spider.spider_login(request)
        logged = True

        names, connections, titles, emails = [], [], [], []
        phones, summaries, skills, urls = [], [], [], []
        im, address, advice_to_connect = [], [], []
        total = {0: names,
                 1: titles,
                 2: connections,
                 3: emails,
                 4: phones,
                 5: summaries,
                 6: skills,
                 7: im,
                 8: address,
                 9: advice_to_connect,
                 10: urls
                     }

        if grab.doc.select('//*[@class="alert error"]'):
            logged = False
            links = []
        else:
            links = grab_spider.links_list(request)
        x_path_elements = grab_spider.spider_xpaths()

        for url in links:
            try:
                grab.go(make_new_link(url))
                if grab.doc.select(x_path_elements[2]).text() == '1st':
                    grab_spider.spider_go_first(grab, url, x_path_elements, names, titles, connections, emails, phones, summaries, skills, urls, im, address, advice_to_connect)
                else:
                    grab_spider.spider_go_second(grab, url, x_path_elements, names, titles, connections, emails, phones, summaries, skills, urls, im, address, advice_to_connect)
            except:
                pass
    sm = SimpleSpider(thread_number=10)
    sm.run()
    db.db_import(sm)
    full_file_name = grab_spider.xls_export(sm, request.POST.get('login'))
    file = open(full_file_name, 'rb')
    # from_email = settings.EMAIL_HOST
    # email = request.POST.get('login')
    # letter = EmailMessage('Search Results', "Profiles" , from_email, [email])
    # letter.attach_file(full_file_name, mimetype='application/vnd.ms-excel')
    # letter.send()
    
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename={0}.xls'.format(request.POST.get('login'))
    if sm.logged:
        return response
    else:
        args['error'] = "Wrong Password"
        return render_to_response('error.html', args)



