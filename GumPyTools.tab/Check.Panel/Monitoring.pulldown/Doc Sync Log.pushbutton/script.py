# -*- coding: utf-8 -*-

__title__ = 'Doc Sync Logger'
__doc__ = """
Log for Opened Documents
__________________________________
Author: Joven Mark Gumana
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

file_path = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\log_info\doc_sync_log.csv'
with open(file_path, 'r') as csvfile:
    data = [line.strip().split(',') for line in csvfile]

output.resize(800, 700)
output.print_table(table_data=data,
                   title='Document Sync Log',
                   columns=['User', 'Computer', 'Model', 'Date', 'Time'],
                   formats=['', '', '', '', ''])
