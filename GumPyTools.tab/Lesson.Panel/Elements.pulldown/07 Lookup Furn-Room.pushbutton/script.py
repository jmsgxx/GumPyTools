# -*- coding: utf-8 -*-

__title__ = 'Copying Parameter'
__doc__ = """
Copy Parameter from one 
Category to another.
_______________________________
v1: 28Sep2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms

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

all_phases  = list(doc.Phases)
# for phase in all_phases:
#     print(phase.Name)
phase = all_phases[-1]



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================

# GET ELEMENTS
all_furniture    = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Furniture).\
                    WhereElementIsNotElementType().ToElements()
all_f_system      = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FurnitureSystems).\
                    WhereElementIsNotElementType().ToElements()
all_p_fixtures    = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PlumbingFixtures).\
                    WhereElementIsNotElementType().ToElements()

# all_doors    = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).\
#                     WhereElementIsNotElementType().ToElements()
#
# for doors in all_doors:
#     print(doors.Name)

all_elements = list(all_furniture) + list(all_f_system) + list(all_p_fixtures)

# iterate and get room

with Transaction(doc, __title__) as t:
    t.Start()
    for el in elements:
        room = dr.Room[phase]
        # print(room)
        if room:
            room_name       = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
            room_number     = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsValueString()
            print(room_name)
            print(room_number)

            # get parameter to write
            proj_room_name      = el.LookupParameter("JM_ROOM_NAME")
            proj_room_number    = el.LookupParameter("JM_ROOM_NUMBER")

            # set parameter
            # if proj_room_name:
            #     proj_room_name.Set(room_name)
            # if proj_room_number:
            #     proj_room_number.Set(room_number)

    t.Commit()





