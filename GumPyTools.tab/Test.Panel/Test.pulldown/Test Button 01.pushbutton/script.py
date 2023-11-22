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
import pyrevit
from pyrevit import script, forms, revit
from System.Collections.Generic import List
from datetime import datetime
import xlsxwriter

import clr
clr.AddReference("System")


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application
sp_file  = app.OpenSharedParameterFile()

# 📃 Get Parameter Bindings Map.
bm = doc.ParameterBindings

# 💡 Create a forward iterator
itor = bm.ForwardIterator()
itor.Reset()

# 🔁 Iterate over the map and collect Names
param_names = []
while itor.MoveNext():
    d = itor.Key
    param_names.append(d.Name)

# ✅ Check if Parameters are loaded:
req_params = ['Subroom ACMV Type Text', 'Room ACMV Type Text', 'Room Temperature Winter Text 1 condition', 'Room Relative Humidity Summer Text 1 condition',
              'Room Temperature Summer Text 1 condition', 'Room Relative Humidity Winter Text 1 condition']
missing_params = [p for p in req_params if p not in param_names]

# 👀 Display Missing Parameters
if missing_params:
    print('Missing Parameters:')
    for p_name in missing_params:
        print(p_name)
else:
    print('All parameters set!')

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
# with Transaction(doc, __title__) as t:
#     t.Start()
#     # CHANGE HERE
#     t.Commit()

