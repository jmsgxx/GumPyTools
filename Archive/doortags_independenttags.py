# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script will collect elements.
__________________________________
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from Snippets._context_manager import rvt_transaction, try_except
import os
import os.path as op
from datetime import datetime
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument   # type: UIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

all_door_tags = FilteredElementCollector(doc, active_view.Id)\
    .OfCategory(BuiltInCategory.OST_DoorTags)\
    .WhereElementIsNotElementType()\
    .ToElements()

for i in all_door_tags:  # type: IndependentTag
    tagged = i.GetTaggedLocalElements()
    for el in tagged:
        el_type = el.GetTypeId()
        door_el = doc.GetElement(el_type)

        element_name = door_el.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()
        with rvt_transaction(doc, __title__):
            if 'FR' in element_name:
                doc.Delete(i.Id)


