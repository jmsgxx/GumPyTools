# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
import xlsxwriter
from pyrevit import forms
from datetime import datetime
import os
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document   # type: Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =============================================================================================
# ⭕ PREPARE THE EXCEL FILE
directory = forms.save_excel_file(title='Select destination file')
workbook = xlsxwriter.Workbook(directory)
worksheet = workbook.add_worksheet()


# =============================================================================================
views_sheet_ids = FilteredElementCollector(doc).OfClass(ViewSheet).ToElementIds()
tblock_cat_id = ElementId(BuiltInCategory.OST_TitleBlocks)


# 🔴 GET ROOM DEPARTMENT AS LIST OPTION
room_dept_list = []
for view_id_temp in views_sheet_ids:     # type: ElementId
    view_sheet = doc.GetElement(view_id_temp)
    rm_dept_param = view_sheet.LookupParameter('Room Department')
    if rm_dept_param:
        room_dept = rm_dept_param.AsString()
        if room_dept:
            room_dept_list.append(room_dept)

room_dept_list = list(set(room_dept_list))

sel_room_dept = forms.SelectFromList.show(sorted(room_dept_list),
                                          multiselect=False,
                                          button_name='Select Sheet')


# ============================================================================================
# 🟢 MAKE A CONDITION
pharma_rls = []

for v_id in views_sheet_ids:
    view_sheet = doc.GetElement(v_id)
    rm_dept_param = view_sheet.LookupParameter('Room Department').AsString()
    rm_dwg_type = view_sheet.LookupParameter('Drawing Type').AsString()
    if rm_dept_param == sel_room_dept and 'ROOM LAYOUT SHEET' in rm_dwg_type:
        pharma_rls.append(v_id)


# ============================================================================================
# 🔵 SEPARATE THE NEEDED PARAMETER
output_report = []

for sht_id in pharma_rls:
    view_el = doc.GetElement(sht_id)
    t_block_id = FilteredElementCollector(doc, sht_id).OfCategoryId(tblock_cat_id).ToElementIds()
    sheet_number = view_el.SheetNumber
    sheet_name = view_el.Name
    pharma_dwg_type = view_el.LookupParameter('Drawing Type')
    for tblock in t_block_id:
        t_block_el = doc.GetElement(tblock)
        tblock_name = t_block_el.Name
        output_report.append((sheet_number, sheet_name, tblock_name))

# ============================================================================================
# ⭕ write to excel
for index, (sheet_number, sheet_name, tblock_name) in enumerate(sorted(output_report), start=1):
    worksheet.write('A{}'.format(index), sheet_number)
    worksheet.write('B{}'.format(index), sheet_name)
    worksheet.write('C{}'.format(index), tblock_name)

