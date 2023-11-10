# -*- coding: utf-8 -*-

__title__ = 'BS Devices Extract'
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
1. Opem MEP model
2. Go to the desired Level
3. Make sure AR Link is loaded and 
visible in the view.
4. Click the button and let it run.
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
import xlsxwriter
import pyrevit
from pyrevit import script, forms, revit
from datetime import datetime

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

# 🟦 ROOM
all_links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# Find the specific link
ar_model = None
for link in all_links:
    link_name = link.Name
    if 'ARC' in link_name:
        ar_model = link

linked_doc = ar_model.GetLinkDocument()
all_rooms_in_link_level = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()


# ⭕ PREPARE EXCEL EXPORT
workbook = xlsxwriter.Workbook(r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\Output\Data Devices from MEP.xlsx')
worksheet = workbook.add_worksheet()
headings = ['Element ID', 'Category', 'Family', 'Type', 'Image', 'PosX', 'PosY', 'PosZ', 'Room']
for i, heading in enumerate(headings):
    worksheet.write(0, i, heading)

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:

    t.Start()
    # # 🟢 ROOM
    # for room_link in all_rooms_in_link_level:
    #     if room_link and room_link.Location:    # exclude the unplaced rooms
    #         room_loc = room_link.Location.Point
    #
    #         room_copy = doc.Create.NewRoom(active_level, UV(room_loc.X, room_loc.Y))
    #         #  name
    #         room_copy_name = room_copy.get_Parameter(BuiltInParameter.ROOM_NAME)
    #         rm_link_name = room_link.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
    #         if rm_link_name:
    #             room_copy_name.Set(str(rm_link_name.upper()))
    #         else:
    #             continue
    #
    #         # number
    #         room_copy_number = room_copy.get_Parameter(BuiltInParameter.ROOM_NUMBER)
    #         rm_link_number = room_link.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    #         if rm_link_number:
    #             room_copy_number.Set(str(rm_link_number))
    #         else:
    #             continue
    #         # print
    #         # print("Room Name:   {}".format(rm_link_name))  # print statement to check rm_link_name
    #         # print("Room Number: {}".format(rm_link_number))  # print statement to check rm_link_number
    #         # print('-' * 50)
    #
    # # CHECK THE CURRENT MODEL AFTER THE CREATION OF TEMPORARY ROOM
    # current_level_filter = ElementLevelFilter(active_level.Id)
    #
    # rooms_current = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Rooms)\
    #     .WherePasses(current_level_filter).WhereElementIsNotElementType().ToElements()
    #
    # print("Total Room in link:      {}".format(len(all_rooms_in_link_level)))
    # print("Total Room in current:   {}".format(len(rooms_current)))
    #
    # for room_cur in rooms_current:
    #     print(room_cur.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString())
    #     print(room_cur.Number)
    #     print('=' * 50)

# ================================================================================================================
    # 🔵 ELEMENT
    row = 1
    for element in all_elements_in_level:
        if element:
            #  type param
            el_type_id = element.GetTypeId()
            el_type = doc.GetElement(el_type_id)
            if el_type:
                type_description    = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)
                type_image          = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_IMAGE)

            #  instance param
            element_id = element.Id
            category_name = element.Category.Name
            family_name = element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()

            element_location = element.Location
            if element_location is not None:
                el_loc_point = element_location.Point
                pos_x = el_loc_point.X
                pos_y = el_loc_point.Y
                pos_z = el_loc_point.Z

            # room of elements
            room_active = element.Room[phase]
            if room_active:
                room_active_number  = room_active.Number
                room_num_split      = room_active_number.split('.')
                # print("--x---" * 3)
                if len(room_num_split) < 4:
                    new_room_number     = room_num_split[0]+"."+room_num_split[1]+"."+room_num_split[2]+".01"
                    room_active_number  = new_room_number
                #     print(room_active_number)
                # else:
                #     print(room_active_number)


            # 🆗 WRITE TO EXCEL
            worksheet.write('A' + str(row+1), int((str(element_id))))
            worksheet.write('B' + str(row+1), category_name)
            worksheet.write('C' + str(row+1), family_name)
            worksheet.write('D' + str(row+1), type_description.AsValueString())
            worksheet.write('E' + str(row+1), type_image.AsValueString().strip())
            worksheet.write('F' + str(row+1), pos_x)
            worksheet.write('G' + str(row+1), pos_y)
            worksheet.write('H' + str(row+1), pos_z)
            worksheet.write('I' + str(row+1), room_active_number)

            row += 1

    workbook.close()

    t.Commit()

    # if t.GetStatus() == TransactionStatus.Started:
    #     t.RollBack()
# ==========================================================================================================

current_datetime = datetime.now()
time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')
forms.alert('Excel exported!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)

