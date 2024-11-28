# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
*** DO NOT CREATE A HEADROOM MASS ON A BIG ACTIVE VIEW. MACHINE WILL CRASH. ***

This script will create a mass from an element's surface.

HOW TO:
1. Select the categories you want to check.
    - Stairs
    - Floor
2. Select how you want to create the mass:
    - By Active View - this will create a mass for all the 
    visible elements of selected categories on the view
    - Selection - handpick the elements you would want to create
    the mass and hit 'Finish' at the upper left of the screen
    
WHEN IN DOUBT CONTACT THE AUTHOR: 👇👀
__________________________________
Author: Joven Mark Gumana

v1. 10 Aug 2024
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Snippets._convert import convert_m_to_feet
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button)
from Snippets._x_selection import get_multiple_elements, ISelectionFilter_Classes, StairsFilter
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import clr

clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum

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
output.resize(400, 300)


all_link = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
str_link = None
for link in all_link:
    if "STR" in link.Name:
        str_link = link
link_doc = str_link.GetLinkDocument()


def get_intersect_solid(solid_obj, doc_to_check):
    """ will return a list of intersected objects """
    solid_filter = ElementIntersectsSolidFilter(solid_obj)
    collector = FilteredElementCollector(doc_to_check).WherePasses(solid_filter).ToElements()
    return collector


selected_elements = get_multiple_elements()

if not selected_elements:
    filter_type = ISelectionFilter_Classes([DirectShape])
    stair_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Element")
    selected_elements = [doc.GetElement(el) for el in stair_list]

for element in selected_elements:
    if isinstance(element, DirectShape):
        el_geo = element.get_Geometry(Options())
        for geo_object in el_geo:
            if isinstance(geo_object, Solid):
                solid = geo_object
                collection = get_intersect_solid(solid, link_doc)

                # will return clash except for this categories
                exempt_cat = [BuiltInCategory.OST_Stairs,
                              BuiltInCategory.OST_StairsRailing,
                              BuiltInCategory.OST_Floors]
                sel_el = []
                for _element in collection:
                    el_doc = _element.Document.Title
                    el_id = None
                    if _element.Category.Id.IntegerValue not in [int(cat) for cat in exempt_cat]:
                        level_id = _element.LevelId
                        if level_id != ElementId.InvalidElementId:
                            level_el = doc.GetElement(level_id)
                            if level_el:
                                level_name = level_el.Name
                                el_id = _element.Id
                                el_cat_name = _element.Category.Name
                                print(el_cat_name, el_id, el_doc)
                                sel_el.append(el_id)
                        else:
                            print("Invalid LevelId for {}.".format(el_id))
                            print("No clash.")

                # uidoc.Selection.SetElementIds(List[ElementId](sel_el))







