# -*- coding: utf-8 -*-

__title__ = 'Revit API: Parameters'
__doc__ = """
This script will return parameters
__________________________________
Author: Joven Mark Gumana
"""

# imports
from Autodesk.Revit.DB import *


# variables
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

# main
wall_id = ElementId(139857)
wall = doc.GetElement(wall_id)
# print(wall)

# print("***Parameters***")

# for p in wall.Parameters:
#     print(p)
#     print(".Definition.Name:             {}".format(p.Definition.Name))
#     print(".Definition.BuiltInParameter: {}".format(p.Definition.BuiltInParameter))
#     print(".StorageType:                 {}".format(p.StorageType))
#     print(".IsShared:                    {}".format(p.IsShared))
#     print(".IsReadOnly:                  {}".format(p.IsReadOnly))
#     print("-"*50)

# get built-in parameter
# print("-"*50)
# print("***Built-in Parameter****")
# wall_comments = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
# wall_type = wall.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM)
# # print(wall_comments.AsString())
# print(wall_type.AsValueString())

# wall_type = wall.WallType
# wall_type_description = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION)
# print(wall_type_description.AsString())
# wall_type_mark = wall_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID)
# print(wall_type_mark.AsString())

# set parameter value
# t = Transaction(doc, __title__)
# # t.Start()
# #
# # wall_comments = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
# # wall_comments.Set("I've changed the comment text")
# # print(wall_comments.AsString())
# #
# #
# # t.Commit()

t = Transaction(doc, __title__)
t.Start()

all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

for wall in all_walls:
    wall_mark = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
    wall_mark.Set(str(wall.Id))
    print(wall.Id)

t.Commit()