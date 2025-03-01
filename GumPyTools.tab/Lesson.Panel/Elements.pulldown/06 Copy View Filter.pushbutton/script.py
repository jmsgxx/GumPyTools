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
                                title= " Select source view",
                                multiselect=False,
                                button_name='Select source view')

if not selected_source_view:
    forms.alert('No views selected. Please select view!', exitscript=True)

source_view = dict_views_filters[selected_source_view]

# 🔴 select filters to copy
filter_ids = source_view.GetFilters()
filters = [doc.GetElement(f_id) for f_id in filter_ids]

dict_filters = {f.Name: f for f in filters}

selected_filters = forms.SelectFromList.show(sorted(dict_filters),
                                title = 'Select filters to copy',
                                multiselect=True,
                                button_name='Select filters to copy')

if not selected_filters:
    forms.alert('No filters selected. Please select filter!', exitscript=True)

filters_to_copy = [dict_filters[f_name] for f_name in selected_filters]
filter_names = dict_filters.keys()


# 🟥 SELECT DESTINATION VIEW

dict_all_views = {v.Name: v for v in all_views}

selected_destination_view = forms.SelectFromList.show(sorted(dict_all_views),
                                title= " Select destination view",
                                multiselect=True,
                                button_name='Select destination view')

if not selected_destination_view:
    forms.alert('No view/s selected. Please try again!', exitscript=True)

destination_views = [dict_all_views[v_name] for v_name in selected_destination_view]


with Transaction(doc, __title__) as t:
    t.Start()

    # 🟩 SET THE FILTER
    for view_filter in filters_to_copy:
        filter_overrides = source_view.GetFilterOverrides(view_filter.Id)

        for view in destination_views:
            view.SetFilterOverrides(view_filter.Id, filter_overrides)


    numbered_items = "\n".join("%d. %s" % (index, filter_name) for index, filter_name in enumerate(filter_names, start=1))
    forms.alert('Success! The following filters were applied on the view/s:\n{}'
                .format(numbered_items), exitscript=True)

    t.Commit()
