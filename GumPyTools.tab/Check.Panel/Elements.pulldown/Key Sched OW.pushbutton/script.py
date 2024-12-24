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

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Application, Window
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem, ComboBox, ComboBoxItem
from System import Uri

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
# Inherit .NET Window for your UI Form Class
# Path to the script folder


class KeySchedOverwrite(Window):
    def __init__(self):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'my_form.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        self.populate_sched_views()

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
        return self.UI_textbox_search.SelectedItem.Tag



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


    # ------------------------------------------------------------
    # ╔═╗╦  ╦╔═╗╔╗╔╔╦╗╔═╗
    # ║╣ ╚╗╔╝║╣ ║║║ ║ ╚═╗
    # ╚═╝ ╚╝ ╚═╝╝╚╝ ╩ ╚═╝
    # ------------------------------------------------------------


    def UIe_select_view(self):
        pass


    # ------------------------------------------------------------
    # ╔╗ ╦ ╦╔╦╗╔╦╗╔═╗╔╗╔╔═╗
    # ╠╩╗║ ║ ║  ║ ║ ║║║║╚═╗
    # ╚═╝╚═╝ ╩  ╩ ╚═╝╝╚╝╚═╝
    # ------------------------------------------------------------

    def UIe_button_run(self, sender, event):
        print("Form submitted!")
        self.Close()


# ------------------------------------------------------------
# ╦═╗╔═╗╦  ╦╦╔╦╗
# ╠╦╝║╣ ╚╗╔╝║ ║
# ╩╚═╚═╝ ╚╝ ╩ ╩
# ------------------------------------------------------------

UI = KeySchedOverwrite()


"""
selected_sched_view = self.sched_view

        view_def = selected_sched_view.Definition
        count = view_def.GetFieldCount()

        params_in_sched = []

        for i in range(count):
            field = view_def.GetField(i)
            param_ele = doc.GetElement(field.ParameterId)
            params_in_sched.append(param_ele)

        params_sched_dict = {}
        for param in params_in_sched:
            param_name = None
            try:
                param_name = param.Name
            except:
                pass
            params_sched_dict[param_name] = param_name

        self.populate_param_combo(self, params_sched_dict)

    def populate_param_combo(self, param_sched_dict):
        self.UI_combo_param.Items.Clear()

        for param_name, param_el in sorted(param_sched_dict.items()):
            combo_param_item = ComboBoxItem()
            combo_param_item.Content = param_name
            combo_param_item.Content = param_el

            self.UI_combo_param.Items.Add(combo_param_item)
"""