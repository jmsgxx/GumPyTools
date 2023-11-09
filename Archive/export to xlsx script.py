# -*- coding: utf-8 -*-

__title__ = 'Test Button'
__doc__ = """
testing button for anything.
__________________________________
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

# 🟢 GET THE DOORS IN VIEW
doors_in_view = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
active_doors = [door for door in doors_in_view if door.Name != 'STANDARD']
door_list = forms.SelectFromList.show(active_doors, multiselect=True, name_attr='Name', button_name='Select Doors')



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # START THE EXCEL
    workbook = xlsxwriter.Workbook(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\Output\A4 Template _1.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0

    for door in door_list:
        """
        By using XlsxWriter, you cannot append or modify and existing excel file, you can just always write a new file.
        """
        # -------xxx get the type first xxx------
        dr_type_id      = door.GetTypeId()
        door_symbol     = doc.GetElement(dr_type_id)
        # parameter
        door_mark       = door.LookupParameter('Door Number').AsValueString()
        door_height     = door_symbol.LookupParameter('Door Designated Clear Height').AsValueString()
        door_width1     = door_symbol.LookupParameter('Door Designated Clear Width 1').AsValueString()
        door_width2     = door_symbol.LookupParameter('Door Designated Clear Width 2').AsValueString()
        door_remarks    = door_symbol.LookupParameter('Door Remarks').AsValueString()

        worksheet.write('A10', door_mark)
        worksheet.write('B10', door_height+" mm")
        worksheet.write('C10', door_width1 + " + " + door_width2)
        worksheet.write('D10', door_remarks)

        row += 1
    workbook.close()

    t.Commit()





