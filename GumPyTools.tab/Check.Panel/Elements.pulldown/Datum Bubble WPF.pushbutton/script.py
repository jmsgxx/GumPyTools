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
from Snippets._context_manager import try_except
from Snippets._x_selection import ISelectionFilter_Classes, get_multiple_elements
from Autodesk.Revit.UI.Selection import Selection, ObjectType
import logging




# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List, HashSet
from System.Windows import Application, Window, Visibility
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem, ComboBox, ComboBoxItem
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

logging.basicConfig(level=logging.DEBUG)


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

        if image_path:
            self.UI_img.Source = BitmapImage(Uri(image_path))
            self.UI_img.Visibility = Visibility.Visible


        # Show Form
        self.Show()

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


    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝
    # ---------------------------------------------------------


    def start_bub_show(self, element):
        print("start_bub_show called with element: {}".format(element))
        element.ShowBubbleInView(DatumEnds.End0, active_view)

    def start_bub_hide(self, element):
        print("start_bub_hide called with element: {}".format(element))
        element.HideBubbleInView(DatumEnds.End0, active_view)

    def end_bub_show(self, element):
        print("end_bub_show called with element: {}".format(element))
        element.ShowBubbleInView(DatumEnds.End1, active_view)

    def end_bub_hide(self, element):
        print("end_bub_hide called with element: {}".format(element))
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


    # ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝
    # ---------------------------------------------------------


    def UIe_button_apply(self, sender, event):
        print("apply button start")
        print("selected_datum: {}".format(self.selected_datum))
        print("start_bub: {}, end_bub: {}, start_end_show: {}, start_end_hide: {}".format(
            self.start_bub, self.end_bub, self.start_end_show, self.start_end_hide))

        try:
            print("Inside transaction")
            for datum in self.selected_datum:
                if self.start_bub:
                    print("start_bub is checked")
                    self.start_bub_show(datum)
                    self.end_bub_hide(datum)

                elif self.end_bub:
                    print("end_bub is checked")
                    self.start_bub_hide(datum)
                    self.end_bub_show(datum)

                elif self.start_end_show:
                    print("start_end_show is checked")
                    self.start_bub_show(datum)
                    self.end_bub_show(datum)

                elif self.start_end_hide:
                    print("start_end_hide is checked")
                    self.start_bub_hide(datum)
                    self.end_bub_hide(datum)

        except Exception as e:
            print("Error: {}".format(e))

    def UIe_button_run(self, sender, event):

        self.Close()


# ------------------------------------------------------------
# ╦═╗╔═╗╦  ╦╦╔╦╗
# ╠╦╝║╣ ╚╗╔╝║ ║
# ╩╚═╚═╝ ╚╝ ╩ ╩
# ------------------------------------------------------------

img_name = "gumpy.png"
img_path = os.path.join(PATH_SCRIPT, img_name)

UI = ShowHideBubble(image_path=img_path)

