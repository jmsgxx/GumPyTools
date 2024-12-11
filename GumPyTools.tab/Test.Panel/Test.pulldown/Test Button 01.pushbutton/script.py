# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """

"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from pyrevit import script
from Snippets._x_selection import get_multiple_elements
from Snippets._context_manager import rvt_transaction
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

all_floor = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).\
    WhereElementIsNotElementType().ToElements()



with rvt_transaction(doc, __title__):
    is_slope = False

    selected_flr = get_multiple_elements()

    for fl in selected_flr:     # type: Floor
        ss_shape = fl.SlabShapeEditor.IsEnabled
        if ss_shape:
            slab_vertices = fl.SlabShapeEditor.SlabShapeVertices
            for vertices in slab_vertices:
                vertex_pt = vertices.Position
                if vertex_pt.Z != 0:
                    is_slope = True
                    break

    for fl in selected_flr:
        mark_param = fl.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
        if is_slope:
            mark_param.Set("Slope")
        else:
            mark_param.Set("Not Slope")









