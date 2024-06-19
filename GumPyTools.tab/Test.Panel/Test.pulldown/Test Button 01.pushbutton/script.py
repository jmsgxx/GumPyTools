# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from pyrevit import forms, script
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================
output = script.get_output()
all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
data = []
for i in all_levels:
    level_name = i.Name
    level_val = i.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsValueString()
    data.append((level_name, level_val))

sorted_data = sorted(data, key=lambda x: float(x[1]))

output.center()
output.print_table(table_data=sorted_data,
                   title='Levels',
                   columns=['Level Name', 'Elevation'],
                   formats=["", ""])



