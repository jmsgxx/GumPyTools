# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
import math
import xlsxwriter
from pyrevit import forms, revit
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
    center = (bounding.Max + bounding.Min) * 0.5
    loc_pt = room_el.Location
    if bounding and loc_pt:
        center = (bounding.Max + bounding.Min) * 0.5
        room_center = XYZ(center.X, center.Y, loc_pt.Point.Z)
        return room_center
    else:
        return None


level_filter = active_level.Id

rooms = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Rooms)\
    .WherePasses(ElementLevelFilter(level_filter))\
    .ToElements()

with Transaction(doc, __title__) as t:
    t.Start()

    for room in rooms:
        room_class = room.LookupParameter('Rooms_Classification_BLP').AsString()
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
            else:
                print("Could not get center of room {}".format(room.Id))

    t.Commit()


