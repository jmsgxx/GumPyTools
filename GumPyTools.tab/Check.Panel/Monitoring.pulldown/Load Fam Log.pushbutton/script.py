# -*- coding: utf-8 -*-

__title__ = 'Load Fam Logger'
__doc__ = """
Log for Loaded Family in a Document
__________________________________
Author: Joven Mark Gumana

v1. 26 Jul 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection


# ======================================================================================================
output = script.get_output()
output.center()
output.resize(1500, 700)

file_path = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\log_info\fam_logger.csv'
with open(file_path, 'r') as csvfile:
    lines = csvfile.readlines()
    data = [line.strip().split(',') for line in lines[1:]]

output.print_table(table_data=data,
                   title='Document Open Log',
                   columns=['User', 'Computer', 'Loaded To', 'Family Name', 'File Path', 'Date', 'Time'],
                   formats=['', '', '', '', '', '', ''])
