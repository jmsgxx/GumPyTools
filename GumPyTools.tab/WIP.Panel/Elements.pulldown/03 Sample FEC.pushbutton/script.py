# -*- coding: utf-8 -*-

__title__ = 'Filtered Element Collector'
__doc__ = """
This script will collect elements.
__________________________________
Author: Joven Mark Gumana
"""

# imports
from Autodesk.Revit.DB import *

import clr
clr.AddReference("System")
from System.Collections.Generic import List


# variables
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view = doc.ActiveView


# main
all_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
all_walls = FilteredElementCollector(doc).OfClass(Wall).WhereElementIsNotElementType().ToElements()
all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
all_windows = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

# getting the legend, sample
all_legends = [view for view in all_views if view.ViewType == ViewType.Legend]

# for view in all_views:
#     if view.ViewType == ViewType.Legend:
#         all_legends.append(view)
#     else:
#         None

print("All furnitures = {}".format(len(all_legends)))


all_furn_in_view = FilteredElementCollector(doc, active_view.Id)\
                .OfCategory(BuiltInCategory.OST_Furniture)\
                .WhereElementIsNotElementType()\
                .ToElements()

# print(len(all_furn_in_view))

# where passes = to filter element, Element Multi category filter

categories = List[BuiltInCategory]([BuiltInCategory.OST_Walls,
                                   BuiltInCategory.OST_Floors,
                                   BuiltInCategory.OST_Roofs,
                                   BuiltInCategory.OST_Ceilings])

custom_filter = ElementMulticategoryFilter(categories)
my_elements = FilteredElementCollector(doc).WherePasses(custom_filter).WhereElementIsNotElementType().ToElements()
print(my_elements)



# t = Transaction(doc, __title__)
# t.Start()
# t.Commit()