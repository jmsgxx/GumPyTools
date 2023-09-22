# -*- coding: utf-8 -*-

__title__ = 'Create/Delete/Copy Elements'
__doc__ = """
This script will create, delete and copy elements.
__________________________________
Author: Joven Mark Gumana
20230922
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *

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



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
with Transaction(doc, __title__) as t:
    t.Start()
    # CHANGE HERE
    # =========================================================================================================
    # ╔╦╗╔═╗═╗ ╦╔╦╗
    #  ║ ║╣ ╔╩╦╝ ║ 
    #  ╩ ╚═╝╩ ╚═ ╩ #text
    # =========================================================================================================
    """
    Text Note CLass
    public static TextNote Create(
        Document document,
        ElementId viewId,
        XYZ position,
        string text,
        ElementId typeId
    )
    """
    # text_type_id = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
    # pt = XYZ(0,0,0)
    # text = 'This is your first create method in Revit API.'

    # TextNote.Create(doc, active_view.Id, pt, text, text_type_id)
    # ============================================================================================================
    # ╦═╗╔═╗╔═╗╔╦╗
    # ╠╦╝║ ║║ ║║║║
    # ╩╚═╚═╝╚═╝╩ ╩#room
    # ============================================================================================================
    # pt = UV(40, 0)
    # room = doc.Create.NewRoom(active_level, pt)

    # ===========================================================================================================
    # ╦═╗╔═╗╔═╗╔╦╗  ╔╦╗╔═╗╔═╗
    # ╠╦╝║ ║║ ║║║║   ║ ╠═╣║ ╦
    # ╩╚═╚═╝╚═╝╩ ╩   ╩ ╩ ╩╚═╝
    # ===========================================================================================================
    """
    public RoomTag NewRoomTag(
	LinkElementId roomId,
	UV point,
	ElementId viewId
    """
    # room_id = LinkElementId(room.Id)
    # doc.Create.NewRoomTag(room_id, pt, active_view.Id)
    # ============================================================================================================
    # ╦  ╦╔╗╔╔═╗╔═╗
    # ║  ║║║║║╣ ╚═╗
    # ╩═╝╩╝╚╝╚═╝╚═╝ detail lines
    # ============================================================================================================
    """
    public DetailCurve NewDetailCurve(
	View view,
	Curve geometryCurve
    )
    """
    # pt_start    = XYZ(60, 0, 0)
    # pt_end      = XYZ(60, 20, 0)
    # curve       = Line.CreateBound(pt_start, pt_end)

    # detail_line = doc.Create.NewDetailCurve(active_view, curve)


    # ================================================================================================================
    # ╦ ╦╔═╗╦  ╦  ╔═╗
    # ║║║╠═╣║  ║  ╚═╗
    # ╚╩╝╩ ╩╩═╝╩═╝╚═╝walls
    # ================================================================================================================
    """
    public static Wall Create(
	Document document,
	Curve curve,
	ElementId levelId,
	bool structural

    """
    # pt_start    = XYZ(80, 0, 0)
    # pt_end      = XYZ(80, 20, 0)
    # curve       = Line.CreateBound(pt_start, pt_end)

    # Wall.Create(doc, curve, active_level.Id, False)

    # ======================================================================================================================
    # ╦ ╦╦╔╗╔╔╦╗╔═╗╦ ╦╔═╗
    # ║║║║║║║ ║║║ ║║║║╚═╗
    # ╚╩╝╩╝╚╝═╩╝╚═╝╚╩╝╚═╝WINDOWS
    # ======================================================================================================================





# ╔═╗╦ ╦╔═╗╔═╗╔╦╗╔═╗
# ╚═╗╠═╣║╣ ║╣  ║ ╚═╗
# ╚═╝╩ ╩╚═╝╚═╝ ╩ ╚═╝#sheets



# ╦  ╦╦╔═╗╦ ╦╔═╗
# ╚╗╔╝║║╣ ║║║╚═╗
#  ╚╝ ╩╚═╝╚╩╝╚═╝#views




# ╦═╗╔═╗╔═╗╦╔═╗╔╗╔
# ╠╦╝║╣ ║ ╦║║ ║║║║
# ╩╚═╚═╝╚═╝╩╚═╝╝╚╝#region



# ╔═╗╦  ╔═╗╔═╗╦═╗
# ╠╣ ║  ║ ║║ ║╠╦╝
# ╚  ╩═╝╚═╝╚═╝╩╚═#floor




# ╔═╗╔═╗╔═╗╦ ╦  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
# ║  ║ ║╠═╝╚╦╝  ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
# ╚═╝╚═╝╩   ╩   ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝#copy




# ╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
#  ║║║╣ ║  ║╣  ║ ║╣   ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
# ═╩╝╚═╝╩═╝╚═╝ ╩ ╚═╝  ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝#delete elements


    t.Commit()