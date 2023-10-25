from Autodesk.Revit.DB import *
new_paint = Paint(elementId, face, materialId)

def PaintWallFaces(wall, matId):
"""Paint any unpainted faces of a given wall"""\
# type hint:
doc = wall.Document
geometryElement = wall.get_Geometry(Options())
for geometryObject in geometryElement:
    if geometryObject is Solid:
        solid = geometryObject
        for face in solid.Faces:
            if doc.IsPainted(wall.Id, face) == False:
                doc.Paint(wall.Id, face, matId)








