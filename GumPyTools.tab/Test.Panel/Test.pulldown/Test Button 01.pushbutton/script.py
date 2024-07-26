# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from pyrevit import forms, script
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
all_room_tags = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()

selected_tags = []

for tag in all_room_tags:
    tag_type_id = tag.GetTypeId()
    tag_fam_el = doc.GetElement(tag_type_id)

    tag_fam_name = tag_fam_el.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()

    if tag_fam_name == 'AN_TAG_RM_LEFT_1':
        tag_type_name = tag_fam_el.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        if tag_type_name == 'SQM + DGFA':
            selected_tags.append(tag.Id)
            print(tag.TagText)
            print('-----')

selection.SetElementIds(List[ElementId](selected_tags))



