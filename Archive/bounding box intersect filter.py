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
from Snippets._convert import convert_internal_units
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._x_selection import ISelectionFilter_Classes, get_multiple_elements
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
import pyrevit
from pyrevit import forms
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================

selected_rooms = get_multiple_elements()
if not selected_rooms:
    try:
        filter_type = ISelectionFilter_Classes([Room])
        room_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Rooms")
        selected_rooms = [doc.GetElement(el) for el in room_list]
        if not selected_rooms:
            forms.alert("No selected rooms. Exiting command", exitscript=True)
    except Exception as e:
        forms.alert("{} Exiting Command.".format(str(e)), exitscript=True)

# =====================================================================================================

for room in selected_rooms:
    room_geometry = room.ClosedShell

    bounding_box = room_geometry.GetBoundingBox()
    bb_min = bounding_box.Min
    bb_max = bounding_box.Max

    room_outline = Outline(bb_min, bb_max)

    bb_filter = BoundingBoxIntersectsFilter(room_outline)

    collector = FilteredElementCollector(doc, active_view.Id).WherePasses(bb_filter).ToElements()

    door_list = [element for element in collector if element.Category.Name == 'Doors']

    for door in door_list:
        door_id = door.GetTypeId()
        door_el = doc.GetElement(door_id)
        door_width = door_el.get_Parameter(BuiltInParameter.FAMILY_WIDTH_PARAM).AsDouble()
        door_height = door_el.get_Parameter(BuiltInParameter.GENERIC_HEIGHT).AsDouble()

        width_mm = convert_internal_units(door_width, False, 'mm')
        height_mm = convert_internal_units(door_height, False, 'mm')

        print(width_mm)
        print(height_mm)

        door_area = door_width * door_height
        # print(door_area)



