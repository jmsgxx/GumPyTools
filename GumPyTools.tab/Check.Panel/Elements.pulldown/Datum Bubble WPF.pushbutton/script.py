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

class ShowHideBubble(Window):
    def __init__(self, image_path=""):
        # Connect to .xaml File (in the same folder!)
        path_xaml_file = os.path.join(PATH_SCRIPT, 'my_form.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        if image_path:
            self.UI_img.Source = BitmapImage(Uri(image_path))
            self.UI_img.Visibility = Visibility.Visible


        # Show Form
        self.ShowDialog()



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

