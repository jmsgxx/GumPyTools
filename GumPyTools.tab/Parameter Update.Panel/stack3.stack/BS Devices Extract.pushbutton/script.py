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
import sys


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
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

# 🔴 USER INPUT
# ==============================================================================================================
user_input = forms.ask_for_string(prompt="Did you check if the AR Model is loaded?", title='Check link',
                                  default='Yes or No')
if not user_input:
    sys.exit()

new_user_input = user_input.upper()

if user_input == 'NO':  # stop and try again
    forms.alert("Please check and run the script again.", warn_icon=True, exitscript=True)

#     ▶  START THE SCRIPT
else:

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

    all_elements_in_level = FilteredElementCollector(doc).WherePasses(combined_filter)\
        .WhereElementIsNotElementType().ToElements()

    # 🟧 Check the link
    all_links_view = FilteredElementCollector(doc, active_view.Id).OfClass(RevitLinkInstance).ToElements()

    # clean the name of the links
    new_link_lst = []
    for links in all_links_view:
        link_name = links.Name
        parts_link = link_name.split(':')
        new_sel_link = parts_link[0] + ":" + parts_link[1]
        new_link_lst.append(new_sel_link)

    selected_link = forms.SelectFromList.show(new_link_lst, multiselect=False, button_name='Select')
    if not selected_link:
        sys.exit()

    # ╔╦╗╔═╗╦╔╗╔
    # ║║║╠═╣║║║║
    # ╩ ╩╩ ╩╩╝╚╝#main
    # =========================================================================================================
    with Transaction(doc, __title__) as t:

        t.Start()

        # Find the specific link
        ar_model = None
        for link in all_links_view:
            #  link type
            link_type = link.GetTypeId()
            link_element = doc.GetElement(link_type)    # type: Element
            # 🟤 get the parameter for 'Room Bounding' on Revit Link
            link_rm_bound = link_element.get_Parameter(BuiltInParameter.WALL_ATTR_ROOM_BOUNDING)  # type: Parameter
            link_name = link.Name
            if selected_link in link_name:
                if link_rm_bound:
                    link_rm_bound.Set(1)    # set to True
                    ar_model = link

        linked_doc = ar_model.GetLinkDocument()

        # 🟦 ROOM
        all_rooms_in_link_level = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Rooms)\
            .WhereElementIsNotElementType().ToElements()

        # 🟢 ROOM
        for index, room_link in enumerate(all_rooms_in_link_level, start=1):
            if room_link and room_link.Location:    # exclude the unplaced rooms
                room_loc = room_link.Location.Point

                room_copy = doc.Create.NewRoom(active_level, UV(room_loc.X, room_loc.Y))
                #  name
                room_copy_name = room_copy.get_Parameter(BuiltInParameter.ROOM_NAME)
                rm_link_name = room_link.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
                if rm_link_name is None:
                    room_copy_name.Set("")
                else:
                    room_copy_name.Set(str(rm_link_name.upper()))
                # number
                room_copy_number = room_copy.get_Parameter(BuiltInParameter.ROOM_NUMBER)
                rm_link_number = room_link.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                if rm_link_number is None:
                    room_copy_number.Set("")
                room_copy_number.Set(str(rm_link_number))

                print('Copying Room...({})'.format(str(index).zfill(3)))
                print("Room Name:   {}".format(rm_link_name))  # print statement to check rm_link_name
                print("Room Number: {}".format(rm_link_number))  # print statement to check rm_link_number
                print('-' * 50)

        time.sleep(5)

        # CHECK THE CURRENT MODEL AFTER THE CREATION OF TEMPORARY ROOM
        current_level_filter = ElementLevelFilter(active_level.Id)

        rooms_current = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Rooms)\
            .WherePasses(current_level_filter).WhereElementIsNotElementType().ToElements()
        print("=" * 50)
        print("Total Room in link:      {}".format(len(all_rooms_in_link_level)))
        print("Total Room in current:   {}".format(len(rooms_current)))

        # for index, room_cur in enumerate(rooms_current, start=1):
        #     print('ROOM CREATED {}'.format(index))
        #     print('Room Name: {}'.format(room_cur.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()))
        #     print('Room Number: {}'.format(room_cur.Number))
        #     print('=' * 50)

    # ================================================================================================================
        # 🔵 ELEMENT
        room_numbers = []  # extracted from temp rooms
        room_name = None
        no_of_elements = []
        row = 1
        for element in all_elements_in_level:
            #  instance param
            element_id = element.Id
            category_name = element.Category.Name
            family_name = element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
            no_of_elements.append(element)

            #  type param
            el_type_id = element.GetTypeId()
            el_type = doc.GetElement(el_type_id)
            if el_type:
                type_description = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)
                type_image = el_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_IMAGE)

            element_location = element.Location
            if element_location:
                el_loc_point = element_location.Point
                pos_x = el_loc_point.X
                pos_y = el_loc_point.Y
                pos_z = el_loc_point.Z

            # room of elements
            room_active = doc.GetRoomAtPoint(el_loc_point, phase)
            if room_active:
                room_active_name = room_active.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
                room_name = room_active_name  # room name
                room_active_number = room_active.Number  # room number
                room_num_param = element.get_Parameter(BuiltInParameter.ROOM_NUMBER)
                parts_room_number = room_active_number.split('.')
                if len(parts_room_number) == 3:
                    room_num_add = parts_room_number[0] + parts_room_number[1] + parts_room_number[2] + "01"
                    if room_num_add is None:
                        continue
                    room_active_number = room_num_param.Set(room_num_add)

            # 🆗 WRITE TO EXCEL
            worksheet.write('A' + str(row + 1), int(str(element_id)))
            worksheet.write('B' + str(row + 1), category_name)
            worksheet.write('C' + str(row + 1), family_name)
            worksheet.write('D' + str(row + 1), type_description.AsValueString())
            worksheet.write('E' + str(row + 1), type_image.AsValueString().strip())
            worksheet.write('F' + str(row + 1), pos_x)
            worksheet.write('G' + str(row + 1), pos_y)
            worksheet.write('H' + str(row + 1), pos_z)
            worksheet.write('I' + str(row + 1), room_active_number)

            row += 1  # increment row at the end of the loop

        workbook.close()

        if t.GetStatus() == TransactionStatus.Started:
            t.RollBack()
    # ==========================================================================================================
    current_datetime = datetime.now()
    time_stamp = current_datetime.strftime('%d %b %Y %H%Mhrs')
    forms.alert('Excel exported!\nTime Stamp: {}'.format(time_stamp), warn_icon=False, exitscript=False)



