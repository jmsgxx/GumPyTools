# -*- coding: utf-8 -*-

__title__ = 'App Log'
__doc__ = """
Log for Revit instance initialization
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

file_path = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\log_info\app_log.csv'
with open(file_path, 'r') as csvfile:
    lines = csvfile.readlines()
    data = [line.strip().split(',') for line in lines[1:]]

output.resize(800, 700)
output.print_table(table_data=data,
                   title='Revit Instance Log',
                   columns=['User', 'Computer', 'Model', 'Date', 'Time'],
                   formats=['', '', '', '', ''])
