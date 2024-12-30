# -*- coding: utf-8 -*-
__title__ = "Key Schedule OW"
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

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms  # By importing forms you also get references to WPF package! IT'S Very IMPORTANT !!!
import wpf, os, clr  # wpf can be imported only after pyrevit.forms!
from Snippets._context_manager import rvt_transaction

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
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


# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
# ====================================================================================================

class KeySchedOverwrite(Window):
    def __init__(self, image_path=""):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'my_form.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        self.populate_sched_views()
        self.collect_params_in_rm()

        if image_path:
            self.UI_img.Source = BitmapImage(Uri(image_path))
            self.UI_img.Visibility = Visibility.Visible


        # Show Form
        self.ShowDialog()

    # ------------------------------------------------------------
    # ╔═╗╦═╗╔═╗╔═╗╔═╗╦═╗╔╦╗╦╔═╗╔═╗
    # ╠═╝╠╦╝║ ║╠═╝║╣ ╠╦╝ ║ ║║╣ ╚═╗
    # ╩  ╩╚═╚═╝╩  ╚═╝╩╚═ ╩ ╩╚═╝╚═╝
    # ------------------------------------------------------------

    @property
    def select_view(self):
        return self.UI_combo_view.SelectedItem.Tag

    @property
    def select_param(self):
        return self.UI_combo_param.SelectedItem.Tag

    @property
    def search_input(self):
        return self.UI_textbox_search.Text



    # ------------------------------------------------------------
    # ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔═╗
    # ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗
    # ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝
    # ------------------------------------------------------------



    def populate_sched_views(self):
        all_sched_views = FilteredElementCollector(doc).OfClass(ViewSchedule).WhereElementIsNotElementType()
        all_sched_dict = {view.Name: view for view in all_sched_views if view.Definition.IsKeySchedule}

        self.UI_combo_view.Items.Clear()    # connected @property

        first_item = True

        for view_name, view_el in all_sched_dict.items():
            all_views_combo = ComboBoxItem()
            all_views_combo.Content = view_name
            all_views_combo.Tag = view_el

            if first_item:
                all_views_combo.IsSelected = True
                first_item = False

            self.UI_combo_view.Items.Add(all_views_combo)

    def collect_params_in_rm(self):
        """
        1. get the parameters of room
        2. get the parameters of view schedule
        3. compare the two sets/list and only get the common parameter to show
        """
        # --------------------------------------------------------------------
        # 🔴 get all the parameters in rooms
        all_rooms = FilteredElementCollector(doc).OfCategory(
            BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

        picked_rm = None    # get only one room
        for rm in all_rooms:
            if rm.Location:
                picked_rm = rm
                break

        param_set = picked_rm.Parameters

        param_set_dict = {}


        for param in param_set:
            if param.IsShared:
                param_set_dict[param.Definition.Name] = param.Definition.Name

            else:
                param_set_dict[param.Definition.Name] = param.Definition.BuiltInParameter

        # --------------------------------------------------------------------
        # 🟠 get the parameters on the schedule view

        selected_view = self.select_view
        key_values = FilteredElementCollector(doc, selected_view.Id).WhereElementIsNotElementType()

        params_in_sched_dict = {}

        for param in key_values:
            for rm_param_key, rm_param_val in param_set_dict.items():
                try:
                    el_param = param.LookupParameter(rm_param_key)
                    if not el_param:
                        built_in_param = getattr(BuiltInParameter, rm_param_key, None)  # get the enum of bip
                        if built_in_param:
                            el_param = param.get_Parameter(built_in_param)
                    if el_param:
                        params_in_sched_dict[rm_param_key] = rm_param_val
                except:
                    pass

        self.UI_combo_param.Items.Clear()

        sorted_param_sched_tup = sorted(params_in_sched_dict.items())

        for param_key, param_value in sorted_param_sched_tup:

            combo_param_str = ComboBoxItem()
            combo_param_str.Content = param_key
            combo_param_str.Tag = str(param_value)

            self.UI_combo_param.Items.Add(combo_param_str)

        if self.UI_combo_param.Items.Count > 0:
            self.UI_combo_param.SelectedIndex = 0

    # ------------------------------------------------------------
    # ╔╗ ╦ ╦╔╦╗╔╦╗╔═╗╔╗╔╔═╗
    # ╠╩╗║ ║ ║  ║ ║ ║║║║╚═╗
    # ╚═╝╚═╝ ╩  ╩ ╚═╝╝╚╝╚═╝
    # ------------------------------------------------------------

    def UIe_button_run(self, sender, event):
        with rvt_transaction(doc, __title__):
            selected_view = self.select_view
            param_get = self.select_param
            input_search = self.search_input

            key_values = FilteredElementCollector(doc, selected_view.Id).WhereElementIsNotElementType()

            for param in key_values:
                try:
                    el_param = param.LookupParameter(param_get)
                    if not el_param:
                        built_in_param = getattr(BuiltInParameter, param_get, None)  # get the enum of bip
                        if built_in_param:
                            el_param = param.get_Parameter(built_in_param)
                    if el_param and el_param.HasValue:
                        try:
                            value = None
                            if el_param.StorageType == StorageType.Double:
                                value = float(input_search)
                            elif el_param.StorageType == StorageType.ElementId:
                                value = ElementId(int(input_search))
                            elif el_param.StorageType == StorageType.Integer:
                                value = int(input_search)
                            elif el_param.StorageType == StorageType.String:
                                value = str(input_search)
                            el_param.Set(value)
                        except:
                            pass
                except Exception as e:
                    forms.alert(str(e))
                    break

        self.Close()


# ------------------------------------------------------------
# ╦═╗╔═╗╦  ╦╦╔╦╗
# ╠╦╝║╣ ╚╗╔╝║ ║
# ╩╚═╚═╝ ╚╝ ╩ ╩
# ------------------------------------------------------------

img_name = "gumpy.png"
img_path = os.path.join(PATH_SCRIPT, img_name)

UI = KeySchedOverwrite(image_path=img_path)

