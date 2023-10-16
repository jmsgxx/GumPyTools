# -*- coding: utf-8 -*-

__title__ = 'TR Area Required'
__doc__ = """
This button will update all the TR
to 19.0 sqm in Area_Reqd param as double.
__________________________________
v1: 11 OCt 2023
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit

import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ========================================

app      = __revit__.Application
rvt_year = int(app.VersionNumber)
def convert_internal_units(value, get_internal = True, units='m'):
    #type: (float, bool, str) -> float
    """Function to convert Internal units to meters or vice versa.
    :param value:        Value to convert
    :param get_internal: True to get internal units, False to get Meters
    :param units:        Select desired Units: ['m', 'm2']
    :return:             Length in Internal units or Meters."""

    if rvt_year >= 2021:
        from Autodesk.Revit.DB import UnitTypeId
        if   units == 'm' : units = UnitTypeId.Meters
        elif units == "m2": units = UnitTypeId.SquareMeters
        elif units == 'cm': units = UnitTypeId.Centimeters
    else:
        from Autodesk.Revit.DB import DisplayUnitType
        if   units == 'm' : units = DisplayUnitType.DUT_METERS
        elif units == "m2": units = DisplayUnitType.DUT_SQUARE_METERS
        elif units == "cm": units = DisplayUnitType.DUT_CENTIMETERS

    if get_internal:
        return UnitUtils.ConvertToInternalUnits(value, units)
    return UnitUtils.ConvertFromInternalUnits(value, units)



# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

with forms.WarningBar(title='Pick an element:'):
    selected_element = revit.pick_element()

el_cat = selected_element.Category.Name

if el_cat != 'Rooms':
    forms.alert('Just pick a Room', exitscript=True)



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()

    # param = selected_element.LookupParameter('AreaReqd')
    # if param:
    #     value = convert_internal_units(62.3, True)
    #     param.Set(value)

    param = selected_element.get_Parameter(BuiltInParameter.ROOM_FINISH_CEILING)
    if param:
        # value = convert_internal_units(62.3, True)
        param.Set('C10')



    t.Commit()

