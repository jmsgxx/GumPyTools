# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script is a test.
__________________________________

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
from pyrevit import forms, revit
from datetime import datetime
import pyrevit
import clr
clr.AddReference("System")



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application


collector = FilteredElementCollector(doc).OfClass(ViewSheet)

# 🟡 DIRECTORY TO SAVE THE FILE
directory = r"C:\Users\gary_mak\Desktop\PDF"

with Transaction(doc, __title__) as t:
    t.Start()

    my_view_set = List[ElementId]
    for vs in collector:
        sheet_number = vs.SheetNumber
        sheet_name = vs.Name
        plot_param = vs.LookupParameter('Plot Batch')
        if plot_param and plot_param.AsString() == "RADS1":
            my_view_set.Add(vs.Id)

        view_set = List[my_view_set]


        # Set the PDF export options
        options = PDFExportOptions()
        options.AlwaysUseRaster = False
        options.ColorDepth = ColorDepthType.Color
        options.Combine = False
        options.ExportQuality = PDFExportQualityType.DPI4000
        options.FileName = sheet_number + " - " + sheet_name
        options.HideCropBoundaries = True
        options.HideReferencePlane = True
        options.HideScopeBoxes = True
        options.HideUnreferencedViewTags = True
        options.MaskCoincidentLines = True
        options.OriginOffsetX = 0
        options.OriginOffsetY = 0
        options.PaperFormat = ExportPaperFormat.ISO_A3
        options.PaperPlacement = PaperPlacementType.Center
        options.RasterQuality = RasterQualityType.High
        options.ReplaceHalftoneWithThinLines = False
        options.StopOnError = True
        options.ViewLinksInBlue = True
        options.ZoomPercentage = 100
        options.ZoomType = ZoomType.Zoom

        try:
            if doc.Export(directory, view_set, options):
                # SHOW NOTIFICATION THAT PRINT IS FINISHED
                forms.alert('Print finish.You can find the file on "Desktop/PDF" folder.', exitscript=True)

        # HANDLE ERROR JUST IN CASE
        except Exception as e:
            print("An error occurred: {}".format(e))

    t.Commit()

