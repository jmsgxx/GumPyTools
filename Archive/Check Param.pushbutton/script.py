# -*- coding: utf-8 -*-

__title__ = 'Check Existing Param'
__doc__ = """
This script will check if the parameters
looking for Contech is existing in the model.
__________________________________
v1: 28 Nov 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
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


output = pyrevit.output.get_output()
output.center()
output.resize(300, 600)

current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H:%M:%S hrs')

# SHARED PARAMETER FILE
sp_file  = app.OpenSharedParameterFile()

# 📃 Get Parameter Bindings Map.
bm = doc.ParameterBindings

# 💡 Create a forward iterator
iter = bm.ForwardIterator()
iter.Reset()

# 🔁 Iterate over the map and collect Names
param_names = []
while iter.MoveNext():
    d = iter.Key
    param_names.append(d.Name)

# ✅ Check if Parameters are loaded:
req_params = ['Subroom ACMV Type Text', 'Room ACMV Type Text', 'Room Temperature Winter Text 1 condition', 'Room Relative Humidity Summer Text 1 condition',
              'Room Temperature Summer Text 1 condition', 'Room Relative Humidity Winter Text 1 condition']
missing_params = [p for p in req_params if p not in param_names]

output.print_md('### MISSING PARAMETERS: | {}'.format(time_stamp))

# 👀 Display Missing Parameters
if missing_params:
    for p_name in missing_params:
        print(p_name)
else:
    print('All parameters set!')

