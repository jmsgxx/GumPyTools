# -*- coding: utf-8 -*-

__title__ = 'Filtered Element Collector'
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
active_level    = doc.ActiveView.Level



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
# CHANGE HERE


# ╔╦╗╔═╗═╗ ╦╔╦╗
#  ║ ║╣ ╔╩╦╝ ║ 
#  ╩ ╚═╝╩ ╚═ ╩ #text


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