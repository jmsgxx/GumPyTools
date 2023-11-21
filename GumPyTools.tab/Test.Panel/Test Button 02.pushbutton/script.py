# -*- coding: utf-8 -*-

__title__ = 'Test 02'
__doc__ = """

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import *
from pyrevit import forms, revit
from System.Collections.Generic import List
from collections import Counter
from datetime import datetime

import clr
clr.AddReference("System")


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ===================================================================================================

doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

selection = uidoc.Selection
el = doc.GetElement(selection.PickObject(ObjectType.Element, 'Get element').ElementId)
# info = WorksharingUtils.GetWorksharingTooltipInfo(doc, el.Id)
# TaskDialog.Show('Who did this?', 'Created by: ' + str(info.Creator) + '\nLast changed by: ' + str(info.LastChangedBy))


# family_manager = doc.FamilyManager
# all_param = family_manager.GetParameters()
# for param in all_param:
#     print(param.Definition.Name)
#     param_element = doc.GetElement(param.Id)
#     print(param_element.CreatedBy)

collector = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()

all_shared_params = []

for param in collector:
    all_shared_params.append(param.Name)

for shared_params in sorted(all_shared_params):
    print(shared_params)

family_manager = doc.FamilyManager
shared_parameter_elements = family_manager.GetParameters()

for element in shared_parameter_elements:
    if element.IsShared:
        print(element.Definition.Name)
        print(element.Id)




# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
# with Transaction(doc, __title__) as t:
#     t.Start()
#
#     t.Commit()


