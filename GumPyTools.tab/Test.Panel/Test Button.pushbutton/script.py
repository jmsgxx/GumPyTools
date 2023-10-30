# -*- coding: utf-8 -*-

__title__ = 'Test Button'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
from System.Collections.Generic import List

import clr
import revitron
clr.AddReference("System")


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


# with forms.WarningBar(title='Pick an element:'):
#     selected_room = revit.pick_element()
#
# el_cat          = selected_room.Category.Name
#
# if el_cat != 'Rooms':
#     forms.alert('Just pick a Room', exitscript=True)

collector = FilteredElementCollector(doc, active_view.Id).WhereElementIsNotElementType()

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    elements = []
    for element in collector:
        element_cat = element.Category
        if element_cat is not None:
            element_name = element_cat.Name
            if element_name != "":
                elements.append(element)

    affected_elements = []
    for element in elements:
        el_type_id = element.GetTypeId()
        el_symbol = doc.GetElement(el_type_id)
        if el_symbol is not None:
            # parameter
            manufacturer_val = el_symbol.get_Parameter(BuiltInParameter.ALL_MODEL_MANUFACTURER)
            filters = active_view.GetFilters()
            for filter_id in filters:
                filter_element = doc.GetElement(filter_id)  # type 'ParameterFilterElement'

                # Get the filter from the ParameterFilterElement
                el_filter = filter_element.GetElementFilter()  # type 'LogicalAndFilter' / 'LogicalOrFilter'

                # Check if the element satisfies the filter
                if el_filter.PassesFilter(element):
                    if filter_element.Name == 'By User':
                        if manufacturer_val is not None and not manufacturer_val.IsReadOnly:
                            manufacturer_val.Set('(BY USER)')
                #     affected_elements.append(element)
                # print("Element {} is affected by filter {}".format(element.Id.IntegerValue, filter_element.Name))



    t.Commit()
# =============================================================================================




