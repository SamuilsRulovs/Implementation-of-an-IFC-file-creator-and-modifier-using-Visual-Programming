import ifcopenshell

import base64
import pickle

schema = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4X3_RC1")


def serialize(data) -> str:
    return base64.b64encode(pickle.dumps(data)).decode('ascii')


class IFC_Entity:

    def __init__(self, ifc_id, classname, ifc_class, number_of_attributes):
        self.ifc_id = ifc_id
        self.classname = classname
        self.ifc_class = ifc_class
        self.number_of_attributes = number_of_attributes

        self.attribute_list = []
        self.widget_data_list = {x: "" for x in range(number_of_attributes + 1)}
        self.widget_data_num = 0
        self.dtypte_state_list = {x: "" for x in range(number_of_attributes + 1)}
        self.dtypte_state_num = 0
        self.value_list = {x: "" for x in range(number_of_attributes + 1)}
        self.value_num = 0

        self.inputs = []
        self.outputs = []
        self.position_x = 0.0
        self.position_y = 0.0

    @classmethod
    def set_classname(cls, entity_data):
        # print("\nReached set_classname method")
        ifc_id = "#{}".format(entity_data['id'])
        classname = entity_data['type']
        ifc_class = schema.declaration_by_name(classname)
        number_of_attributes = ifc_class.attribute_count()
        my_instance = cls(ifc_id, classname, ifc_class, number_of_attributes)
        # print(classname)
        return my_instance

    def create_all_lists(self, info):
        self.create_attribute_list(info)

        # ifc_entity.adjust_attribute_list()

        self.create_widget_data_list()
        self.create_data_type_list()
        self.create_value_list()

    def create_attribute_list(self, info):

        for i in range(0, self.number_of_attributes):
            ifc_attribute = self.ifc_class.attribute_by_index(i)

            attribute_value = info[ifc_attribute.name()]

            self.attribute_list.append(attribute_value)
            # print(attribute_value)

    def create_widget_data_list(self):

        self.widget_data_list[self.widget_data_num] = {'text': self.ifc_id}
        self.widget_data_num += 1
        for attribute in self.attribute_list:
            if str(attribute) == 'None':
                self.widget_data_list[self.widget_data_num] = {'text': '$'}
                self.widget_data_num += 1

            else:
                self.widget_data_list[self.widget_data_num] = {'text': str(attribute)}
                self.widget_data_num += 1
        self.widget_data_num = 0

    #
    def create_data_type_list(self):
        self.dtypte_state_list[self.dtypte_state_num] = {'default': '#', 'val': self.ifc_id, 'doc': '', 'bounds': None,
                                                         'size': 'm'}
        self.dtypte_state_num += 1
        for attribute in self.attribute_list:
            if str(attribute) == 'None' or str(attribute)[0] == '#' or str(attribute)[0:2] == '(#':
                self.dtypte_state_list[self.dtypte_state_num] = {'default': '$', 'val': '$', 'doc': '', 'bounds': None,
                                                                 'size': 'l'}
                self.dtypte_state_num += 1
            else:
                self.dtypte_state_list[self.dtypte_state_num] = {'default': '$', 'val': str(attribute), 'doc': '',
                                                                 'bounds': None, 'size': 'l'}
                self.dtypte_state_num += 1

        self.dtypte_state_num += 0

    #
    def create_value_list(self):
        self.value_list[self.value_num] = self.ifc_id
        self.value_num += 1

        for attribute in self.attribute_list:
            if str(attribute)[0] == '#' or str(attribute)[0:2] == '(#':
                self.value_list[self.value_num] = ''
                self.value_num += 1
            else:
                self.value_list[self.value_num] = str(attribute)
                self.value_num += 1

        self.value_num = 0

    #
    def add_positions(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    #
    def write_inputs_part(self, GID):
        inputIFCID = {"type": "data", "label": "OwnIFCID", "GID": GID, "val": serialize(self.value_list[0]),
                      "dtype": "DType.String", "dtype state": serialize(self.dtypte_state_list[0]), "has widget": True,
                      "widget data": serialize(self.widget_data_list[0])}
        GID += 1
        self.inputs.append(inputIFCID)
        for i in range(0, self.number_of_attributes):
            ifc_attribute = self.ifc_class.attribute_by_index(i)
            # print(ifc_attribute.name())
            input = {"type": "data", "label": ifc_attribute.name(), "GID": GID,
                     "val": serialize(self.value_list[i + 1]),
                     "dtype": "DType.String", "dtype state": serialize(self.dtypte_state_list[i + 1]),
                     "has widget": True,
                     "widget data": serialize(self.widget_data_list[i + 1])}

            GID += 1
            self.inputs.append(input)

        return GID

    #
    def write_outputs_part(self, GID):
        self.outputs.append(
            {
                "type": "data",
                "label": "OwnIFCID",
                "GID": GID
            }
        )
        GID += 1
        return GID

    #
    def write_node(self, GID):
        node = {"identifier": "Prototype Nodes.{}".format(self.classname),
                "version": None,
                "state data": "gAR9lC4=",
                "additional data": {
                    "special actions": {},
                    "display title": "{}".format(self.classname.upper())
                },
                "inputs": [],
                "outputs": [{}],
                "GID": GID,
                "pos x": self.position_x,
                "pos y": self.position_y,
                "unconnected ports hidden": False,
                "collapsed": False}
        GID += 1
        GID = self.write_inputs_part(GID)
        GID = self.write_outputs_part(GID)
        node["inputs"] = self.inputs
        node["outputs"] = self.outputs
        return node, GID

    #
    def adjust_attribute_list(self):
        print(self.attribute_list)
        for i in range(0, len(self.attribute_list)):
            attribute = str(self.attribute_list[i])
            if attribute[0] == '#':
                short_attribute = ""
                count = 0
                loop = True
                while loop:
                    if not attribute[count] == '=':
                        short_attribute = short_attribute + attribute[count]
                        count += 1
                    else:
                        loop = False
                self.attribute_list[i] = short_attribute

            if attribute[0:2] == '(#':
                short_attribute = ""
                count = 0
                loop = True

                while loop:
                    if not attribute[count] == '=':
                        short_attribute = short_attribute + attribute[count]
                        count += 1
                    else:
                        loop = False

                for char in range(0, len(attribute)):
                    x = attribute[char: (char + 3)]
                    if attribute[char: (char + 3)] == ", #":
                        short_attribute = short_attribute + ","
                        loop = True
                        while loop:
                            if not attribute[char + 2] == '=':
                                short_attribute = short_attribute + attribute[char + 2]
                                char += 1
                            else:
                                loop = False

                short_attribute = short_attribute + ')'
                self.attribute_list[i] = short_attribute

        print(self.attribute_list)

    def __repr__(self):
        return "\nIFC ID: {}; Class name: {};" \
               "\nIFC class: {}; Number of attributes: {}\nAttribute list: {}\nWidget dictionary: {}" \
               "\nData type state dictionary: {}\nValue dictionary: {}" \
            .format(self.ifc_id, self.classname, self.ifc_class, self.number_of_attributes, self.attribute_list,
                    self.widget_data_list, self.dtypte_state_list, self.value_list)
