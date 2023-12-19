# -*- coding: utf-8 -*-

__title__ = 'Find RIL Rm'
__doc__ = """
WARNING: MAKE SURE "LINE" CATEGORY IS TURNED ON.

This is script will mark the rooms that you
need with 'Circle' in a specified Department.

HOW TO:
1. Click the command.
2. Select the department that you need.
3. To 'Delete' all, right click on the circle,
select 'Select All Instance in View' and press delete.
__________________________________
v1.18 Dec 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
import math
from pyrevit import forms, revit
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

def get_room_center(room_el):
    """
    gets the center of the room
    """
    bounding = room_el.get_BoundingBox(active_view)
    loc_pt = room_el.Location
    if bounding and loc_pt:
        center = (bounding.Max + bounding.Min) * 0.5
        room_center = XYZ(center.X, center.Y, loc_pt.Point.Z)
        return room_center



level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Rooms)\
    .WherePasses(ElementLevelFilter(level_filter))\
    .ToElements()

with Transaction(doc, __title__) as t:
    t.Start()

    room_dep_lst = []

    for item in rooms:
        room_dept_param = item.LookupParameter('Department_BLP')
        if room_dept_param:
            room_dept = room_dept_param.AsString()
            if room_dept:
                room_dep_lst.append(room_dept)

    room_dep_lst = list(set(room_dep_lst))
    selected_rm_dep = forms.SelectFromList.show(sorted(room_dep_lst), button_name='Select Department',
                                                multiselect=False,
                                                title="Departments in model")

    for room in rooms:
        room_class = room.LookupParameter('Rooms_Classification_BLP').AsString()
        room_dept_param = room.LookupParameter('Department_BLP')
        if room_dept_param:
            room_dept = room_dept_param.AsString()
        if room_dept == selected_rm_dep:
            if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                normal = XYZ.BasisZ  # Normal vector along Z-axis
                origin_point = get_room_center(room)
                if origin_point:
                    plane = Plane.CreateByNormalAndOrigin(normal, origin_point)
                    radius = 10
                    start_angle = 0.0
                    end_angle = 2.0 * math.pi
                    arc = Arc.Create(plane, radius, start_angle, end_angle)
                    doc.Create.NewDetailCurve(active_view, arc)

    t.Commit()


