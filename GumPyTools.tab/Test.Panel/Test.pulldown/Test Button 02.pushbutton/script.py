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

# ---------------------------------------------------------------------------------------------
user_parameter = 'Sheet Department'
all_shared_param = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()

param_element = None

for shared_param in all_shared_param:
    if shared_param.Name == user_parameter:
        param_element = shared_param
        break

f_param         = ParameterValueProvider(param_element.Id)
evaluator       = FilterStringEquals()
f_param_value   = "RADIOLOGY"

f_rule = FilterStringRule(f_param, evaluator, f_param_value)
filter_name = ElementParameterFilter(f_rule)

sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets)\
            .WherePasses(filter_name)\
            .ToElements()

# 🟠 COLLECT ALL ROOMS
level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_Rooms)\
            .WherePasses(ElementLevelFilter(level_filter))\
            .ToElements()

# ---------------------------------------------------------------------------------------------
rooms_lst   = []

for room in rooms:
    room_class          = room.LookupParameter('Rooms_Classification_BLP').AsString()
    room_dept_param     = room.LookupParameter('Department_BLP')
    if room_dept_param:
        room_dept = room_dept_param.AsString()
        if room_dept == 'RADIOLOGY':
            if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                # room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                room_id         = room.Id.IntegerValue
                room_name       = room.LookupParameter('Room_Name_BLP').AsString()
                room_number     = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                rooms_lst.append(room_id)

# ---------------------------------------------------------------------------------------------
sheet_rm_id_lst = []

for sheet in sheets:
    sheet_sht_dept  = sheet.LookupParameter('Sheet Department').AsString()
    sheet_rm_dept   = sheet.LookupParameter('Room Department').AsString()
    sheet_dwg_type  = sheet.LookupParameter('Drawing Type').AsString()
    if sheet_sht_dept == 'RADIOLOGY':
        if sheet_rm_dept == 'ROOM LAYOUT SHEET':
            if sheet_dwg_type == 'ROOM LAYOUT SHEET':
                viewport_id = sheet.GetAllViewports()
                for _id in viewport_id:
                    viewport    = doc.GetElement(_id)
                    view_id     = viewport.ViewId
                    view        = doc.GetElement(view_id)

                    if view.ViewType == ViewType.FloorPlan:

                        room_collector = FilteredElementCollector(doc, view.Id)\
                                        .OfCategory(BuiltInCategory.OST_Rooms)\
                                        .ToElements()

                        for rm in room_collector:
                            sheet_room_id = rm.Id
                            sheet_rm_id_lst.append(sheet_room_id)

print("ROOMS IN MODEL: {}".format(len(rooms_lst)))
print("ROOMS IN SHEET: {}".format(len(sheet_rm_id_lst)))


missing_ids = [ids for ids in rooms_lst if ids not in sheet_rm_id_lst]
for index, ids in enumerate(missing_ids, start=1):
    print('{}. {}'.format(index, ids))




