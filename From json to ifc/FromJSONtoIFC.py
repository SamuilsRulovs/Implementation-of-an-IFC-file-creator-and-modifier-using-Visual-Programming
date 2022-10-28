import json

from IFCNode_class import *
from IFC_file_writer import *
from utilities import *

#with open("use cases/NEW Tessellated-item.json", "r") as data:
#    objectData = json.load(data)

with open("use cases/use-case3_full_cycle.json", "r") as data:
    objectData = json.load(data)

# with open("use cases/Two-Tessellated-items_full_cycle.json", "r") as data:
#     objectData = json.load(data)

scripts = objectData["scripts"]
flow = scripts[0]["flow"]
nodes = flow["nodes"]
instances = []
val_list = []
dtype_state_list = []
for node in nodes:
    print(node)
    if ifIFCNode(node):
        instance = IFCNode.set_classname(node)
        instances.append(instance)
        for data_input in node["inputs"]:
            print(input)
            instance.create_attribute_list(data_input)
            instance.create_dtypte_state_list(data_input)
            instance.create_widget_data_list(data_input)

sorted_instances = arrangeInstances(instances)

#file = open("use cases/Two-Tessellated-items_full_cycle.ifc", "w")
file = open("use cases/use-case3_full_cycle.ifc", "w")
#file = open("use cases/NEW Tessellated-item.ifc", "w")
file = WriteIFCFile(file, sorted_instances)
file.close()

data.close()
