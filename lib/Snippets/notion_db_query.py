# -*- coding: utf-8 -*-

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗
# ║║║║╠═╝║ ║╠╦╝ ║ 
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ # imports
# ================================================================================================
import sys
import csv
from pyrevit import revit, EXEC_PARAMS
import api_key
import requests
import json
from Autodesk.Revit.DB import *
from Snippets._context_manager import try_except
import os
from datetime import datetime
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝# variables
# ======================================================================================================
sender = __eventsender__
arg = __eventargs__
doc = revit.doc


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝#main
# =========================================================================================================
notion_token = api_key.NOTION_TOKEN
notion_page_id = api_key.NOTION_AP_PAGE_ID
NOTION_ENDPOINT = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": "Bearer {}".format(notion_token),
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def notion_db_query():

    # -------------------------------------------------------------------
    # 🔵 import as json file to check
    url = 'https://api.notion.com/v1/databases/{}/query'.format(notion_page_id)
    num_pages = 100
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    file_path = r'C:\Users\gary_mak\Documents\GitHub\GumPyTools.extension\lib\Ref\db_ap_open.json'
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # -------------------------------------------------------------------

