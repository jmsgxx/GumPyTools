# -*- coding: utf-8 -*-

__title__ = 'Copy Elements'
__doc__ = """
This script will show the how to 
uses the different copy method.
__________________________________
20230925
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit.forms import select_views

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


with Transaction(doc, __title__) as t:
    t.Start()

    # ----------------------------------------------XXXXXXXX------------------------------------------------
    # ╔═╗╔═╗╔═╗╦ ╦  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
    # ║  ║ ║╠═╝╚╦╝  ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
    # ╚═╝╚═╝╩   ╩   ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝
    # ----------------------------------------------XXXXXXXX------------------------------------------------
    # 🔴 COPY WITH A VECTOR
    # ======================================================================================================
    # # GET WALLS
    # walls_to_copy = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls)\
    #                 .WhereElementIsNotElementType().ToElementIds()
    # # VECTOR
    # vector = XYZ(25, 50, 0)
    #
    # ElementTransformUtils.CopyElements(doc, walls_to_copy, vector)
    # ========================================================================================================
    # 🔴 COPY BETWEEN VIEWS

    textToCopy = FilteredElementCollector(doc, doc.ActiveView.Id)\
        .OfCategory(BuiltInCategory.OST_TextNotes)\
        .WhereElementIsNotElementType()\
        .ToElementIds()

    # views
    source_view = doc.ActiveView
    destinationView = select_views(__title__, multiple=False)

    # transform and options
    transform = Transform.Identity
    options = CopyPasteOptions

    # execute
    ElementTransformUtils.CopyElements(source_view, textToCopy, destinationView, transform, options)

    t.Commit()