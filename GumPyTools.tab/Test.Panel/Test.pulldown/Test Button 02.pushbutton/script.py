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
from Autodesk.Revit.DB.Architecture import *
from Snippets._x_selection import get_multiple_elements
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction, try_except
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import clr
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection
# ======================================================================================================

selected_sheets = get_multiple_elements()

t_block_id = ElementId(BuiltInCategory.OST_TitleBlocks)

for sheet in selected_sheets:
    tblock_id = FilteredElementCollector(doc, sheet.Id).OfCategoryId(t_block_id).ToElementIds()
    for tblock in tblock_id:    # type: FamilyInstance
        tblock_el = doc.GetElement(tblock)
        tblock_id = tblock_el.GetTypeId()
        tblock_type = doc.GetElement(tblock_id)     # type: FamilySymbol
        tblock_fam_name = tblock_type.Family        # family

        print(tblock_fam_name.Name)      # family name

        tp_name = tblock_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()        # type name
        print(tp_name)




"""
all_t_blocks = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()

# Initialize an empty dictionary
t_blocks_dict = {}

for t_block in all_t_blocks:
    # Get the family name, type name, and element id
    family_name = t_block.Family.Name
    type_name = t_block.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
    element_id = t_block.Id

    # Check if the family name is already in the dictionary
    if family_name not in t_blocks_dict:
        # If not, add a new dictionary for this family
        t_blocks_dict[family_name] = {}

    # Add the type name and element id to the family's dictionary
    t_blocks_dict[family_name][type_name] = element_id

# Now t_blocks_dict is a nested dictionary with the required format

"""

