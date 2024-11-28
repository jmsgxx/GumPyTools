# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import Selection, ObjectType
from pyrevit import forms
from Autodesk.Revit.UI.Selection import ISelectionFilter
from pyrevit import script

import clr
clr.AddReference("System")
from System.Collections.Generic import List

doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel

selection = uidoc.Selection     # type: Selection


def get_multiple_elements():
    """get elements in selected items"""
    return [doc.GetElement(el_id) for el_id in selection.GetElementIds()]


class ISelectionFilter_Classes(ISelectionFilter):
    def __init__(self, allowed_types):
        """ ISelectionFilter made to filter with types
        :param allowed_types: list of allowed Types"""
        self.allowed_types = allowed_types

    def AllowElement(self, element):
        if type(element) in self.allowed_types:
            return True


class ISelectionFilter_Categories(ISelectionFilter):
    def __init__(self, allowed_categories):
        """ ISelectionFilter made to filter with categories
        :param allowed_categories: list of allowed Categories"""
        self.allowed_categories = allowed_categories

    def AllowElement(self, element):
        if element.Category.BuiltInCategory in self.allowed_categories:
            return True


class WallSelectionFilterSTR(ISelectionFilter):
    def __init__(self, allowed_types, search_string):
        """ ISelectionFilter made to filter with types
        will select wall name with search string
        :param allowed_types: list of allowed Types"""
        self.allowed_types = allowed_types
        self.search_string = search_string

    def AllowElement(self, element):
        if type(element) in self.allowed_types:
            type_param = element.Name
            if self.search_string in type_param:
                return True


class ISelectionFilterCatName(ISelectionFilter):
    def __init__(self, allowed_categories):
        """ ISelectionFilter made to filter with categories' name
        :param allowed_categories: list of allowed Categories Name"""
        self.allowed_categories = allowed_categories

    def AllowElement(self, element):
        if element.Category.Name in self.allowed_categories:
            return True


class DoorCustomFilter(ISelectionFilter):
    def __init__(self):
        """
        ISelection Door Custom Filter
        """

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(BuiltInCategory.OST_Doors):
            return True


class CurtainPanelFilter(ISelectionFilter):
    def __init__(self):
        """
        ISelection Curtain Panels
        """

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(BuiltInCategory.OST_CurtainWallPanels):
            return True


class CurvesFilter(ISelectionFilter):
    def __init__(self):
        """
        ISelection Curtain Panels. Will select both model line and detail lines.
        """

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(BuiltInCategory.OST_Lines):
            return True


class StairsFilter(ISelectionFilter):
    def __init__(self):
        """
        ISelection Stairs.
        """

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(BuiltInCategory.OST_Stairs):
            return True


class ParkingFilter(ISelectionFilter):
    def __init__(self):
        """
        ISelection Parking Filter
        """

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(BuiltInCategory.OST_Parking):
            return True


class RailingFilter(ISelectionFilter):
    def __init__(self):
        """
        ISelection Railing Filter
        """

    def AllowElement(self, elem):
        if elem.Category.Id == ElementId(BuiltInCategory.OST_Railings):
            return True


def get_param_of_element():
    """
    select elements and print the available parameters
    """

    def get_param_value(param):
        """Get a value from a Parameter based on its StorageType."""
        value = None
        if param.StorageType == StorageType.Double:
            value = param.AsDouble()
        elif param.StorageType == StorageType.ElementId:
            value = param.AsElementId()
        elif param.StorageType == StorageType.Integer:
            value = param.AsInteger()
        elif param.StorageType == StorageType.String:
            value = param.AsString()
        return value

    output = script.get_output()
    output.center()

    try:
        selected_element = get_multiple_elements()
        if not selected_element:
            element_list = selection.PickObjects(ObjectType.Element)
            selected_element = [doc.GetElement(el) for el in element_list]
    except Exception as e:
        forms.alert(str(e))

    for i in selected_element:
        params = i.Parameters  # get just one item
        for p in sorted(params, key=lambda x: x.Definition.Name):  # loop thorough the parameters to get their name
            print("Name: {}".format(p.Definition.Name))
            print("ParameterGroup: {}".format(p.Definition.ParameterGroup))
            print("BuiltInParameter: {}".format(p.Definition.BuiltInParameter))
            print("IsReadOnly: {}".format(p.IsReadOnly))
            print("HasValue: {}".format(p.HasValue))
            print("IsShared: {}".format(p.IsShared))
            print("StorageType: {}".format(p.StorageType))
            print("Value: {}".format(get_param_value(p)))
            print("AsValueString(): {}".format(p.AsValueString()))
            print('-' * 100)