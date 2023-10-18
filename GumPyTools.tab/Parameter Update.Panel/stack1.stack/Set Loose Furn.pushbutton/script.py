# -*- coding: utf-8 -*-

__title__ = 'Set Loose Furniture'
__doc__ = """
Setting "(BY USER)" value to
'Manufacturer' type parameter.
Might be a placeholder only
__________________________________
v1: 17 Oct 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit
import xlsxwriter

import clr
clr.AddReference("System")
from System.Collections.Generic import List

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
                         BuiltInCategory.OST_MedicalEquipment])

multi_cat_filter = ElementMulticategoryFilter(list_of_categories)

elements = FilteredElementCollector(doc, active_view.Id).WherePasses(multi_cat_filter).WhereElementIsNotElementType().ToElements()

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    for element in elements:
        el_type_id = element.GetTypeId()
        el_symbol = doc.GetElement(el_type_id)
        # parameter
        manufacturer_val  = el_symbol.get_Parameter(BuiltInParameter.ALL_MODEL_MANUFACTURER)
        manufacturer_val.Set('(BY USER)')

    t.Commit()





