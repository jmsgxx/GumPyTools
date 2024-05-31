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
from Autodesk.Revit.DB.Structure import StructuralType

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

    # =================================================================================================================
    # ╦ ╦╦╔╗╔╔╦╗╔═╗╦ ╦╔═╗
    # ║║║║║║║ ║║║ ║║║║╚═╗
    # ╚╩╝╩╝╚╝═╩╝╚═╝╚╩╝╚═╝WINDOWS
    # =================================================================================================================
    # host_wall = doc.GetElement(ElementId(309833))
    # pt_start    = XYZ(80, 0, 0)
    # pt_end      = XYZ(80, 20, 0)

    # pt_mid = (pt_start + pt_end) / 2
    # window_type = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows)\
    #                                                             .WhereElementIsElementType()\
    #                                                                 .FirstElement()

    """
    public FamilyInstance NewFamilyInstance(
	XYZ location,
	FamilySymbol symbol,
	Element host,
	StructuralType structuralType

    """
    # window = doc.Create.NewFamilyInstance(pt_mid, window_type, host_wall, StructuralType.NonStructural)

    # =================================================================================================================
    # ╔═╗╔═╗╔╦╗╦╦ ╦ ╦  ╦╔╗╔╔═╗╔╦╗╔═╗╔╗╔╔═╗╔═╗
    # ╠╣ ╠═╣║║║║║ ╚╦╝  ║║║║╚═╗ ║ ╠═╣║║║║  ║╣ 
    # ╚  ╩ ╩╩ ╩╩╩═╝╩   ╩╝╚╝╚═╝ ╩ ╩ ╩╝╚╝╚═╝╚═╝
    # =================================================================================================================
    """
    public FamilyInstance NewFamilyInstance(
	XYZ location,
	FamilySymbol symbol,
	StructuralType structuralType


    """
    # def get_type_by_name(type_name):
    #     """Extra Function to get Family Type by name."""
    #     # CREATE RULE
    #     param_type = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
    #     f_param    = ParameterValueProvider(param_type)
    #     evaluator  = FilterStringEquals()
    #     f_rule     = FilterStringRule(f_param, evaluator, type_name, True) # Revit 2023 does not need last argument!
    
    #     # CREATE FILTER
    #     filter_type_name = ElementParameterFilter(f_rule)
    
    #     # GET ELEMENTS
    #     return FilteredElementCollector(doc).WherePasses(filter_type_name).WhereElementIsElementType().FirstElement()

    # pt    = XYZ(100, 20, 0)
    # symbol = get_type_by_name("Placeholder B")

    # doc.Create.NewFamilyInstance(pt, symbol, StructuralType.NonStructural)

    # ================================================================================================================
    # ╔═╗╦ ╦╔═╗╔═╗╔╦╗╔═╗
    # ╚═╗╠═╣║╣ ║╣  ║ ╚═╗
    # ╚═╝╩ ╩╚═╝╚═╝ ╩ ╚═╝#sheets
    # =================================================================================================================
    """"
    public static ViewSheet Create(
	Document document,
	ElementId titleBlockTypeId
    """
    tblock_id = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks) \
                                             .WhereElementIsElementType().FirstElementId()
    
    new_sheet = ViewSheet.Create(doc, tblock_id)
    new_sheet.SheetNumber   = "Random Number"
    new_sheet.Name          = "Random Name"

    # =================================================================================================================
    # ╦  ╦╦╔═╗╦ ╦╔═╗
    # ╚╗╔╝║║╣ ║║║╚═╗
    #  ╚╝ ╩╚═╝╚╩╝╚═╝#views
    # =================================================================================================================

    """
    public static View3D CreateIsometric(
	Document document,
	ElementId viewFamilyTypeId
    """
    # all_view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

    # view_type = [vt for vt in all_view_types if vt.ViewFamily == ViewFamily.ThreeDimensional][0]
    # print(view_type)

    # view_3d = View3D.CreateIsometric(doc, view_type.Id)

    # =================================================================================================================
    # ╦═╗╔═╗╔═╗╦╔═╗╔╗╔
    # ╠╦╝║╣ ║ ╦║║ ║║║║
    # ╩╚═╚═╝╚═╝╩╚═╝╝╚╝#region
    # =================================================================================================================
    """"
    public static FilledRegion Create(
	Document document,
	ElementId typeId,
	ElementId viewId,
	IList<CurveLoop> boundaries
    """
    # type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.FilledRegionType)
    
    # #GET POINTS
    # pt_0 = XYZ(120, 0, 0)
    # pt_1 = XYZ(140, 0, 0)
    # pt_2 = XYZ(140, 20, 0)
    # pt_3 = XYZ(120, 20, 0)
	
    # CONVERT POINTS INTO LINES
    l_0 = Line.CreateBound(pt_0, pt_1)
    l_1 = Line.CreateBound(pt_1, pt_2)
    l_2 = Line.CreateBound(pt_2, pt_3)
    l_3 = Line.CreateBound(pt_3, pt_0)

    # GROUP THE LINES AS BOUNDARIES
    boundary = CurveLoop()
    boundary.Append(l_0)
    boundary.Append(l_1)
    boundary.Append(l_2)
    boundary.Append(l_3)

    # LIST OF BOUNDARIES
    list_boundaries = List[CurveLoop]()
    list_boundaries.Add(boundary)

    filled_region = FilledRegion.Create(doc, type_id, active_view.Id, list_boundaries)


    # =================================================================================================================
    # ╔═╗╦  ╔═╗╔═╗╦═╗
    # ╠╣ ║  ║ ║║ ║╠╦╝
    # ╚  ╩═╝╚═╝╚═╝╩╚═#floor
    # =================================================================================================================
    """Floor.Create"""

    """
    Floor Create(
	Document document,
	IList<CurveLoop> profile,
	ElementId floorTypeId,
	ElementId levelId
    """
    floor_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.FloorType)

    #GET POINTS
    pt_0 = XYZ(150, 0, 0)
    pt_1 = XYZ(170, 0, 0)
    pt_2 = XYZ(170, 20, 0)
    pt_3 = XYZ(150, 20, 0)
	
    # CONVERT POINTS INTO LINES
    l_0 = Line.CreateBound(pt_0, pt_1)
    l_1 = Line.CreateBound(pt_1, pt_2)
    l_2 = Line.CreateBound(pt_2, pt_3)
    l_3 = Line.CreateBound(pt_3, pt_0)

    # GROUP THE LINES AS BOUNDARIES
    boundary = CurveLoop()
    boundary.Append(l_0)
    boundary.Append(l_1)
    boundary.Append(l_2)
    boundary.Append(l_3)

     # LIST OF BOUNDARIES
    new_boundary = List[CurveLoop]()
    new_boundary.Add(boundary)
    

    new_floor = Floor.Create(doc, new_boundary, floor_type_id, active_level.Id)

    # =================================================================================================================
    # ╔═╗╔═╗╔═╗╦ ╦  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
    # ║  ║ ║╠═╝╚╦╝  ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
    # ╚═╝╚═╝╩   ╩   ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝#copy
    # GET ALL FLOORS IN VIEW
    # =================================================================================================================


    """
    ICollection<ElementId> CopyElement(
	Document document,
	ElementId elementToCopy,
	XYZ translation
    """
    
    # all_floors_in_view = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Floors) \
    #                                                       .WhereElementIsNotElementType().ToElementIds()
    # elements_to_copy = List[ElementId](all_floors_in_view)

    # for i in range(1,6):
    #     vector = XYZ(20*i, 20*i, 0)
    #     ElementTransformUtils.CopyElements(doc, elements_to_copy, vector)


    # =================================================================================================================
    # ╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗  ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗
    #  ║║║╣ ║  ║╣  ║ ║╣   ║╣ ║  ║╣ ║║║║╣ ║║║ ║ ╚═╗
    # ═╩╝╚═╝╩═╝╚═╝ ╩ ╚═╝  ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝#delete elements
    # ==================================================================================================================

    """
    public ICollection<ElementId> Delete(
	ICollection<ElementId> elementIds
    """

    all_floors_in_view = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Floors) \
                                .WhereElementIsNotElementType().ToElementIds()
    elements_to_delete = List[ElementId](all_floors_in_view)

    doc.Delete(elements_to_delete)
    t.Commit()  