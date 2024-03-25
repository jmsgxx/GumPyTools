import os
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Clipboard


def set_text(text):
    Clipboard.SetText(text)


def get_text():
    return Clipboard.GetText()


# Specify the path of the directory you want to open
directory_path = r"X:\J521\BIM"
set_text(directory_path)   # copy to clipboard


# Open the directory
os.startfile(directory_path)
