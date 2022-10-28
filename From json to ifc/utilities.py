

def ifIFCNode(ifc_data):
    classname = ifc_data['additional data']['display title']
    if classname[0:3] == 'IFC':
        return True
    else:
        return False


def arrangeInstances(instances):
    instace_dictionary = {}
    for instance in instances:
        entity_place = instance.recieve_entity_place()
        instace_dictionary[entity_place] = instance

    sorted_instance_dictionary = sorted(instace_dictionary.items(), key=lambda x: x[0], reverse=False)
    sorted_instances = []
    for instance in sorted_instance_dictionary:
        sorted_instances.append(instance[1])

    return sorted_instances
