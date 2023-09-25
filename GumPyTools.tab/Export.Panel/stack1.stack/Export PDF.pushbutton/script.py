# -*- coding: utf-8 -*-

__title__ = 'PDF Current View'
__doc__ = """
This script will export the overall
plan view in 1-200 on A0 size paper.
- Centered 
- 25%
===================================
1st version: 20230925
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
import os

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
current_view = [active_view.Id]

# 🟡 FILE NAME
model_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(doc.GetWorksharingCentralModelPath())
file_path = model_path
file_name = os.path.splitext(os.path.basename(file_path))[0]

suffix = forms.ask_for_string(
    default='suffix',
    prompt='Enter string to append file name:',
    title='File name'
)

# 🟡 DIRECTORY TO SAVE THE FILE
directory = r"C:\Users\gary_mak\Desktop\PDF"

# 🟢 MAIN CODE
with Transaction(doc, __title__) as t:
    t.Start()

    # PDFExportOptions properties
    options = PDFExportOptions()
    options.AlwaysUseRaster = False
    options.ColorDepth.Color
    options.Combine = True
    options.ExportQuality.DPI4000
    options.FileName = file_name + "_{}".format(suffix)
    options.HideCropBoundaries = True
    options.HideReferencePlane = True
    options.HideScopeBoxes = True
    options.HideUnreferencedViewTags = True
    options.MaskCoincidentLines = True
    options.OriginOffsetX = 0
    options.OriginOffsetY = 0
    options.PaperFormat.ISO_A0
    options.PaperPlacement.Center
    options.RasterQuality.High
    options.ReplaceHalftoneWithThinLines = False
    options.StopOnError = True
    options.ViewLinksInBlue = True
    options.ZoomPercentage = 25
    options.ZoomType.Zoom

    doc.Export(directory, current_view, options)
    t.Commit()
