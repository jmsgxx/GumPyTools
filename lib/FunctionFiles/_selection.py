# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ISelectionFilter, ObjectType
from pyrevit import forms
from Snippets._context_manager import try_except

import clr
clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System import Enum


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection
# =================================================================
# ╔═╗╦  ╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝


class SelectElementBIGClass(ISelectionFilter):
    def __init__(self, big_enum):
        """
        select any element provided by any built in category enum
        elem.Category.Id == ElementId(BuiltInCategory.OST_SpecialityEquipment)
        """
        self.big_enum = big_enum

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(self.big_enum):
            return True



class FECollectorCat:
    def __init__(self, big_enum, selected_view_id="", by_instance=True):
        """
        @param big_enum:
        @param selected_view_id: view_id
        @param by_instance:
        """
        self.big_enum = big_enum
        self.selected_view_id = selected_view_id
        self.by_instance = by_instance

    def get_elements(self):
        if self.selected_view_id:
            fec = FilteredElementCollector(doc, self.selected_view_id)
        else:
            fec = FilteredElementCollector(doc)

        if self.by_instance:
            elements = fec.OfCategory(self.big_enum).WhereElementIsNotElementType().ToElements()
        else:
            elements = fec.OfCategory(self.big_enum).WhereElementIsElementType().ToElements()

        return elements

# =================================================================
# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝


def highlight_selected_elements(element_id_lst):
    """
    Will highlight the selected elements
    @param element_id_lst: element id list
    @return: selected elements
    """
    return selection.SetElementIds(List[ElementId](element_id_lst))


def get_multiple_elements():
    """get elements in selected items"""
    return [doc.GetElement(el_id) for el_id in selection.GetElementIds()]


def selection_filter(filter_type, selected_els):
    """
    @param filter_type: Iselection filter
    @param selected_els: elements to check
    @return:
    """

    if not selected_els:
        with try_except():
            el_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Wall")
            selected_els = [doc.GetElement(el) for el in el_list]

        if not selected_els:
            forms.alert('No element selected', exitscript=True)

    return selected_els
