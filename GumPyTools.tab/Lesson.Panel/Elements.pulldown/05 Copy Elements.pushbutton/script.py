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


# with Transaction(doc, __title__) as t:
#     t.Start()

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
    # COPY BETWEEN VIEWS
    #👉 Get TextNotes
    # textToCopy = FilteredElementCollector(doc, doc.ActiveView.Id)\
    #     .OfCategory(BuiltInCategory.OST_TextNotes)\
    #     .WhereElementIsNotElementType()\
    #     .ToElementIds()
    #
    # #👁️ ️Get Views
    # src_view = doc.ActiveView
    # dest_view = select_views(__title__,multiple=False)
    #
    # #⚙ Transform & Options
    # transform = Transform.Identity
    # opts      = CopyPasteOptions()
    #
    #
    # #✅ Copy Elements
    # ElementTransformUtils.CopyElements(src_view, textToCopy, dest_view, transform, opts)

    # =======================================================================================================
    # COPY BETWEEN PROJECTS

walls_to_copy = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls)\
                    .WhereElementIsNotElementType().ToElementIds()

all_docs = list(app.Documents)
doc_a = all_docs[0]
doc_b = all_docs[1]

with Transaction(doc_b, __title__) as t:
    t.Start()

    # ⚙ Transform & Options
    transform = Transform.Identity
    opts = CopyPasteOptions()


    ElementTransformUtils.CopyElements(doc_a, walls_to_copy, doc_b, transform, opts)

    t.Commit()