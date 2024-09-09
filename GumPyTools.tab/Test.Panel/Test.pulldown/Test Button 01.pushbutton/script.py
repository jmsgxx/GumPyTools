# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from pyrevit import forms, script
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================


def get_param_value(param):
    """Get a value from a Parameter based on its StorageType."""
    value = None
    if param.StorageType == StorageType.Double:
        value = param.AsDouble()
    elif param.StorageType == StorageType.ElementId:
        value = param.AsElementId()
    elif param.StorageType == StorageType.Integer:
        value = param.AsInteger()
    elif param.StorageType == StorageType.String:
        value = param.AsString()
    return value


output = script.get_output()
output.center()

try:
    selected_element = get_multiple_elements()
    if not selected_element:
        element_list = selection.PickObjects(ObjectType.Element)
        selected_element = [doc.GetElement(el) for el in element_list]
except Exception as e:
    forms.alert(str(e))


for i in selected_element:

    params = i.Parameters    # get just one item
    for p in sorted(params, key=lambda x: x.Definition.Name):    # loop thorough the parameters to get their name
        print("Name: {}".format(p.Definition.Name))
        print("ParameterGroup: {}".format(p.Definition.ParameterGroup))
        print("BuiltInParameter: {}".format(p.Definition.BuiltInParameter))
        print("IsReadOnly: {}".format(p.IsReadOnly))
        print("HasValue: {}".format(p.HasValue))
        print("IsShared: {}".format(p.IsShared))
        print("StorageType: {}".format(p.StorageType))
        print("Value: {}".format(get_param_value(p)))
        print("AsValueString(): {}".format(p.AsValueString()))
        print('-' * 100)



