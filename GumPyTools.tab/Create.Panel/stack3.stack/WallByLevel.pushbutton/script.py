# -*- coding: utf-8 -*-

__title__ = 'WallByLevel'
__doc__ = """
This script will create a constrained wall in
Top Level by selecting a line or group of
lines.

HOW TO:
1. Select the line/s and hit finish.
2. On the pop up menu, select the desired wall type and
desired top level and hit 'Create'.
__________________________________
v1. 26 Mar 2024
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import FlexForm, Label, ComboBox, Separator, Button
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, CurvesFilter
from Snippets._context_manager import rvt_transaction, try_except
from Autodesk.Revit.DB import *
from pyrevit import forms
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
selection = uidoc.Selection     # type: Selection
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

# =====================================================================================================
wall_type = FilteredElementCollector(doc).OfClass(WallType).FirstElement()

line_selection = get_multiple_elements()

if not line_selection:
    with try_except():
        # filter_type = ISelectionFilter_Classes([ModelLine])
        filter_type = CurvesFilter()
        line_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Lines")
        line_selection = [doc.GetElement(dr) for dr in line_list]

        if not line_selection:
            forms.alert("No doors selected. Exiting command.", exitscript=True, warn_icon=False)

wall_id = ElementId(45419)

all_level = FilteredElementCollector(doc).OfClass(Level).ToElements()
level_dict = {level.get_Parameter(BuiltInParameter.DATUM_TEXT).AsString(): level.Id for level in all_level}

wall_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()
wall_type_dict = {wall.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString(): wall.Id for wall in wall_types}
# =====================================================================================================

wall_choice = None
top_level = None

try:
    components = [Label('Select Wall'),
                  ComboBox('wall_type_var', wall_type_dict),
                  Label('Top Level'),
                  ComboBox('level_top', level_dict),
                  Separator(),
                  Button('Create')]

    form = FlexForm('Create Wall', components)
    form.show()
    user_inputs = form.values

    wall_choice = user_inputs['wall_type_var']
    top_level = user_inputs['level_top']

except KeyError as e:
    forms.alert('No input selected', exitscript=True, warn_icon=True)
# =====================================================================================================

with rvt_transaction(doc, __title__):
    try:
        line_list = []
        created_walls = []

        for line in line_selection:     # type: ModelLine
            curve = line.GeometryCurve
            start_pt = curve.GetEndPoint(0)
            end_pt = curve.GetEndPoint(1)
            l_curve = Line.CreateBound(start_pt, end_pt)
            line_list.append(l_curve)

        for el in line_list:
            """
            args: Document, list of curves, ElementID Wall, ElementID Level,
             height dbl, offset dbl, flip bool, struc bool
            """
            created_wall = Wall.Create(doc, el, wall_choice, active_level.Id, 10, 0, False, False)
            created_walls.append(created_wall)

        for wall in created_walls:
            top_cons = wall.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE)
            top_cons.Set(top_level)

    except Exception as e:
        forms.alert(str(e))

    else:
        if created_wall:
            for line in line_selection:
                doc.Delete(line.Id)
