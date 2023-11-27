# -*- coding: utf-8 -*-

__title__ = 'Test Button 02'
__doc__ = """
This script will get the parameters
needed on BS elements such as:
- Data Devices
- Electrical Fixtures
- Communication Devices
- Security Devices
- Nurse Call Devices
========================================
HOW TO:
1. Open MEP model
2. Go to the desired Level
3. Make sure AR Link is loaded and 
visible in the view.
4. Click the button, select a file
destination with a file name of your
choice and let it run.
A prompt will confirm that Excel file is
created.

This should be done inside the MEP model.
Why?

Type parameters inside the link model is
unreachable unlike the instances. Hence,
the BS data extraction cannot be done
inside AR model. As a workaround, it 
should be done inside the MEP. The
script will temporarily recreate the
rooms inside the MEP model based on 
the AR model properties then it will 
roll back and undo the newly created room.
----------------------------------------
v1: 09 Nov 2023

Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
from pyrevit import script, forms, revit
from datetime import datetime
import time
import xlsxwriter
import clr
clr.AddReference("System")


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
# phase
all_phase = list(doc.Phases)
phase = (all_phase[1])

# output window
output = script.get_output()
output.center()


# ╔═╗═╗ ╦╔═╗╔═╗╦
# ║╣ ╔╩╦╝║  ║╣ ║
# ╚═╝╩ ╚═╚═╝╚═╝╩═╝
# ===========================================================================================================
# ⭕ PREPARE EXCEL EXPORT
file_path = forms.save_excel_file(title='Select destination file')
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
headings = ['Element ID', 'Category', 'Family', 'Type', 'Image', 'PosX', 'PosY', 'PosZ', 'Room']
for i, heading in enumerate(headings):
    worksheet.write(0, i, heading)
worksheet.set_column(0, len(headings), 30)
# ===========================================================================================================

# 🟩 BS elements
list_of_categories = List[BuiltInCategory]([
    BuiltInCategory.OST_DataDevices,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_CommunicationDevices,
    BuiltInCategory.OST_SecurityDevices,
    BuiltInCategory.OST_NurseCallDevices])

level_filter = ElementLevelFilter(active_level.Id)
category_filter = ElementMulticategoryFilter(list_of_categories)
combined_filter = LogicalAndFilter(category_filter, level_filter)

all_elements_in_level = FilteredElementCollector(doc).WherePasses(combined_filter).WhereElementIsNotElementType().ToElements()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:

    t.Start()

    # CHECK THE CURRENT MODEL AFTER THE CREATION OF TEMPORARY ROOM
    current_level_filter = ElementLevelFilter(active_level.Id)

    rooms_current = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Rooms)\
        .WherePasses(current_level_filter).WhereElementIsNotElementType().ToElements()
    print("Total Room in current:   {}".format(len(rooms_current)))

    for room_cur in rooms_current:
        print('ROOM CREATED')
        print('Room Name: {}'.format(room_cur.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()))
        print('Room Number: {}'.format(room_cur.Number))
        print('=' * 50)

# ================================================================================================================
    # 🔵 ELEMENT
    room_numbers = []   # extracted from temp rooms
    room_name = None

    row = 1
    for element in all_elements_in_level:
        if element:
            #  instance param
            element_id = element.Id
            category_name = element.Category.Name
            family_name = element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()

            #  type param
            el_type_id = element.GetTypeId()
            el_type = doc.GetElement(el_type_id)
            if el_type:
                type_description = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)
                type_image = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_IMAGE)

            element_location = element.Location
            if element_location is not None:
                el_loc_point = element_location.Point
                pos_x = el_loc_point.X
                pos_y = el_loc_point.Y
                pos_z = el_loc_point.Z

            # room of elements
            room_active = element.Room[phase]
            if room_active:
                room_active_name = room_active.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
                room_name = room_active_name  # room name
                room_active_number = room_active.Number  # room number
                room_numbers.append(room_active_number)

        drawings_dict = {}  # initialize a dictionary
        for i in range(len(room_numbers)):
            parts = room_numbers[i].split('.')  # separate the drawing number into parts

            if len(parts) == 4:  # skip those AA.BB.CC.01
                continue

            if room_numbers[i] not in drawings_dict:
                drawings_dict[room_numbers[i]] = 1
            else:
                drawings_dict[room_numbers[i]] += 1
            room_numbers[i] = "{}.{}".format(room_numbers[i], str(drawings_dict[room_numbers[i]]).zfill(2))

        # 🆗 WRITE TO EXCEL
        worksheet.write('A' + str(row + 1), int((str(element_id))))
        worksheet.write('B' + str(row + 1), category_name)
        worksheet.write('C' + str(row + 1), family_name)
        worksheet.write('D' + str(row + 1), type_description.AsValueString())
        worksheet.write('E' + str(row + 1), type_image.AsValueString().strip())
        worksheet.write('F' + str(row + 1), pos_x)
        worksheet.write('G' + str(row + 1), pos_y)
        worksheet.write('H' + str(row + 1), pos_z)
        for room_number in room_numbers:
            worksheet.write('I' + str(row + 1), room_number)

        row += 1  # increment row at the end of the loop

    workbook.close()

    if t.GetStatus() == TransactionStatus.Started:
        t.RollBack()
# ==========================================================================================================
current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')
forms.alert('Excel exported!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)


