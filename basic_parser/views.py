# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from basic_parser import db
from django.utils.encoding import smart_str
from grab import Grab
from grab.spider import Spider, Task
from django.shortcuts import render_to_response
from django.contrib import auth
from basic_parser import grab_spider
from basic_parser.models import Profile, Skills
import time
import os
from django.conf import settings

def basic(request):
    return render_to_response('main.html', {'user':auth.get_user(request)})

def parser(request):
    return render_to_response('parse.html', {'user':auth.get_user(request)})



def statistics(request):
    args = {}
    args['total'] = Profile.objects.count()
    args['user'] = auth.get_user(request)
    return  render_to_response('statistics.html', args)

def upload(request):
    args = {}
    args['user'] = auth.get_user(request)

    file = request.FILES.get('files')
    full_path = os.path.join(settings.BASE_DIR,'media/') + str(file)
    with open(full_path, 'wb+') as destinaton:
        for chunck in file.chunks():
            destinaton.write(chunck)

    sheet_index = request.POST.get('sheet number')
    column_index = request.POST.get('column number')
    p_start = request.POST.get('p-start')
    p_end = request.POST.get('p-end')


    class SimpleSpider(Spider):
        grab = Grab()
        login = request.POST.get('login')
        password = request.POST.get('password')
        grab.go("https://www.linkedin.com/uas/login")
        names, connections, titles, emails = [], [], [], []
        phones, summaries, skills, urls = [], [], [], []
        im, address, advice_to_connect = [], [], []
        page_titles = []
        total = {0: names,
                 1: titles,
                 2: connections,
                 3: emails,
                 4: phones,
                 5: summaries,
                 6: skills,
                 7: im,
                 8: address,
                 9: advice_to_connect
                 }
        logged = True

        grab.doc.set_input('session_key', login)
        grab.doc.set_input('session_password', password)
        grab.doc.submit()
        if grab.doc.select('//*[@class="alert error"]'):
            logged = False
            links = []
        else:
            links = grab_spider.links_list(full_path,sheet_index, column_index, p_start, p_end)
            x_path_elements = ['//*[@class="full-name"]',
                               '//*[@id="headline"]/p',
                               "//*[@class='fp-degree-icon']",
                               '//*[@id="email-view"]/ul/li/a', '//*[@id="phone-view"]',
                               '//*[@id="summary-item-view"]/div/p',
                               '//*[@class="endorse-item-name-text"]',
                               '//*[@id="im"]',
                               '//*[@id="location"]/dl/dd[1]/span/a',
                               '//*[@id="contact-comments-view"]']

        def insert_new(self, grab, elem, table):
            if grab.doc.select(elem):
                    if self.x_path_elements.index(elem) !=6:
                        self.total[table].append(grab.doc.select(self.x_path_elements[self.x_path_elements.index(elem)]).text())
                    else:
                        self.total[table].append( " | ".join([elem_in.text() for elem_in in grab.doc.select(elem)]))
            else:
                self.total[table].append("")

        def task_generator(self):
            for url in self.links:
                    self.grab.setup(url=url)
                    try:
                        profile = Profile.objects.get(url=url)
                        yield Task('existing', grab=self.grab)
                    except:
                        yield Task('new', grab=self.grab)

        def task_existing(self, grab, task):

            if grab.doc.select(self.x_path_elements[2]).text() == '1st':
                self.urls.append(grab.config['url'])
                for elem in self.x_path_elements:
                    self.insert_new(grab, elem, self.x_path_elements.index(elem))
            else:
                profile = Profile.objects.get(url=grab.config['url'])
                self.urls.append(profile.url)
                self.total[0].append(str(profile.name))
                self.total[1].append(str(profile.title))
                self.total[2].append(grab.doc.select(self.x_path_elements[2]).text())

                if profile.email !=None: self.total[3].append(str(profile.email))
                else: self.total[3].append("")

                if profile.phone !=None: self.total[4].append(str(profile.phone))
                else: self.total[4].append("")

                if profile.summary !=None: self.total[5].append(str(profile.summary))
                else: self.total[5].append("")

                if profile.im !=None: self.total[6].append(str(profile.im))
                else: self.total[6].append("")

                self.total[7].append(" | ".join([skill.skill_name for skill in Skills.objects.filter(profile=profile)]))

                if profile.address !=None: self.total[8].append(profile.address)
                else: self.total[8].append("")

                if profile.advice_to_connect !=None: self.total[9].append(profile.advice_to_connect)
                else: self.total[9].append("")

        def task_new(self, grab, task):
                self.urls.append(grab.config['url'])

                for elem in self.x_path_elements:
                    self.insert_new(grab, elem, self.x_path_elements.index(elem))

    sm = SimpleSpider(thread_number=10)
    sm.run()
    db.db_import(sm)
    full_file_name = grab_spider.xls_export(sm, sm.login)
    file = open(full_file_name, 'rb')
    from_email = settings.EMAIL_HOST
    email = request.POST.get('login')
    letter = EmailMessage('Search Results', "Profiles" , from_email, [email])
    letter.attach_file(full_file_name, mimetype='application/vnd.ms-excel')
    letter.send()


    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=all_profiles.xls'
    if sm.logged:
        return response
    else:
        args['error'] = "Wrong Password"
        return render_to_response('error.html', args)


