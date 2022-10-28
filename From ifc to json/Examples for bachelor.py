import ifcopenshell

ifc = ifcopenshell.open("tessellated-item.ifc")
entity = ifc.by_id(1)
print(entity)
