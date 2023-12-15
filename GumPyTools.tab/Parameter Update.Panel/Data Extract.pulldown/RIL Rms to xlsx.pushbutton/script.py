# -*- coding: utf-8 -*-

__title__ = 'RIL Rms to xlsx'
__doc__ = """
This script will export out the list
of rooms that needs to have an RIL.
e.g. "DEPARTMENTAL - BLP" and
"REPEATABLE - BLP" under the parameter
'Room_Classification_BLP'.

HOW TO:
1. Click the command.
2. Choose an option to export.
3. Prompt will pop up if exportation was 
successful or not.
__________________________________
v1. 15 Dec 2023
Author: Joven Mark Gumana
"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
import xlsxwriter
from pyrevit import forms
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application


active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel
current_view    = [active_view.Id]

ask_user = forms.ask_for_one_item(
    ['Yes', 'No'],
    prompt='Export out room info for RIL?',
    title='Export room data'
)

if ask_user == 'No' or ask_user is None:
    forms.alert("Alright. Try again later.", exitscript=True)
else:
    try:

        file_path = forms.save_excel_file(title='Select destination file')
        if file_path:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()
            headings = ['Room Element Id', 'Room Name', 'Room Number', 'Room SoA']
            for i, heading in enumerate(headings):
                worksheet.write(0, i, heading)
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 85)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 15)

            level_filter = active_level.Id

            rooms = FilteredElementCollector(doc)\
                .OfCategory(BuiltInCategory.OST_Rooms)\
                .WherePasses(ElementLevelFilter(level_filter))\
                .ToElements()

            collected_rooms = []

            for room in rooms:
                room_class = room.LookupParameter('Rooms_Classification_BLP').AsString()
                if room_class == 'DEPARTMENTAL - BLP' or room_class == 'REPEATABLE - BLP':
                    room_el_id = room.Id
                    room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                    room_number = room.Number
                    room_soa = room.LookupParameter('Room SoA Ref Number').AsString()
                    collected_rooms.append((room_el_id, room_name, room_number, room_soa))

            row = 1
            for room_el_id, room_name, room_number, room_soa in sorted(collected_rooms, key=lambda x: x[2]):
                worksheet.write(row, 0, str(room_el_id))
                worksheet.write(row, 1, room_name)
                worksheet.write(row, 2, room_number)
                worksheet.write(row, 3, room_soa)
                row += 1

            forms.alert("Export successful", warn_icon=False, exitscript=False)

        else:
            forms.alert("No Input", exitscript=True)

    except Exception as e:
        forms.alert("{}".format(e))


