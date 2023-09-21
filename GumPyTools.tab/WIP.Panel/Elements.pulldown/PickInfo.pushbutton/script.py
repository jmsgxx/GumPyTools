# -*- coding: utf-8 -*-

__title__ = "Element Information"
__doc__ = """This is a simple tool for element selection"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ___________________________________________________
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
import sys


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
# __________________________________________________
doc     =__revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
# _________________________________________________
# selected_views = forms.select_views()
# if selected_views:
#     print(selected_views)

# pick an element
with forms.WarningBar(title='Pick an element:'):
    element = revit.pick_element()

element_type = type(element)

if element_type != Wall:
    forms.alert('Just pick a wall', exitscript=True)

# print(element)
# print(element_type)

# get information
el_cat          = element.Category.Name
el_id           = element.Id
el_level        = doc.GetElement(element.LevelId)
el_wall_type    = element.WallType
el_width        = element.Width

print("Element Category: {}".format(el_cat))
print("Element ID: {}".format(el_id))
print("Element Level ID: {}".format(el_level.Name))
print("Element Wall Type: {}".format(el_wall_type))
print("Element Width: {}".format(el_width))