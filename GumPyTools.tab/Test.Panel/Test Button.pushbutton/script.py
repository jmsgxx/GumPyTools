# -*- coding: utf-8 -*-

__title__ = 'Test Button'
__doc__ = """
testing button for anything.
__________________________________
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
import math

import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================




# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
# with Transaction(doc, __title__) as t:
#     t.Start()
#
#     t.Commit()

# Get the SiteLocation instance.
site = doc.SiteLocation

# Angles are in radians when coming from Revit API, so we
# convert to degrees for display
angleRatio = math.pi / 180   # angle conversion factor

# Format the prompt information.
prompt = "Current project's Site location information:"
prompt += "\n\t" + "Latitude: " + str(site.Latitude / angleRatio) + " degrees"
prompt += "\n\t" + "Longitude: " + str(site.Longitude / angleRatio) + " degrees"

print(prompt)

