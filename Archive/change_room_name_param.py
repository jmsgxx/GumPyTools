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

level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_Rooms)\
            .WherePasses(ElementLevelFilter(level_filter))\
            .ToElements()

for room in rooms:
    room_class = room.LookupParameter('Rooms_Classification_BLP').AsString()
    room_dept_param = room.LookupParameter('Department_BLP')
    room_name_param = room.LookupParameter('Room_Name_BLP')
    room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    with Transaction(doc, __title__) as t:
        t.Start()

        if room_name_param.AsString() == 'STRESS TREADMILL':
            room_name_param.Set(str('STRESS TREADMILL ROOM'))

        t.Commit()


