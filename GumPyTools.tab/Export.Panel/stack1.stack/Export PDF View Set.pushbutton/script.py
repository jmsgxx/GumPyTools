# -*- coding: utf-8 -*-

__title__ = 'Export View Set'
__doc__ = """
This script will export the selected
view set to pdf. Will always be combined
by default.
Current the same as 'PDF By View Set'
without selecting the destination file

TODO: Study how to pdf multiple file
on view set.

HOW TO:
- Run Command.
- Select view set.
- Wait for confirmation.
__________________________________
v1. 05 Dec 2023
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


active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# 🟡 FILE NAME
model_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(doc.GetWorksharingCentralModelPath())
file_path = model_path
file_name = os.path.splitext(os.path.basename(file_path))[0]

current_datetime = datetime.now()
current_date = current_datetime.strftime('%Y''%m''%d')
current_time = current_datetime.strftime('%H.%M.%S')
time_stamp = "_{}-{}".format(current_date, current_time)

# 🟡 DIRECTORY TO SAVE THE FILE
directory = r"C:\Users\gary_mak\Desktop\PDF"

# 🟢 MAIN CODE
with Transaction(doc, __title__) as t:
    t.Start()

    sheet_set_collector = FilteredElementCollector(doc).OfClass(ViewSheetSet)
    collector_name = sorted([item.Name for item in sheet_set_collector])
    chosen_view_set = forms.SelectFromList.show(collector_name, button_name='Select View Set')
    if not chosen_view_set:
        sys.exit()
    else:
        sheets_id = []
        for view_set in sheet_set_collector:
            if view_set.Name == chosen_view_set:
                for sheet in view_set.Views:
                    sheet_number = sheet.SheetNumber
                    sheet_name = sheet.Name
                    sheets_id.append(sheet.Id)
                break
    options = PDFExportOptions()
    options.AlwaysUseRaster = False
    options.ColorDepth = ColorDepthType.Color
    options.Combine = True
    options.ExportQuality = PDFExportQualityType.DPI4000
    options.FileName = file_name + time_stamp
    options.HideCropBoundaries = True
    options.HideReferencePlane = True
    options.HideScopeBoxes = True
    options.HideUnreferencedViewTags = True
    options.MaskCoincidentLines = True
    options.OriginOffsetX = 0
    options.OriginOffsetY = 0
    options.PaperFormat = ExportPaperFormat.ISO_A3
    # options.PaperOrientation.Auto
    options.PaperPlacement = PaperPlacementType.Center
    options.RasterQuality = RasterQualityType.High
    options.ReplaceHalftoneWithThinLines = False
    options.StopOnError = True
    options.ViewLinksInBlue = True
    options.ZoomPercentage = 100
    options.ZoomType = ZoomType.Zoom

    try:
        if doc.Export(directory, sheets_id, options):
            # SHOW NOTIFICATION THAT PRINT IS FINISHED
            forms.alert('Print finish.You can find the file on "Desktop/PDF" folder.', exitscript=True)

    # HANDLE ERROR JUST IN CASE
    except Exception as e:
        print("An error occurred: {}".format(e))

    t.Commit()


