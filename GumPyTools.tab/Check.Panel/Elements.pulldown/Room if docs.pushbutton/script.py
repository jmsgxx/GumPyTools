# -*- coding: utf-8 -*-

__title__ = 'Room Docs'
__doc__ = """
***MUST RUN ON THE LEVEL YOU WANT TO CHECK***

This script will check if the rooms are documented on sheets.

NOTE: RLS Sheets to have either DEPARTMENTAL  - BLP or 
REPEATABLE - BLP as value for Rooms_Classification_BLP Parameter.

HOW TO:
1. Select department. This will filter the sheets.
2. Interface will pop up. Select parameters based on the organization
of sheets.
3. Print statement will be shown in the end.
__________________________________
v2. 08 Jan 2024 - fixed datatype comparison
v1. 31 Dec 2023

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Autodesk.Revit.DB import *
import math
from Autodesk.Revit.DB.Architecture import Room
import pyrevit
from pyrevit import forms
import sys
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
# ===================================================================================================


def get_room_center(room_el):
    """
    get the center of the room
    """
    bounding = room_el.get_BoundingBox(active_view)
    loc_pt = room_el.Location
    if bounding and loc_pt:
        center = (bounding.Max + bounding.Min) * 0.5
        room_center = XYZ(center.X, center.Y, loc_pt.Point.Z)
        return room_center
# ===================================================================================================


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]
# ===============================================================================
# ✅ first UI

sheet_all = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
f_sheet_all = [i for i in sheet_all if i is not None]
sheet_all = list(set(f_sheet_all))
lst_sheet = [item.LookupParameter('Sheet Department').AsString() for item in sheet_all]     # sheet with 'Sheet Department'
sheet_dict_all = {name: name for name in lst_sheet}     # dictionary of department

# ===============================================================================
user_dept = None
try:
    components = [Label('Select Department to Check'),
                  ComboBox('user_dept', sheet_dict_all),
                  Separator(),
                  Button('Select Department')]

    form = FlexForm('Check Rooms if on Sheet', components)

    form.show()
    user_inputs = form.values
    user_dept      = user_inputs['user_dept']

except KeyError:
    forms.alert("No parameter selected.\nExiting Command.", exitscript=True, warn_icon=True)
# ===============================================================================
# 🟠🟠🟠 COLLECT ALL SHEETS

user_parameter = 'Sheet Department'
all_shared_param = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()

param_element = None

for shared_param in all_shared_param:
    if shared_param.Name == user_parameter:
        param_element = shared_param
        break

f_param = ParameterValueProvider(param_element.Id)
evaluator = FilterStringEquals()
f_param_value = user_dept

f_rule = FilterStringRule(f_param, evaluator, f_param_value)
filter_name = ElementParameterFilter(f_rule)

all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
    .WherePasses(filter_name) \
    .ToElements()


# 🟠 COLLECT ALL ROOMS
level_filter = None
try:

    level_filter = active_level.Id

except AttributeError:
    forms.alert("Go to view with level.\nTry again.", exitscript=True)

rooms = FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_Rooms) \
    .WherePasses(ElementLevelFilter(level_filter)) \
    .ToElements()



# =================================================================================
# 1️⃣ GET RELEVANT PARAMETERS

# initiate an empty dictionary
sheet_dict = {}
sheet_rm_dept = {}
sheet_dwg_type = {}
room_class_dict = {}

# sheets
if all_sheets:
    for sheet in all_sheets:    # type: ViewSheet
        sht_sheet_dept  = sheet.LookupParameter('Sheet Department').AsString()
        room_dept       = sheet.LookupParameter('Room Department').AsString()
        dwg_type        = sheet.LookupParameter('Drawing Type').AsString()
        if sht_sheet_dept:
            sheet_dict[sht_sheet_dept]      = sht_sheet_dept
        if room_dept:
            sheet_rm_dept[room_dept]    = room_dept
        if dwg_type:
            sheet_dwg_type[dwg_type]    = dwg_type


    # rooms
    for room in rooms:
        room_class = room.LookupParameter('Department_BLP').AsString()
        if room_class:
            room_class_dict[room_class] = room_class
else:
    forms.alert("'{}'\nParameter doesn't exist.".format(user_dept.upper()), exitscript=True)

# =================================================================================
# 2️⃣ UI
try:
    components = [Label('Sheet Department:'),
                  ComboBox('sheet_dept', sheet_dict),
                  Label('Sheet Room Department:'),
                  ComboBox('room_dept', sheet_rm_dept),
                  Label('Sheet Drawing Department:'),
                  ComboBox('dwg_type', sheet_dwg_type),
                  Separator(),
                  Label('Room Department:'),
                  ComboBox('rm_class', room_class_dict),
                  Separator(),
                  Label('Mark the missing rooms?'),
                  CheckBox('with_mark', 'Mark room center'),
                  Separator(),
                  Button('Select')]

    form = FlexForm('Check Rooms if on Sheet', components)

    form.show()
    user_inputs = form.values
    # sheets
    sht_depart      = user_inputs['sheet_dept']
    rm_dept         = user_inputs['room_dept']
    dwg_t_dept      = user_inputs['dwg_type']
    # rooms
    room_rm_class      = user_inputs['rm_class']

    with_mark = user_inputs['with_mark']

# =================================================================================
# 3️⃣ MAIN CODE
    sheet_rm_id_lst = []

    for sheet in all_sheets:
        sheet_sht_dept = sheet.LookupParameter('Sheet Department').AsString()
        sheet_rm_dept = sheet.LookupParameter('Room Department').AsString()
        sheet_dwg_type = sheet.LookupParameter('Drawing Type').AsString()
        if sheet_sht_dept == sht_depart:
            if sheet_rm_dept == rm_dept:
                if sheet_dwg_type == dwg_t_dept:
                    viewport_id = sheet.GetAllViewports()
                    for _id in viewport_id:
                        viewport = doc.GetElement(_id)
                        view_id = viewport.ViewId
                        view = doc.GetElement(view_id)

                        if view.ViewType == ViewType.FloorPlan:

                            room_collector = FilteredElementCollector(doc, view.Id) \
                                .OfCategory(BuiltInCategory.OST_Rooms) \
                                .ToElements()

                            for rm in room_collector:   # type: Room
                                sheet_room_id = rm.Id
                                sheet_rm_id_lst.append(sheet_room_id)

    # ---------------------------------------------------------------------------------------------
    rooms_lst = []

    for room in rooms:
        room_class = room.LookupParameter('Rooms_Classification_BLP').AsString()
        room_dept_param = room.LookupParameter('Department_BLP')
        if room_dept_param:
            room_dept = room_dept_param.AsString()
            if room_dept == room_rm_class:
                if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                    # room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                    room_id = room.Id.IntegerValue
                    room_name = room.LookupParameter('Room_Name_BLP').AsString()
                    room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                    if room.Area > 0:
                        rooms_lst.append({room_name: room_id})

    missing_rm = []

    for room_dict in rooms_lst:
        for rm_name, rm_id in room_dict.items():
            if str(rm_id) not in [str(item) for item in sheet_rm_id_lst]:
                missing_rm.append("{} - Id:{}".format(rm_name, rm_id))

                if with_mark:
                    #  create circle at the center of missing  rooms
                    with Transaction(doc, __title__) as t:
                        t.Start()

                        el_id = ElementId(rm_id)
                        find_room = doc.GetElement(el_id)
                        normal = XYZ.BasisZ
                        origin_point = get_room_center(find_room)
                        if origin_point:
                            plane = Plane.CreateByNormalAndOrigin(normal, origin_point)
                            radius = 15
                            start_angle = 0.0
                            end_angle = 2.0 * math.pi
                            arc = Arc.Create(plane, radius, start_angle, end_angle)
                            circ_elements = [doc.Create.NewDetailCurve(active_view, arc)]

                        for el in circ_elements:
                            color = Color(255, 0, 0)
                            ogs = OverrideGraphicSettings().SetProjectionLineColor(color)
                            active_view.SetElementOverrides(el.Id, ogs)

                        t.Commit()

    # -------------------------------------------------------------------------------------
    # print statement
    output = pyrevit.output.get_output()
    output.center()
    output.resize(300, 500)

    if len(missing_rm) == 0:
        print("No missing rooms. All rooms are documented")
    else:
        print("=" * 50)
        print("Rooms not documented")
        print("=" * 50)
        for index, item in enumerate(sorted(missing_rm), start=1):
            print("{}. {}".format(str(index).zfill(2), item))

except KeyError:
    forms.alert("No parameter selected.\nExiting Command.", exitscript=True, warn_icon=True)
