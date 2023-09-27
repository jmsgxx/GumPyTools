# -*- coding: utf-8 -*-

__title__ = 'Copy View Filter'
__doc__ = """
This script will copy view filter
from one view and will paste on another view.
============================================
1st version: 27 Sep 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms

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



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
# with Transaction(doc, __title__) as t:
#     t.Start()
#
#     t.Commit()

# 🟢 get all views
all_views = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Views)\
    .WhereElementIsNotElementType()\
    .ToElements()

# 🟡 view with filters
view_w_filters = [v for v in all_views if v.GetFilters()]
# only_view_w_filters = [v for v in all_views if v.GetFilters() and not v.IsTemplate]
# only_templates_w_filters = [v for v in all_views if v.GetFilters() and v.IsTemplate]

# ✅ make sure there are views with filters in the project
if not view_w_filters:
    forms.alert('Project has no views with filters and view templates!', exitscript=True)

# 🔵 create dictionary of views
dict_views_filters = {v.Name: v for v in view_w_filters}

# for k, v in dict_views_filters.items():
#     print(k, v)

# 🟣 select views from list using pyrevit forms
selected_source_view = forms.SelectFromList.show(sorted(dict_views_filters),
                                multiselect=False,
                                button_name='Select source view')

print("Selected source view: {}".format(selected_source_view))


