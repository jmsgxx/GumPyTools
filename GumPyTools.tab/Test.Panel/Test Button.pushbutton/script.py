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
from pyrevit import forms
from System.Collections.Generic import List

import os
import csv
import clr
import xlrd
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


list_of_categories = List[BuiltInCategory](
            [BuiltInCategory.OST_SpecialityEquipment,
             BuiltInCategory.OST_Furniture,
             BuiltInCategory.OST_MedicalEquipment]
)

multi_cat_filter = ElementMulticategoryFilter(list_of_categories)

element_list = FilteredElementCollector(doc).WhereElementIsElementType().WherePasses(multi_cat_filter).ToElementIds()

collect_views = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

for view in collect_views:
    placed_views = view.GetAllPlacedViews()
    print(placed_views)  # Add this line to check if placed_views is populated correctly
    plan_views = []
    for placed_view in placed_views:
        view_element = doc.GetElement(placed_view)
        view_object = view_element.View
        if view_object.ViewType == ViewType.ViewPlan:
            plan_views.append(placed_view)
    print(plan_views)





# with Transaction(doc, __title__) as t:
#     t.Start()
#
#
#     t.Commit()


