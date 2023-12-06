# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *
from pyrevit import forms
from Autodesk.Revit.UI.Selection import ISelectionFilter

import clr
clr.AddReference("System")
from System.Collections.Generic import List

doc      = __revit__.ActiveUIDocument.Document
uidoc    = __revit__.ActiveUIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel


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

