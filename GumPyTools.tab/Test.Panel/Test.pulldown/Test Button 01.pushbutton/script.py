# -*- coding: utf-8 -*-

__title__ = 'Test Button 01'
__doc__ = """
This script will collect elements.
__________________________________
Author: Joven Mark Gumana
"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ===================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from Snippets._context_manager import rvt_transaction, try_except
import os
import os.path as op
from datetime import datetime
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
doc      = __revit__.ActiveUIDocument.Document  # type: Document
uidoc    = __revit__.ActiveUIDocument   # type: UIDocument
app      = __revit__.Application

active_view     = doc.ActiveView
active_level    = doc.ActiveView.GenLevel


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
def _logger(script_name):
    # get date and time
    time = datetime.now()
    datestamp = str(time.strftime("%d-%m-%y"))
    timestamp = str(time.strftime("%H:%M:%S"))

    # get pc and user info
    username = os.environ['USERNAME']
    computer_name = os.environ['COMPUTERNAME']
    directory = r'X:\J521\BIM\00_SKA-Tools\SKA_Tools'
    filepath = op.join(directory, 'logger.csv')

    # project info
    project_number = doc.ProjectInformation.get_Parameter(BuiltInParameter.PROJECT_NAME).AsString()
    project_name = doc.ProjectInformation.get_Parameter(BuiltInParameter.PROJECT_NUMBER).AsString()
    file_name = doc.Title

    # put all info parameters together in a single line and add it to a CSV file
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
        with open(filepath, 'a') as f:
            items = [username, computer_name, script_name, project_name, project_number, file_name, datestamp, timestamp]
            lines_to_write = '\n' + ','.join(items)
            f.writelines(lines_to_write)

    except Exception as e:
        forms.alert(str(e))
