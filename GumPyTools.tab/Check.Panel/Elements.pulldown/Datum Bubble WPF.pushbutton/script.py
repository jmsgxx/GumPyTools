# -*- coding: utf-8 -*-
__title__ = "Datum Grid WPF"
__doc__ = """
Description:
This is the base for building your WPF forms.
It includes a very simple XAML file and the Python code 
to display your form and react to the submit button.

________________________________________________________________
Last Updates:
- "" ""
________________________________________________________________
Author: JOVEN MARK GUMANA
Version: v1
"""

import pyrevit.revit
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms  # By importing forms you also get references to WPF package! IT'S Very IMPORTANT !!!
import wpf, os, clr  # wpf can be imported only after pyrevit.forms!
from Snippets._context_manager import try_except, rvt_transaction
from Snippets._x_selection import ISelectionFilter_Classes, get_multiple_elements
from Autodesk.Revit.UI.Selection import Selection, ObjectType


# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System.Windows import Application, Window, Visibility
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem, ComboBox, ComboBoxItem, TextBlock
from System import Uri
from System.Windows.Media.Imaging import BitmapImage

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
doc = __revit__.ActiveUIDocument.Document  #type: Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
selection = uidoc.Selection  # type: Selection


# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
# ====================================================================================================

class ShowHideBubble(Window):
    def __init__(self, image_path=""):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'my_form.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        self.selected_datum = self.collected_datum()
        self.populate_listbox()

        if image_path:
            self.UI_img.Source = BitmapImage(Uri(image_path))
            self.UI_img.Visibility = Visibility.Visible


        # Show Form
        self.ShowDialog()

    # ╔═╗╦═╗╔═╗╔═╗╔═╗╦═╗╔╦╗╦╔═╗╔═╗
    # ╠═╝╠╦╝║ ║╠═╝║╣ ╠╦╝ ║ ║║╣ ╚═╗
    # ╩  ╩╚═╚═╝╩  ╚═╝╩╚═ ╩ ╩╚═╝╚═╝
    # ---------------------------------------------------------

    @property
    def start_bub(self):
        return self.UI_radio_start.IsChecked

    @property
    def end_bub(self):
        return self.UI_radio_end.IsChecked

    @property
    def start_end_show(self):
        return self.UI_radio_show_both.IsChecked

    @property
    def start_end_hide(self):
        return self.UI_radio_hide_both.IsChecked

    @property
    def apply_view(self):
        return self.UI_apply_view.IsChecked

    @property
    def search_txt(self):
        return self.UI_search.Text

    @property
    def extent_max_grid(self):
        return self.UI_max_extents.IsChecked

    @property
    def selected_listbox_items(self):
        selected_views = []
        for listbox_item in self.UI_listbox.Items:
            checkbox = listbox_item.Content
            if checkbox.IsChecked:
                selected_views.append(checkbox.Tag)

        return selected_views



    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝
    # ---------------------------------------------------------


    def start_bub_show(self, element):
        with rvt_transaction(doc, __title__):
            element.ShowBubbleInView(DatumEnds.End0, active_view)


    def start_bub_hide(self, element):
        with rvt_transaction(doc, __title__):
            element.HideBubbleInView(DatumEnds.End0, active_view)

    def end_bub_show(self, element):
        with rvt_transaction(doc, __title__):
            element.ShowBubbleInView(DatumEnds.End1, active_view)


    def end_bub_hide(self, element):
        with rvt_transaction(doc, __title__):
            element.HideBubbleInView(DatumEnds.End1, active_view)

    # --------------------------
    # 🟠 collect the grids
    def collected_datum(self):
        """
        select the grids first.
        @return: Grids Datum
        """
        selected_datum = get_multiple_elements()

        if not selected_datum:
            with try_except():
                filter_type = ISelectionFilter_Classes([Grid, Level])
                datum_list = selection.PickObjects(ObjectType.Element, filter_type, "Select Datum")
                selected_datum = [doc.GetElement(gr) for gr in datum_list]

            if not selected_datum:
                forms.alert('No datum selected', exitscript=True)

        return selected_datum
    # --------------------------

    def populate_listbox(self):

        if not self.apply_view:
            for listbox in self.UI_listbox.Items:
                listbox.Visibility = Visibility.Collapsed

        else:
            all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

            plan_view = List[ViewType]([ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.AreaPlan])
            elev_sec_view = List[ViewType]([ViewType.Elevation, ViewType.Section])

            dict_views = {}

            # 🟩 if plans
            if active_view.ViewType in [view for view in plan_view]:
                for view in all_views:
                    if view.Id == active_view.Id:
                        continue
                    elif view.ViewType == active_view.ViewType:
                        dict_views["{}: {}".format(view.ViewType, view.Name)] = view

            elif active_view.ViewType in [view for view in elev_sec_view]:
                for view in all_views:
                    if view.Id == active_view.Id:
                        continue
                    elif view.ViewType == active_view.ViewType and \
                            view.ViewDirection.Negate().IsAlmostEqualTo(active_view.ViewDirection):
                        dict_views["{}: {}".format(view.ViewType, view.Name)] = view

            self.UI_listbox.Items.Clear()
            sorted_dict_views = sorted(dict_views.items())

            for view_name, view in sorted_dict_views:
                textblock = TextBlock()
                textblock.Text = view_name

                checkbox = CheckBox()
                checkbox.Content = textblock
                checkbox.Tag = view

                listbox_item = ListBoxItem()
                listbox_item.Content = checkbox

                self.UI_listbox.Items.Add(listbox_item)

    # --------------------------
    def listbox_select_all(self, toggle):

        for listbox_item in self.UI_listbox.Items:
            if listbox_item.Visibility == Visibility.Visible:
                checkbox = listbox_item.Content
                checkbox.IsChecked = toggle
    # --------------------------

    def get_selected_items(self):
        selected_items = []
        for listbox_item in self.UI_listbox.Items:
            checkbox = listbox_item.Content
            if checkbox.IsChecked:
                selected_items.append(checkbox.Tag)

        return selected_items
    # --------------------------

    def max_extents(self):
        with rvt_transaction(doc, __title__):
            collected_datum = self.selected_datum
            for datum in collected_datum:
                if self.extent_max_grid:
                    datum.Maximize3DExtents()

    # ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝
    # ---------------------------------------------------------


    def UIe_apply_check(self, sender, event):
        self.populate_listbox()

    def UIe_apply_uncheck(self, sender, event):
        self.populate_listbox()

    def UIe_max_3d_check(self, sender, event):
        self.max_extents()

    def UIe_max_3d_uncheck(self, sender, event):
        self.max_extents()

    def UIe_search_text(self, sender, e):
        search_text = self.search_txt.lower().strip()

        if search_text:
            search_words = search_text.split()

            for listbox_item in self.UI_listbox.Items:
                checkbox  = listbox_item.Content
                textblock = checkbox.Content
                view_name = textblock.Text.lower()

                if all(word in view_name for word in search_words):
                    listbox_item.Visibility = Visibility.Visible
                else:
                    listbox_item.Visibility = Visibility.Collapsed

        if not search_text:
            for listbox_item in self.UI_listbox.Items:
                listbox_item.Visibility = Visibility.Visible



    def UIe_button_apply(self, sender, event):
        try:
            for datum in self.selected_datum:
                if self.start_bub:

                    self.start_bub_show(datum)
                    self.end_bub_hide(datum)

                elif self.end_bub:

                    self.start_bub_hide(datum)
                    self.end_bub_show(datum)

                elif self.start_end_show:

                    self.start_bub_show(datum)
                    self.end_bub_show(datum)

                elif self.start_end_hide:

                    self.start_bub_hide(datum)
                    self.end_bub_hide(datum)

        except Exception as e:
            forms.alert("Error: {}".format(str(e)))

    def UIe_btn_select_all(self, sender, e):
        self.listbox_select_all(True)

    def UIe_btn_select_none(self, sender, e):
        self.listbox_select_all(False)

    def UIe_button_run(self, sender, event):
        with rvt_transaction(doc, __title__):
            try:
                selected_items = self.get_selected_items()
                collected_datum = self.selected_datum

                if selected_items:
                    i_set_view = HashSet[ElementId]()
                    for view in selected_items:
                        i_set_view.Add(view.Id)

                    for datum in collected_datum:
                        datum.PropagateToViews(active_view, i_set_view)

            except:
                pass

        self.Close()


# ------------------------------------------------------------
# ╦═╗╔═╗╦  ╦╦╔╦╗
# ╠╦╝║╣ ╚╗╔╝║ ║
# ╩╚═╚═╝ ╚╝ ╩ ╩
# ------------------------------------------------------------

img_name = "gumpy.png"
img_path = os.path.join(PATH_SCRIPT, img_name)

UI = ShowHideBubble(image_path=img_path)

