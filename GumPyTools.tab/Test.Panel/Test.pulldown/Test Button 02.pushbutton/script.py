# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
import xlsxwriter
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
doc = __revit__.ActiveUIDocument.Document   # type: Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

ffl_list = []
sfl_list = []

with Transaction(doc, __title__) as t:
    t.Start()


    for level in all_levels:
        if "FFL" in level.Name:
            ffl_list.append(level)
        elif "ffl" in level.Name:
            ffl_list.append(level)

    for ffl in ffl_list:
        for sfl in sfl_list:
            part_ffl = ffl.Name.split('_')
            part_ffl = ffl.Name.split('_')
            if part_ffl[0] == part_ffl[0]:
                num_def_param = ffl.LookupParameter('Number of Defendants')
                ffl_num_def = ffl.LookupParameter('Number of Defendants')
                ffl_num_def.Set(num_def_param.AsInteger())


    t.Commit()




