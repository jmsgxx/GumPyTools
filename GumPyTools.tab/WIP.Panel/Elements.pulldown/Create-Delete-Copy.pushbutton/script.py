# -*- coding: utf-8 -*-

__title__ = 'Create/Delete/Copy Elements'
__doc__ = """
This script will create, delete and copy elements.
__________________________________
Author: Joven Mark Gumana
20230922
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *

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
# active_level    = doc.ActiveView.Level



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
# CHANGE HERE
# =========================================================================================================
# ╔╦╗╔═╗═╗ ╦╔╦╗
#  ║ ║╣ ╔╩╦╝ ║ 
#  ╩ ╚═╝╩ ╚═ ╩ #text
# =========================================================================================================
    """
    Text Note CLass
    public static TextNote Create(
        Document document,
        ElementId viewId,
        XYZ position,
        string text,
        ElementId typeId
    )
    """
    text_type_id = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
    pt = XYZ(0,0,0)
    text = 'This is your first create method in Revit API.'

    TextNote.Create(doc, active_view.Id, pt, text, text_type_id)
# ============================================================================================================
# ╦═╗╔═╗╔═╗╔╦╗
# ╠╦╝║ ║║ ║║║║
# ╩╚═╚═╝╚═╝╩ ╩#room




# ╦  ╦╔╗╔╔═╗╔═╗
# ║  ║║║║║╣ ╚═╗
# ╩═╝╩╝╚╝╚═╝╚═╝#lines




# ╦ ╦╔═╗╦  ╦  ╔═╗
# ║║║╠═╣║  ║  ╚═╗
# ╚╩╝╩ ╩╩═╝╩═╝╚═╝#walls




# ╔═╗╦ ╦╔═╗╔═╗╔╦╗╔═╗
# ╚═╗╠═╣║╣ ║╣  ║ ╚═╗
# ╚═╝╩ ╩╚═╝╚═╝ ╩ ╚═╝#sheets



# ╦  ╦╦╔═╗╦ ╦╔═╗
# ╚╗╔╝║║╣ ║║║╚═╗
#  ╚╝ ╩╚═╝╚╩╝╚═╝#views




# ╦═╗╔═╗╔═╗╦╔═╗╔╗╔
# ╠╦╝║╣ ║ ╦║║ ║║║║
# ╩╚═╚═╝╚═╝╩╚═╝╝╚╝#region



# ╔═╗╦  ╔═╗╔═╗╦═╗
# ╠╣ ║  ║ ║║ ║╠╦╝
# ╚  ╩═╝╚═╝╚═╝╩╚═#floor




# ╔═╗╔═╗╔═╗╦ ╦  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
# ║  ║ ║╠═╝╚╦╝  ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
# ╚═╝╚═╝╩   ╩   ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝#copy




# ╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
#  ║║║╣ ║  ║╣  ║ ║╣   ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
# ═╩╝╚═╝╩═╝╚═╝ ╩ ╚═╝  ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝#delete elements


    t.Commit()