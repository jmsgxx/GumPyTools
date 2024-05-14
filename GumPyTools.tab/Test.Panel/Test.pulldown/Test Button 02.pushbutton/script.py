# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
script test
__________________________________
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
import math
from Snippets._x_selection import get_multiple_elements
from Autodesk.Revit.DB import *
from Snippets._context_manager import rvt_transaction
from pyrevit import forms, revit
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from collections import Counter
import sys
import xlrd
import clr
clr.AddReference("System")

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
selection = uidoc.Selection     # type: Selection
# ======================================================================================================

#
# all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
#
#
# directory = forms.pick_excel_file(False, 'Select File')
# wb = xlrd.open_workbook(directory)
#
# sheet = wb.sheet_by_index(0)
#
# data_dict = {}
#
# for rw in range(1, sheet.nrows):
#     key = sheet.cell_value(rw, 0)
#     value = sheet.row_values(rw)[1:]
#     data_dict[key] = value
#
# with Transaction(doc, __title__) as t:
#     t.Start()
#
#     for k, v in data_dict.items():
#         print("{}:{}".format(k, v))
#         # this is just a print statement to show you that the value is a list
#         for item in v:     # this is to loop through the list in values
#             if item == '':      # if item is None type, it will skip
#                 continue
#
#             for element in all_elements:
#                 if element:
#                     if element.Id == ElementId(int(k)):
#                         ifc_guid = element.LookupParameter("IfcGUID")
#                         ifc_guid.Set(v[0])
#                         fab_type = element.LookupParameter("Fabrikationsnummer/Type")
#                         fab_type.Set(v[1])
#                         """
#                         write the rest of the parameter here and see what you will get
#                         """
#
#     t.Commit()

# By Clockwork


def WallOrientation(wall):
	loc = wall.Location
	not_flipped = False
	if hasattr(loc, "Curve"):
		l_curve = loc.Curve
		if hasattr(wall, "Flipped"):
			not_flipped = wall.Flipped
		if str(type(l_curve)) == "Autodesk.Revit.DB.Line":
			if not_flipped:
				return wall.Orientation.ToVector().Reverse()
			else:
				return wall.Orientation.ToVector()
		else:
			direction = (l_curve.GetEndPoint(1) - l_curve.GetEndPoint(0)).Normalize()
			if not_flipped:
				return XYZ.BasisZ.CrossProduct(direction).ToVector().Reverse()
			else:
				return XYZ.BasisZ.CrossProduct(direction).ToVector()
	else:
		return None


elem_width = []
elem_func = []

# By Clockwork
for item in items:
	doc = item.Document

	UIunit = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()

	try:
		counter = 0
		layer_width, layer_func = [], []
		comp_struc = item.WallType.GetCompoundStructure()
		num = comp_struc.LayerCount
		while counter < num:
			layer_width.append(UnitUtils.ConvertFromInternalUnits((comp_struc.GetLayerWidth(counter)), UIunit))
			layer_func.append(comp_struc.GetLayerFunction(counter))
			counter += 1
	except:
		pass
	elem_width.append(layer_width)
	elem_func.append(layer_func)

increments = [[sum(data[:i+1]) for i in range(len(data))] for data in elem_width]

direction = [WallOrientation(x) for x in items]

wall.GetLocation().Translate(direction, (math.fsum(element_width) / 2 - (increments - (element_width / 2)))


# TODO: fix this shit this last part doesn't work, integrate with the deconstructed wall elements