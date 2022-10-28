import base64
import pickle


def deserialize(data):
    return pickle.loads(base64.b64decode(data))


class IFCNode:

    def __init__(self, classname, number_of_attributes):
        self.classname = classname
        self.number_of_attributes = number_of_attributes
        self.attribute_list = {x: "" for x in range(number_of_attributes)}
        self.attribute_num = 0
        self.dtypte_state_list = {x: "" for x in range(number_of_attributes)}
        self.dtypte_state_num = 0
        self.widget_data_list = {x: "" for x in range(number_of_attributes)}
        self.widget_data_num = 0

    #
    @classmethod
    def set_classname(cls, ifc_data):
        print("Reached set_classname method")

        classname = ifc_data['additional data']['display title']
        number_of_attributes = len(ifc_data['inputs'])

        my_instance = cls(classname, number_of_attributes)
        return my_instance

    #
    def create_attribute_list(self, data_input):
        try:
            val = deserialize(data_input['val'])
            self.attribute_list[self.attribute_num] = val
            self.attribute_num += 1

        except:
            self.attribute_num += 1

    #
    def create_dtypte_state_list(self, data_input):
        try:
            dtype_state = deserialize(data_input['dtype state'])
            self.dtypte_state_list[self.dtypte_state_num] = dtype_state
            self.dtypte_state_num += 1
        except:
            self.dtypte_state_num += 1

    #
    def create_widget_data_list(self, data_input):
        try:
            widget_data = deserialize(data_input['widget data'])
            self.widget_data_list[self.widget_data_num] = widget_data
            self.widget_data_num += 1
        except:
            self.widget_data_num += 1

    #
    def write_ifc_entity(self):
        IFC_ID = "{}= ".format(self.widget_data_list[0]['text'])
        Entity = "{}".format(self.classname)

        ifc_line = IFC_ID + Entity + "("
        for i in range(1, self.number_of_attributes - 1):
            ifc_line = ifc_line + "{},".format(self.widget_data_list[i]['text'])

        ifc_line = ifc_line + "{});\n".format(self.widget_data_list[self.number_of_attributes - 1]['text'])
        return ifc_line

    #
    def recieve_entity_place(self):
        IFC_ID = self.widget_data_list[0]['text']
        place = int(IFC_ID[1:])
        return place

    #
    def __repr__(self):
        return "\nClass name: {} Number of attributes: {} \nAttribute list {} \nDtype state list {} \nWidget data dictionary {}" \
            .format(self.classname, self.number_of_attributes, self.attribute_list, self.dtypte_state_list,
                    self.widget_data_list)
