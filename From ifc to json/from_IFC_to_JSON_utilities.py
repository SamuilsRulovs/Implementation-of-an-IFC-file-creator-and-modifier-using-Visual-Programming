import ifcopenshell

schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4X3_RC1")


# Returns how much entities are contained in the .ifc file
def countIFCEntities(file):
    types = set(i.is_a() for i in file)

    counter = 0
    for t in types:
        counter += len(file.by_type(t))

    # Somehow IFCOpenShell counts IfcGeometricRepresentationSubContext 2 times
    if len(file.by_type('IfcGeometricRepresentationSubContext')) > 0:
        print(len(file.by_type('IfcGeometricRepresentationSubContext')))
        counter -= len(file.by_type('IfcGeometricRepresentationSubContext'))

    return counter


# Since Ryven needs entities arranged, default positions should be added for each entity
def create_default_position_list(number_of_entities):
    starting_postion_x = 5400.0
    starting_postion_y = 200.0
    positions_x = []
    positions_y = []
    position_x = starting_postion_x
    position_y = starting_postion_y
    for i in range(0, number_of_entities):
        positions_x.append(position_x)
        positions_y.append(position_y)

        position_x -= 900.0
        if position_x <= 1000.0:
            position_x = starting_postion_x
            position_y += 400.0

    return positions_x, positions_y


# ifcopenshell get_info() method returns some attribute values different from ones received .ifc file.
# Thus infromation should be rewritten in accordance to .ifc file
def rewrite_info(info, entity_string):
    ifc_class = schema.declaration_by_name(info['type'])

    continue_loop = True
    char = 0
    new_entity_string = ""
    while continue_loop:
        if entity_string[char] == "(":
            new_entity_string = entity_string[char + 1: len(entity_string) - 1]
            continue_loop = False
        char += 1
    print("\n" + new_entity_string)

    Splitted_entity = new_entity_string.split(",")
    right_entity = []
    i = 0
    while i < len(Splitted_entity):
        x = Splitted_entity[i]
        j = i
        if Splitted_entity[i][0:3] == "(((":
            continue_loop = True
            if Splitted_entity[i][len(str(Splitted_entity[i])) - 1] == ")))":
                x = Splitted_entity[i]
            else:
                while continue_loop:
                    y = Splitted_entity[j]
                    length_y = len(str(y))
                    if Splitted_entity[j][length_y - 3:length_y] == ")))":
                        x = ",".join(Splitted_entity[i:j + 1])
                        continue_loop = False
                    j += 1
                j -= 1

        elif Splitted_entity[i][0:2] == "((":
            continue_loop = True
            if Splitted_entity[i][len(str(Splitted_entity[i])) - 1] == "))":
                x = Splitted_entity[i]
            else:
                while continue_loop:
                    y = Splitted_entity[j]
                    length_y = len(str(y))
                    if Splitted_entity[j][length_y - 2:length_y] == "))":
                        x = ",".join(Splitted_entity[i:j + 1])
                        continue_loop = False
                    j += 1
                j -= 1

        elif Splitted_entity[i][0] == "(":
            continue_loop = True
            if Splitted_entity[i][len(str(Splitted_entity[i])) - 1] == ")":
                x = Splitted_entity[i]
            else:
                while continue_loop:
                    y = Splitted_entity[j]
                    length_y = len(str(y))
                    if Splitted_entity[j][length_y - 1] == ")":
                        x = ",".join(Splitted_entity[i:j + 1])
                        continue_loop = False
                    j += 1
                j -= 1

        i = j
        i += 1
        right_entity.append(x)

    for k in range(0, ifc_class.attribute_count()):
        ifc_attribute = ifc_class.attribute_by_index(k)
        info[ifc_attribute.name()] = right_entity[k]

    return info


def arrangeConnections(node_connections):
    node_connections_dictionary = {}
    for connection in node_connections:
        parent_node_index = connection.parent_node_index
        connected_node_index = connection.connected_node_index
        connected_input_port_index = connection.connected_input_port_index
        if len(str(parent_node_index)) < 2:
            parent_node_index = "0{}".format(str(parent_node_index))
        if len(str(connected_node_index)) < 2:
            connected_node_index = "0{}".format(str(connected_node_index))
        if len(str(connected_input_port_index)) < 2:
            connected_input_port_index = "0{}".format(str(connected_input_port_index))
        entity_place = int(str(parent_node_index) + str(connected_node_index) + str(connected_input_port_index))
        node_connections_dictionary[entity_place] = connection

    sorted_connection_dictionary = sorted(node_connections_dictionary.items(), key=lambda x: x[0], reverse=False)
    sorted_connections = []

    for connection in sorted_connection_dictionary:
        sorted_connections.append(connection[1])

    return sorted_connections


def create_json_dictionary(nodes, sorted_connections_json):
    flow = {
        "algorithm mode": "data", "nodes": nodes, "connections": sorted_connections_json, "GID": 6, "flow view": {
            "drawings": [],
            "view size": [
                6400.0,
                4800.0
            ]
        }}

    general_info = {
        "type": "Ryven project file",
        "ryven version": "v3.1"
    }
    required_packages = [
        {
            "name": "Prototype Nodes",
            "dir": "C:/dev/Bachelorarbeit/Ryven/Prototype Nodes"
        }
    ]

    scripts = [{
        "title": "hello world",
        "variables": {},
        "flow": flow,
        "GID": 1
    }]

    json_dictionary = {
        "general info": general_info,
        "required packages": required_packages,
        "scripts": scripts
    }
    return json_dictionary
