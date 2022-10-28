import ifcopenshell

import base64
import pickle

schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4X3_RC1")


def serialize(data) -> str:
    return base64.b64encode(pickle.dumps(data)).decode('ascii')


class combine_entities:
    def __init__(self, list_of_id, combination_node_index, position_x, position_y):
        self.list_of_id = list_of_id
        self.combination_node_index = combination_node_index
        self.position_x = position_x
        self.position_y = position_y

        self.widget_data_list = {x: "" for x in range(len(self.list_of_id))}
        self.widget_data_num = 0
        self.dtypte_state_list = {x: "" for x in range(len(self.list_of_id))}
        self.dtypte_state_num = 0
        self.value_list = {x: "" for x in range(len(self.list_of_id))}
        self.value_num = 0

        self.inputs = []
        self.outputs = []
        self.special_action_dict = {}

    @classmethod
    def define_combination(cls, entity, entities, entities_to_combine,
                         combination_index):

        combination_node_index = len(entities) + combination_index
        string_of_IFCID = entities_to_combine[1:-1]

        list_of_ID = string_of_IFCID.split(",")
        new_isntance = cls(list_of_ID, combination_node_index, entity.position_x - 300, entity.position_y + 200)

        return new_isntance

    def create_widget_data_list(self):
        for IFCID in self.list_of_id:
            if str(IFCID) == 'None':
                self.widget_data_list[self.widget_data_num] = {'text': '$'}
                self.widget_data_num += 1

            else:
                self.widget_data_list[self.widget_data_num] = {'text': str(IFCID)}
                self.widget_data_num += 1
        self.widget_data_num = 0

    def create_data_type_list(self):
        for IFCID in self.list_of_id:
            if str(IFCID) == 'None' or str(IFCID)[0] == '#' or str(IFCID)[0:2] == '(#':
                self.dtypte_state_list[self.dtypte_state_num] = {'default': '$', 'val': '$', 'doc': '', 'bounds': None,
                                                                 'size': 'l'}
                self.dtypte_state_num += 1
            else:
                self.dtypte_state_list[self.dtypte_state_num] = {'default': '$', 'val': str(IFCID), 'doc': '',
                                                                 'bounds': None, 'size': 'l'}
                self.dtypte_state_num += 1

        self.dtypte_state_num += 0

    def create_value_list(self):
        for IFCID in self.list_of_id:
            if str(IFCID)[0] == '#' or str(IFCID)[0:2] == '(#':
                self.value_list[self.value_num] = ''
                self.value_num += 1
            else:
                self.value_list[self.value_num] = str(IFCID)
                self.value_num += 1

        self.value_num = 0

    def write_inputs_part(self, GID):
        for i in range(0, len(self.list_of_id)):
            input = {"type": "data", "label": "IFCID", "GID": GID,
                     "dtype": "DType.String", "dtype state": serialize(self.dtypte_state_list[i]),
                     "has widget": True,
                     "widget data": serialize(self.widget_data_list[i])}

            GID += 1
            self.inputs.append(input)

        return GID

    def write_outputs_part(self, GID):
        self.outputs.append(
            {
                "type": "data",
                "label": "IFCID",
                "GID": GID
            }
        )
        GID += 1
        return GID

    def write_special_actions(self):
        self.special_action_dict["add input"] = "add_operand_input"
        action_remove_input = {"method": "remove_operand_input", "data": 0}
        for i in range(0, len(self.list_of_id)):
            action_remove_input["data"] = i
            self.special_action_dict["remove input {}".format(i)] = {"method": "remove_operand_input", "data": i}

        print('"special actions": {}'.format(self.special_action_dict))

    def write_node(self, GID):
        node = {"identifier": "Prototype Nodes.combine_entities",
                "version": None,
                "state data": "gAR9lC4=",
                "additional data": {
                    "special actions": {},
                    "display title": "Combine entities"
                },
                "inputs": [],
                "outputs": [{}],
                "GID": GID,
                "pos x": self.position_x,
                "pos y": self.position_y,
                "unconnected ports hidden": False,
                "collapsed": False}
        GID += 1
        self.write_special_actions()
        GID = self.write_inputs_part(GID)
        GID = self.write_outputs_part(GID)
        node["additional data"]["special actions"] = self.special_action_dict
        node["inputs"] = self.inputs
        node["outputs"] = self.outputs
        return node, GID

    def __repr__(self):
        return "\nList of ID: {}\nCombination node index: {}\nWidget dictionary: {}" \
               "\nData type dictionary: {}\nValue dictionary: {}" \
            .format(self.list_of_id, self.combination_node_index, self.widget_data_list, self.dtypte_state_list,
                    self.value_list)


class connecetions:
    def __init__(self, parent_node_index, connected_node_index, connected_input_port_index):
        self.parent_node_index = parent_node_index
        self.output_port_index = 0
        self.connected_node_index = connected_node_index
        self.connected_input_port_index = connected_input_port_index

    @classmethod
    def define_connections(cls, entities, connected_node_index, connected_input_port_index, parent_node_IFC_ID):
        parent_node_index = 0
        for enitity in entities:
            if str(enitity.ifc_id) == str(parent_node_IFC_ID):
                my_instance = cls(parent_node_index, connected_node_index, connected_input_port_index)
                return my_instance

            parent_node_index += 1

    def write_connection(self, GID):
        connection = {
            "GID": GID,
            "parent node index": self.parent_node_index,
            "output port index": self.output_port_index,
            "connected node": self.connected_node_index,
            "connected input port index": self.connected_input_port_index}
        GID += 1
        return connection, GID

    def __repr__(self):
        return "\nparent node index: {} \noutput port index: {}\nconnected node : {} \nconnected input port index: {}\n" \
            .format(self.parent_node_index, self.output_port_index, self.connected_node_index,
                    self.connected_input_port_index)
