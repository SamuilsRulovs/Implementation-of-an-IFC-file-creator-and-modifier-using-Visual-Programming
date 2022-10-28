import json

from Node_classes import *
from from_IFC_to_JSON_utilities import *
from Connection_classes import *

# TO DO: correct this text:
# Open .ifc file
# For bachelor thesis purposes only entities from tessellated-item.ifc were implemented in Ryven
# For this reason only file tessellated-item.ifc can be opened with Ryven
# However fromIFCtoJSON and fromJSONtoIFC scripts should convert all files regardless of entity support
ifc = ifcopenshell.open("use_cases/tessellated-item.ifc")
#ifc = ifcopenshell.open("use_cases/two-tessellated-items.ifc")
#ifc = ifcopenshell.open("use_cases/basin-faceted-brep.ifc")
# schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4X3_RC1")

entities_count = countIFCEntities(ifc)
# print(entities_count)

ifc_entities = []
nodes = []
GID = 7

positions_x, positions_y = create_default_position_list(entities_count)
print(entities_count)
file = open("use_cases/tessellated-item.json", "w")
# file = open("use_cases/use-case2.json", "w")
#file = open("use_cases/use-case4.json", "w")
list_of_id = []
endFor = False
for i in range(1, entities_count + 1):
    try:
        entity = ifc.by_id(i)
        list_of_id.append(i)
    except:
        find_instance_id = True
        j = list_of_id[-1] + 1
        while find_instance_id:
            try:
                entity = ifc.by_id(j)
                list_of_id.append(j)
                find_instance_id = False
            except:
                j += 1
                if j >= 10000:
                    print("Too big IFC ID, might be a problem in the countIFCEntities (Some entities were counted several times, thus \"for\" loop continues to go through file even if all entities are already read)")
                    i = entities_count
                    endFor = True
                    break

    if endFor:
        break
    #entity = ifc.by_id(i)
    print(entity)
    entity_string = str(entity)
    info = entity.get_info()
    print('\n', "old info", info)
    info = rewrite_info(info, entity_string)
    ifc_entity = IFC_Entity.set_classname(info)
    print('\n',"new info", info)

    ifc_entity.create_all_lists(info)

    print(ifc_entity)
    ifc_entity.add_positions(positions_x[i - 1], positions_y[i - 1])

    ifc_entities.append(ifc_entity)

    node, GID = ifc_entity.write_node(GID)
    nodes.append(node)

entity_index = 0
node_connections = []
combination_index = 0
for ifc_entity in ifc_entities:
    for i in range(1, ifc_entity.number_of_attributes + 1):
        if ifc_entity.widget_data_list[i]['text'][0] == '#':
            parent_node_IFC_ID = ifc_entity.widget_data_list[i]['text']
            node_connecetion = connecetions.define_connections(ifc_entities, entity_index, i,
                                                               parent_node_IFC_ID)
            print(node_connecetion)
            node_connections.append(node_connecetion)
        elif ifc_entity.widget_data_list[i]['text'][0:2] == '(#':

            entities_to_combine = ifc_entity.widget_data_list[i]['text']
            combined = combine_entities.define_combination(ifc_entity, ifc_entities, entities_to_combine,
                                                           combination_index)
            combined.create_value_list()
            combined.create_data_type_list()
            combined.create_widget_data_list()
            node, GID = combined.write_node(GID)
            nodes.append(node)
            combi_node_connecetion = connecetions(combined.combination_node_index, entity_index, i)
            node_connections.append(combi_node_connecetion)
            print(combined)
            print(combi_node_connecetion)
            for j in range(0, len(combined.list_of_id)):
                node_connecetion = connecetions.define_connections(ifc_entities, combined.combination_node_index, j,
                                                                   combined.list_of_id[j])
                print(node_connecetion)
                node_connections.append(node_connecetion)

            combination_index += 1

    entity_index += 1

#
sorted_connections = arrangeConnections(node_connections)
sorted_connections_json = []

#
for sorted_connection in sorted_connections:
    connection_json, GID = sorted_connection.write_connection(GID)
    sorted_connections_json.append(connection_json)

#
json_dictionary = create_json_dictionary(nodes, sorted_connections_json)

json_file = json.dumps(json_dictionary, indent=3)
file.write(json_file)

file.close()
