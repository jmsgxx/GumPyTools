# -*- coding: utf-8 -*-

__title__ = 'Export View Set'
__doc__ = """
TEST
===================================
v1. 04 Dec 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
import os
from datetime import datetime

import clr
clr.AddReference("System")
from System.Collections.Generic import List

from pyrevit import forms

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
current_time = current_datetime.strftime('%Y''%m''%d')
current_date = current_datetime.strftime('%H.%M.%S')
time_stamp = "_{}-{}".format(current_time, current_date)

# 🟡 DIRECTORY TO SAVE THE FILE
directory = r"C:\Users\gary_mak\Desktop\PDF"




# 🟢 MAIN CODE
with Transaction(doc, __title__) as t:
    t.Start()

    # PDFExportOptions properties
    ExportPDFSettings.FindByName(doc, "RADS1")
    options = PDFExportOptions()
    options.AlwaysUseRaster = False
    options.ColorDepth = ColorDepthType.Color
    options.Combine = False
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
        if doc.Export(directory, current_view, options):
            # SHOW NOTIFICATION THAT PRINT IS FINISHED
            forms.alert('Print finish.You can find the file on "Desktop/PDF" folder.', exitscript=True)

    # HANDLE ERROR JUST IN CASE
    except Exception as e:
        print("An error occurred: {}".format(e))

    t.Commit()
