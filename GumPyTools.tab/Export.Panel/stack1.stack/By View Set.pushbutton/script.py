# -*- coding: utf-8 -*-

__title__ = 'PDF by View Set'
__doc__ = """
THIS IS THE SAME AS EXPORT PDF
WITHOUT SELECTING A DESTINATION
FOLDER.

Cons: Label name isn't set unlike
the PDFExportOptions command.

This script will print the specified
view set. It is advisable to use
the command "View Set Create".

HOW TO:
- Run the command.
- Select the desired view set on
selection interface.
- Select Print Setting on the 
selection interface.
- Find the file on your desktop.
__________________________________
v1. 
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from datetime import datetime
import clr
import os
import sys
clr.AddReference("System")



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

model_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(doc.GetWorksharingCentralModelPath())
file_path = model_path
file_name = os.path.splitext(os.path.basename(file_path))[0]

current_datetime = datetime.now()
current_date = current_datetime.strftime('%Y''%m''%d')
current_time = current_datetime.strftime('%H.%M.%S')

with Transaction(doc, __title__) as t:
    try:
        t.Start()

        # 🟡 DIRECTORY TO SAVE THE FILE
        directory = r"C:\Users\gary_mak\Desktop\PDF"

        print_manager               = doc.PrintManager
        print_manager.PrintRange    = PrintRange.Select
        print_manager.CombinedFile  = True

        view_sheet_setting          = print_manager.ViewSheetSetting

        # 🟢 CHOOSE VIEW SET FROM THE LIST
        my_view_set = None
        collector = FilteredElementCollector(doc).OfClass(ViewSheetSet)
        collector_name = sorted([item.Name for item in collector])
        chosen_view_set = forms.SelectFromList.show(collector_name, button_name='Select View Set')
        if not chosen_view_set:
            sys.exit()
        else:
            for view_set in collector:
                for name_view_set in collector_name:
                    if view_set.Name == chosen_view_set:
                        my_view_set = ViewSet()
                        for sheet in view_set.Views:
                            my_view_set.Insert(sheet)
                        break

        # Set the current view sheet set to your ViewSet
        view_sheet_setting.CurrentViewSheetSet.Views = my_view_set

        # If you want to print to a file, set PrintToFile to true and specify the file path
        print_manager.PrintToFile = True
        print_manager.PrintToFileName = directory[:-3] + "{}-{}-{}.pdf".format(file_name, current_date, current_time)

        # Get the PrintSetup from the active document
        print_setup = doc.PrintManager.PrintSetup

        # 🟡 CHOOSE PRINT SETTING
        my_print_setting = None
        print_collector = FilteredElementCollector(doc).OfClass(PrintSetting).ToElements()
        print_collector_name = sorted(item.Name for item in print_collector)
        chosen_print_setting = forms.SelectFromList.show(print_collector_name, button_name='Select Setting', title='Select Setting')
        if not chosen_print_setting:
            sys.exit()
        else:
            for print_setting in print_collector:
                if print_setting.Name == chosen_print_setting:
                    my_print_setting = print_setting
                    break

        # Set the current print setting
        print_setup.CurrentPrintSetting = my_print_setting

        # Print
        print_manager.SubmitPrint()

        t.Commit()
    except Exception as e:
        pass
