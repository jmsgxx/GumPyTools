# -*- coding: utf-8 -*-

"""
Family Wrecker Catcher
__________________________________
Author: Joven Mark Gumana
"""

from pyrevit import revit, EXEC_PARAMS
import sys
from datetime import datetime
import os

sender = __eventsender__
arg = __eventargs__
doc = revit.doc

if doc.IsFamilyDocument:
    sys.exit()

# ✅ main code
else:
    family_name = EXEC_PARAMS.event_args.FamilyName
    family_path = EXEC_PARAMS.event_args.FamilyPath
    fam_path_name = None
    if family_path == '':
        family_path = '<missing link>'
        fam_path_name = family_path
    else:
        fam_path_name = family_path + family_name
    loaded_to = EXEC_PARAMS.event_args.Document.Title
    cur_time = datetime.now()
    date = str(cur_time.strftime("%d-%m-%y"))
    time = str(cur_time.strftime("%H:%M:%S"))

    # get pc and user info
    username = os.environ['USERNAME']
    computer_name = os.environ['COMPUTERNAME']

    filepath = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\fam_logger.csv'

    try:
        with open(filepath, 'a') as f:
            if not os.path.isfile(filepath):
                open(filepath, 'w').close()
            if os.stat(filepath).st_size == 0:
                headings = [
                    'User',
                    'Computer Number',
                    'Loaded to',
                    'Family Name',
                    'File Path',
                    'Date',
                    'Time'
                ]
                f.write(','.join(headings) + '\n')

            items = [
                username,
                computer_name,
                loaded_to,
                family_name,
                fam_path_name,
                date,
                time
            ]
            lines_to_write = ','.join(items) + '\n'
            f.write(lines_to_write)
    except:
        pass
