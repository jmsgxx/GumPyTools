# -*- coding: utf-8 -*-
__title__ = "my_form"
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
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem
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
class FirstButton(Window):
    def __init__(self):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'my_form.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        # Show Form
        self.ShowDialog()


# Show form to the user
UI = FirstButton()
