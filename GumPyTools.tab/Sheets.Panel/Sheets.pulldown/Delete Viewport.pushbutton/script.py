# -*- coding: utf-8 -*-

__title__ = 'Delete Viewport'
__doc__ = """
Will delete all the viewports on sheet/s.

HOW TO:
- Select sheets and run the command
__________________________________
Author: Joven Mark Gumana
v1. 23 May 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import math
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from Autodesk.Revit.UI.Selection import Selection
import clr

clr.AddReference("System")
from System.Collections.Generic import List

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
selected_sheets = get_multiple_elements()

with rvt_transaction(doc, __title__):
    for sheet in selected_sheets:
        viewport_id = sheet.GetAllViewports()
        for vp in viewport_id:
            doc.Delete(vp)

