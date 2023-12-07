# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
ISN'T RESOLVE IN API. STICK WITH COMBINE FOR NOW.
SEE LINK.
https://forums.autodesk.com/t5/revit-api-forum/revit-2022-pdfexportoptions-isvalidnamingrule-always-return-true/td-p/11119662
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from datetime import datetime
import os
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
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

    try:

        # 🟩 sub-transaction start
        st = SubTransaction(doc)
        st.Start()
        illegal_char = ['\\', '/', ':', '*', '?', '<', '>', '"', '|']

        sheet_set_collector = FilteredElementCollector(doc).OfClass(ViewSheetSet)
        collector_name = sorted([item.Name for item in sheet_set_collector])
        chosen_view_set = forms.SelectFromList.show(collector_name, button_name='Select View Set')
        if not chosen_view_set:
            raise Exception("No view set chosen")
        else:
            sheets_id = []
            for view_set in sheet_set_collector:
                if view_set.Name == chosen_view_set:
                    for sheet in view_set.Views:
                        sht_name_param = sheet.get_Parameter(BuiltInParameter.SHEET_NAME)
                        sht_number_param = sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER)
                        sheet_number = sheet.SheetNumber
                        sheet_name = sheet.Name
                        new_sheet_name = sheet_name
                        sht_number_param.Set(sheet_number)
                        for char in illegal_char:
                            if char in new_sheet_name:
                                new_sheet_name = new_sheet_name.replace(char, "-")
                                sht_name_param.Set(new_sheet_name)
                        sheets_id.append(sheet.Id)
                    break

        # 🟥 sub-transaction commit
        st.Commit()

        options = PDFExportOptions()
        options.AlwaysUseRaster = False
        options.ColorDepth = ColorDepthType.Color
        options.Combine = False
        options.ExportQuality = PDFExportQualityType.DPI4000
        # options.FileName = file_name + time_stamp
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


        if doc.Export(directory, sheets_id, options):
            # SHOW NOTIFICATION THAT PRINT IS FINISHED
            forms.alert('Print finish.You can find the file on "Desktop/PDF" folder.', exitscript=False)

        # 🟪 sub-transaction rollback
        if t.GetStatus() == TransactionStatus.Committed:
            st.RollBack()

    # HANDLE ERROR JUST IN CASE
    except Exception as e:
        print("An error occurred: {}".format(e))

    # finally:
    #     if st.GetStatus() == TransactionStatus.Started:
    #         st.RollBack()

    t.Commit()