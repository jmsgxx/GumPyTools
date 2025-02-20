# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script, forms
from Snippets._x_selection import ISelectionFilter_Classes
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from FunctionFiles._selection import (FECollectorCat, get_multiple_elements, selection_filter, SelectElementBIGClass,
                                      highlight_selected_elements)
from Snippets._convert import convert_internal_units, convert_internal_to_m

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
rvt_year = int(app.VersionNumber)

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================
# ╔═╗╔═╗╔╦╗  ╔═╗╦  ╦    ╦═╗╔═╗╔═╗╦╔═╗╔╗╔  ╔╗╔╔═╗╔╦╗╔═╗╔═╗
# ║ ╦║╣  ║   ╠═╣║  ║    ╠╦╝║╣ ║ ╦║║ ║║║║  ║║║╠═╣║║║║╣ ╚═╗
# ╚═╝╚═╝ ╩   ╩ ╩╩═╝╩═╝  ╩╚═╚═╝╚═╝╩╚═╝╝╚╝  ╝╚╝╩ ╩╩ ╩╚═╝╚═╝

filled_regions = get_multiple_elements()

filter_type = ISelectionFilter_Classes([FilledRegion])
selected_filled_regions = selection_filter(filter_type, filled_regions)

region_id = []
region_names = []

for region in selected_filled_regions:
    region_name = region.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsValueString()
    hatch_names = ["TR", "AMR"]
    if region_name in hatch_names:
        region_names.append(region_name)
        region_id.append(region.Id)


# sorted_regions = sorted(region_names)
#
# counter = 0
# for rg in set(sorted_regions):
#     counter += 1
#     print("{}- {}".format(str(counter).zfill(2), rg))


highlight_selected_elements(region_id)


#     # ---------------------------------------------------------
#
#     if region_name != "TR":
#         all_fr.append(region.Id)
#
# highlight_selected_elements(all_fr)
#
# with rvt_transaction(doc, __title__):
#     active_view.HideElements(List[ElementId](all_fr))

# =====================================================================================================
# ╔═╗╦╦  ╦  ╔═╗╔╦╗  ╦═╗╔═╗╔═╗╦╔═╗╔╗╔  ╦╔╗╔  ╔═╗╔═╗╔╦╗╦╦  ╦╔═╗  ╦  ╦╦╔═╗╦ ╦
# ╠╣ ║║  ║  ║╣  ║║  ╠╦╝║╣ ║ ╦║║ ║║║║  ║║║║  ╠═╣║   ║ ║╚╗╔╝║╣   ╚╗╔╝║║╣ ║║║
# ╚  ╩╩═╝╩═╝╚═╝═╩╝  ╩╚═╚═╝╚═╝╩╚═╝╝╚╝  ╩╝╚╝  ╩ ╩╚═╝ ╩ ╩ ╚╝ ╚═╝   ╚╝ ╩╚═╝╚╩╝

# filled_region = FilteredElementCollector(doc, active_view.Id).OfClass(FilledRegion).WhereElementIsNotElementType().ToElements()
#
# for fr in filled_region:
#     region_name = fr.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsValueString()
#     hatch_names = ["TR", "AMR"]
#     if region_name in hatch_names:
#         print(True)


# ====================================================================================
# ╔═╗╔═╗╔╦╗  ╦  ╦╦╔═╗╦ ╦  ╔═╗╦╦ ╔╦╗╔═╗╦═╗  ╦  ╦╦╔═╗╦╔╗ ╦╦  ╦╔╦╗╦ ╦
# ╚═╗║╣  ║   ╚╗╔╝║║╣ ║║║  ╠╣ ║║  ║ ║╣ ╠╦╝  ╚╗╔╝║╚═╗║╠╩╗║║  ║ ║ ╚╦╝
# ╚═╝╚═╝ ╩    ╚╝ ╩╚═╝╚╩╝  ╚  ╩╩═╝╩ ╚═╝╩╚═   ╚╝ ╩╚═╝╩╚═╝╩╩═╝╩ ╩  ╩


# filters = active_view.GetFilters()
#
# sorted_filter = sorted(filters, key=lambda x: doc.GetElement(x).Name)
#
# filter_lst = []
#
# for f_id in sorted_filter:
#     filter_el = doc.GetElement(f_id)
#     filter_lst.append(filter_el)
#
# sel_filter = forms.SelectFromList.show(filter_lst, multiselect=True, name_attr="Name", button_name="Select Filter")
#
# with rvt_transaction(doc, __title__):
#     for _filter in sel_filter:
#         filter_is_on = active_view.GetFilterVisibility(_filter.Id)
#         if not filter_is_on:
#             active_view.SetFilterVisibility(_filter.Id, True)
#         else:
#             active_view.SetFilterVisibility(_filter.Id, False)



# ====================================================================================1
# ╔═╗╔═╗╔╦╗  ╔═╗╦  ╦    ╦  ╦╦╔═╗╦ ╦  ╔═╗╦╦ ╔╦╗╔═╗╦═╗╔═╗
# ║ ╦║╣  ║   ╠═╣║  ║    ╚╗╔╝║║╣ ║║║  ╠╣ ║║  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╚═╝ ╩   ╩ ╩╩═╝╩═╝   ╚╝ ╩╚═╝╚╩╝  ╚  ╩╩═╝╩ ╚═╝╩╚═╚═╝

# filters = active_view.GetFilters()
#
# sorted_filter = sorted(filters, key=lambda x: doc.GetElement(x).Name)
#
#
# for f_id in sorted_filter:
#     filter_el = doc.GetElement(f_id)
#     print(filter_el.Name)

# ====================================================================================
# ╔╦╗╦ ╦╔═╗╦  ╦╔═╗╔═╗╔╦╗╔═╗  ╦  ╦╦╔═╗╦ ╦
#  ║║║ ║╠═╝║  ║║  ╠═╣ ║ ║╣   ╚╗╔╝║║╣ ║║║
# ═╩╝╚═╝╩  ╩═╝╩╚═╝╩ ╩ ╩ ╚═╝   ╚╝ ╩╚═╝╚╩╝
# with rvt_transaction(doc, __title__):
#
#     selected_view = get_multiple_elements()
#
#     for i in selected_view:     # type: View
#         if i.CanViewBeDuplicated(ViewDuplicateOption.AsDependent):
#             for num in range(2):
#                 i.Duplicate(ViewDuplicateOption.AsDependent)
