# -*- coding: utf-8 -*-

__title__ = 'Export View Set'
__doc__ = """
This script will export the selected
view set to pdf. Will always be combined
by default.
Currently the same as 'PDF By View Set'
without selecting the destination file.

NOTE: By using this export, label names
on pdf is already set and ready for extraction
via Bluebeam.

HOW TO:
- Run Command.
- Select view set.
- Wait for confirmation.

__________________________________
v2. 02 Jan 20234 - UI Added
v1. 05 Dec 2023
Author: Joven Mark Gumana


TODO: Study how to pdf multiple file
on view set.
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button)
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

current_datetime = datetime.now()
current_date = current_datetime.strftime('%Y''%m''%d')
current_time = current_datetime.strftime('%H.%M.%S')
time_stamp = "_{}-{}".format(current_date, current_time)

# 🟡 DIRECTORY TO SAVE THE FILE
directory = r"C:\Users\gary_mak\Desktop\PDF"

# 🟢 MAIN CODE
with Transaction(doc, __title__) as t:
    t.Start()
    file_name = None

    # =============================================================================================
    # 🔵 COLLECT SHEETS
    sheet_set_collector = FilteredElementCollector(doc).OfClass(ViewSheetSet).ToElements()
    collector_name = sorted([item.Name for item in sheet_set_collector])
    # 🟢 CREATE A DICTIONARY OF VIEW SET
    collector_dict = {name: name for name in collector_name}

    # =============================================================================================
    # 🟠 CREATE A DICTIONARY OF PAPER SIZE
    paper_size_dict = {
        "A0": ExportPaperFormat.ISO_A0,
        "A1": ExportPaperFormat.ISO_A1,
        "A2": ExportPaperFormat.ISO_A2,
        "A3": ExportPaperFormat.ISO_A3,
        "A4": ExportPaperFormat.ISO_A4,
    }

    # =============================================================================================
    # 🟦 UI
    try:
        components = [Label('View Set Name:'),
                      ComboBox('view_set', collector_dict),
                      Label('Paper Size:'),
                      ComboBox('paper_size', paper_size_dict),
                      Separator(),
                      Button('Select')]

        form = FlexForm('PDF Set', components)

        form.show()
        user_inputs = form.values
        # sheets
        v_set   = user_inputs['view_set']
        p_size  = user_inputs['paper_size']

    except KeyError:
        forms.alert("No selected values. Exiting command.", exitscript=True, warn_icon=True)
    # ===============================================================================================
    # GET THE IDS FOR EXPORT

    sheets_id = []
    for view_set in sheet_set_collector:
        file_name = view_set.Name
        if view_set.Name == v_set:
            for sheet in view_set.Views:
                sheets_id.append(sheet.Id)
            break


    # ===============================================================================================
    # ⭕ MAIN CODE PDFEXPORT
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
    options.PaperFormat = p_size
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
            forms.alert('Print finish.You can find the file on "Desktop/PDF" folder.', exitscript=False)

    # HANDLE ERROR JUST IN CASE
    except Exception as e:
        print("An error occurred: {}".format(e))

    t.Commit()


