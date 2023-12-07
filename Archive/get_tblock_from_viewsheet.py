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

views_sheet_ids = FilteredElementCollector(doc).OfClass(ViewSheet).ToElementIds()
title_block_category_id = ElementId(BuiltInCategory.OST_TitleBlocks)

pharma_rls = []

for v_id in views_sheet_ids:
    view_sheet = doc.GetElement(v_id)
    rm_dept_param = view_sheet.LookupParameter('Room Department').AsString()
    rm_dwg_type = view_sheet.LookupParameter('Drawing Type').AsString()
    if rm_dept_param == 'PHARMACY' and rm_dwg_type == 'ROOM LAYOUT SHEET':
        pharma_rls.append(v_id)

# output_report = []

for sht_id in pharma_rls:
    view_el = doc.GetElement(sht_id)
    t_block_id = FilteredElementCollector(doc, sht_id).OfCategoryId(title_block_category_id).ToElementIds()
    sheet_number = view_el.SheetNumber
    pharma_dwg_type = view_el.LookupParameter('Drawing Type')
    for tblock in t_block_id:
        t_block_el = doc.GetElement(tblock)
        tblock_name = t_block_el.Name

        with Transaction(doc, __title__) as t:
            t.Start()
            if "A1" in tblock_name:
                pharma_dwg_type.Set('ROOM LAYOUT SHEET A1')
            elif "A3" in tblock_name:
                pharma_dwg_type.Set('ROOM LAYOUT SHEET A3')
                # output_report.append((sheet_number, tblock_name))
            t.Commit()

# output_report.sort()

# for sheet_number, tblock_name in output_report:
#     print("{} - {}".format(sheet_number, tblock_name))

# # ⭕ EXPORT IN EXCEL. Print statement takes too long.
# workbook = xlsxwriter.Workbook(r"C:\Users\gary_mak\Downloads\A1_tblocks.xlsx")
# worksheet = workbook.add_worksheet
#
# worksheet.write('A1', 'Sheet Number')
# worksheet.write('B1', 'Title block Name')
#
#
# for index, (sheet_number, tblock_name) in enumerate(output_report, start=2):
#     worksheet.write('A{}'.format(index), sheet_number)
#     worksheet.write('B{}'.format(index), tblock_name)
#
# workbook.close()