# -*- coding: utf-8 -*-

__title__ = 'Test Button 03'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets._convert import convert_internal_to_sqm, convert_m_to_feet
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter, StairsFilter
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import sys
import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection


# ======================================================================================================
# 1️⃣ collect the rooms
all_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

# 2️⃣ collect the rooms parameter and the object
rooms_lst = []
rooms_obj = []

for room in all_rooms:
    if room.Location:
        room_dept = room.get_Parameter(BuiltInParameter.ROOM_OCCUPANCY).AsString()
        room_area = room.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble()
        if room_dept:
            rooms_lst.append((room_dept, room_area))
            rooms_obj.append(room)

# 3️⃣ get the total area per department by dictionary
dept_total_area = {}
for department, area in rooms_lst:
    if department in dept_total_area:
        dept_total_area[department] += area
    else:
        dept_total_area[department] = area

# 4️⃣ combine the 2 lists that was extracted from 2️⃣
combined_list = list(zip(rooms_lst, rooms_obj))
combined_list.sort(key=lambda x: x[0][0])

# 5️⃣ set the parameter
with rvt_transaction(doc, __title__):
    for data in combined_list:
        """
        the loop knows which object to set because it was sorted already beforehand, the area value to set 
        came from the dictionary
        """
        # (0=(0=data, 1=area), 1=room object)
        rm_obj = data[1]
        total_area = dept_total_area[data[0][0]]
        area_conv = convert_internal_to_sqm(total_area)
        rm_param = rm_obj.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
        rm_param.Set(str("{:,.2f} sqm".format(area_conv)))
