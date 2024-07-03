# -*- coding: utf-8 -*-

__title__ = 'Command Log'
__doc__ = """
Log for used Commands
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script
from Autodesk.Revit.UI.Selection import Selection
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

file_path = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools\log_info\logger.csv'

data = []

with open(file_path, 'r') as csvfile:
    lines = csvfile.readlines()
    for l in lines:
        part_lines = l.strip().split(',')
        if len(part_lines) >= 2:
            user = part_lines[0]
            computer = part_lines[1]
            command = part_lines[2]
            model = part_lines[5]
            date = part_lines[6]
            time = part_lines[7]
            data.append([user, computer, command, model, date, time])



output.resize(800, 700)
output.print_table(table_data=data,
                   title='Command Log',
                   columns=['User', 'Computer', 'Command', 'Model', 'Date', 'Time'],
                   formats=['', '', '', '', '', ''])
