# -*- coding: utf-8 -*-

__title__ = 'Sheet Count'
__doc__ = """
----------------------------------------
v1. 02 Feb 2024
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import script
import clr
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝  variables
# ======================================================================================================

doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection

# ==========================================================x============================================

output = script.get_output()
output.center()

def count_items(item_list, keyword, level):
    collected_lst = []
    for item in item_list:
        sheet_number = item.SheetNumber
        sheet_name = item.Name
        if 'CONTENT PAGE' not in sheet_name and sheet_number.startswith(str(keyword)):
            collected_lst.append(item)

    return "All sheets in {} is {}.".format(str(level), len(collected_lst))


all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType()\
    .ToElements()

b2 = count_items(all_sheets, 'DL0001', 'B2')
b1 = count_items(all_sheets, 'DL0002', 'B1')
lg = count_items(all_sheets, 'DL0003', 'LG')

# print("SHEETS FOR DETAIL LAYOUT ONLY")
# print("-" * 50)
# print(b2)
# print(b1)
# print(lg)
#
# for count in range(15):
#     items = count_items(all_sheets, "DL10{}".format(str(count).zfill(2)), "L{}".format(count))
#     print(items)

dlp = 0
mic = 0
ocp = 0
ss = 0
lp = 0

count = 0
for sheet in all_sheets:    # type: ViewSheet
    sort_cat = sheet.LookupParameter("Sorting category").AsString()
    if sort_cat == "DETAIL LAYOUT PLAN":
        dlp += 1
    elif sort_cat == "MIC":
        mic += 1
    elif sort_cat == "OVERALL CEILING PLAN":
        ocp += 1
    elif sort_cat == "SUNKEN SLAB":
        ss += 1
    elif sort_cat == "LAYOUT PLAN":
        lp += 1

print(" Total 'DETAIL LAYOUT PLAN': {}".format(dlp))
print("Total 'LAYOUT PLAN': {}".format(lp))
print(" Total 'MIC': {}".format(mic))
print(" Total 'OVERALL CEILING PLAN': {}".format(ocp))
print(" Total 'SUNKEN SLAB': {}".format(ss))
print("=" * 50)
print("Total Sheets: {}".format(dlp + mic + ocp + ss + lp))





