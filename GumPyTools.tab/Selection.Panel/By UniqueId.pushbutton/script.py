# -*- coding: utf-8 -*-

__title__ = 'By UniqueId'
__doc__ = """
This script will auto select the Element once UniqueId
is pasted as input.
 - Click the Element Name/Element Id whichever as available
   to select the element
 - Click the search button to zoom in.
   DISCLAIMER: zoom in might not always work.
    
*** PLEASE RAISE ANY ERROR YOU'LL ENCOUNTER**
    
WHEN IN DOUBT CONTACT THE AUTHOR: 👇👀
__________________________________
Author: Joven Mark Gumana

v1. 21 Aug 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
from Autodesk.Revit.DB import *
from pyrevit import forms, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet

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
output = script.get_output()
output.center()
output.resize(200, 200)

un_id = None
try:
    components = [Label('Enter UniqueId:'),
                  TextBox('unique_id', ''),
                  Separator(),
                  Button('Find')]

    form = FlexForm('Find the Element', components)
    form.show()

    user_input = form.values
    un_id = user_input['unique_id']

except Exception as e:
    forms.alert("No UniqueId input. Try again.", warn_icon=True, exitscript=True)

element = doc.GetElement(un_id)
print(output.linkify(element.Id, (element.Name if element else element.Id)))







