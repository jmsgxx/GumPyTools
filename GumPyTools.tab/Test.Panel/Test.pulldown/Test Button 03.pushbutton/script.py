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
from Snippets._x_selection import get_multiple_elements
import xlrd
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
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

all_scope_bx = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_VolumeOfInterest).ToElements()
all_views = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()

with rvt_transaction(doc, __title__):
    for view in all_views:
        view_p_name = Element.Name.GetValue(view)
        if 'DOC_FP_FFL_08M_50' in view_p_name:
            for scope_bx in all_scope_bx:
                scope_bx_name = scope_bx.Name
                if scope_bx_name.startswith("L7L8_DL"):
                    if view_p_name[-3:] == scope_bx_name[-3:]:
                        view_s_box = view.get_Parameter(BuiltInParameter.VIEWER_VOLUME_OF_INTEREST_CROP)
                        view_s_box.Set(scope_bx.Id)


"""
TO SET SCOPE BOX, DO NOT DELETE FOR NOW!
"""

