from Autodesk.Revit.DB import *
import pyrevit

all_ref = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CLines).WhereElementIsNotElementType().ToElements()

t = Transaction(doc, 'ref delete')


t.Start()
for ref in all_ref:
    ref_id = ref.Id
    if ref.SubCategories.Name is None:
        doc.Delete(ref_id)
t.Commit()