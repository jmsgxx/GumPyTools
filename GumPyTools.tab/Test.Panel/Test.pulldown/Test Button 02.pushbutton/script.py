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

if version < 2021:
	UIunit = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits
else:
	UIunit = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()


def tolist(obj1):
	if hasattr(obj1, "__iter__"):
		return obj1
	else:
		return [obj1]


elements = tolist(UnwrapElement(IN[0]))
new_fam_type_names = tolist(IN[1])
functions = tolist(IN[2])
materials = tolist(UnwrapElement(IN[3]))
widths = tolist(IN[4])
new_fam_types = []

for elem, new_fam_type_name in zip(elements, new_fam_type_names):
	if isinstance(elem, ElementType):
		fam_type = elem
	elif isinstance(elem, Wall):
		fam_type = elem.WallType
	else:
		pass
	try:
		new_fam_type = fam_type.Duplicate(new_fam_type_name)
		layers = []
		for material, width, function in zip(materials, widths, functions):
			if isinstance(function, MaterialFunctionAssignment):
				layerFunction = function
			else:
				layerFunction = System.Enum.Parse(MaterialFunctionAssignment, function)
			layers.append(
				CompoundStructureLayer((UnitUtils.ConvertToInternalUnits(width, UIunit)), layerFunction, material.Id))
		compound = CompoundStructure.CreateSimpleCompoundStructure(layers)
		if fam_type.ToString() != 'Autodesk.Revit.DB.WallType':
			compound.EndCap = EndCapCondition.NoEndCap
		else:
			pass
		new_fam_type.SetCompoundStructure(compound) 	# can stop in here
		new_fam_types.append(new_fam_type)

	except:
		fec = FilteredElementCollector(doc).OfClass(fam_type.GetType())
		type_dict = dict([(Element.Name.__get__(i), i) for i in fec])
		n1 = unicode(new_fam_type_name)
		if n1 in type_dict:
			new_fam_types.append(type_dict[n1])

if isinstance(IN[0], list):
	OUT = new_fam_types
else:
	OUT = new_fam_types[0]