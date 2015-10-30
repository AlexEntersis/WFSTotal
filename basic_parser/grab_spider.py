
import xlrd
from openpyxl import Workbook
from openpyxl.compat import range
import time
import os
from django.conf import settings


def links_list(filename, sheet_index, column_index, p_start, p_end):
    """method creates links to be followed and parsed from uploaded files"""

    wb = xlrd.open_workbook(filename=filename, encoding_override='utf-8')
    worksheet = wb.sheet_by_index(int(sheet_index)-1)
    table = []
    for cell in worksheet.col(int(column_index)-1):
        if cell.value not in table:
            table.append(str(cell.value))
    return table[int(p_start)-1:int(p_end)]


def xls_export(sm, name):
    """method to export to xls file profiles from current Spider"""

    dest_filename = os.path.join(settings.MEDIA_ROOT, '{0}: {1}.xls'.format(str(name), time.strftime("%H:%M:%S")))
    wb = Workbook()
    ws3 = wb.get_sheet_by_name('Sheet')
    for x in range(len(sm.names)):
        ws3.cell(column=1, row=x+1, value=sm.names[x])
        ws3.cell(column=2, row=x+1, value=sm.titles[x])
        ws3.cell(column=3, row=x+1, value=sm.connections[x])
        ws3.cell(column=4, row=x+1, value=str(sm.emails[x] + '\n' + sm.phones[x] + '\n' + sm.advice_to_connect[x]).strip())
        ws3.cell(column=5, row=x+1, value=sm.im[x])
        ws3.cell(column=6, row=x+1, value=sm.summaries[x])
        ws3.cell(column=7, row=x+1, value=sm.skills[x])
        ws3.cell(column=8, row=x+1, value=sm.urls[x])
    wb.save(filename=dest_filename)
    return dest_filename


