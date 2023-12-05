# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
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
from Autodesk.Revit.UI.Selection import Selection, ISelectionFilter
from pyrevit import forms, script
import xlsxwriter
import clr
from datetime import datetime

clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel

selection = uidoc.Selection  # type: Selection


# ╔═╗╦  ╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝ CLASSES
# ======================================================================================================


class CustomFilter(ISelectionFilter):
    def AllowElement(self, element):
        if element.Category.BuilInCategory == BuiltInCategory.OST_Rooms:
            return True


custom_filter = CustomFilter()
selected_elements = selection.PickElementsByRectangle(custom_filter, "Select rooms ")
print(selected_elements)