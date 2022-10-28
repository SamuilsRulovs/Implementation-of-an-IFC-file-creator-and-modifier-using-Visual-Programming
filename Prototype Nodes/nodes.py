from ryven.NENV import *


# your node definitions go here
class NodeBase(Node):
    pass

    # here we could add some stuff for all nodes below...


class IFCNode(NodeBase):
    def __init__(self, params):
        super().__init__(params)
        self.val = None

    init_inputs = [
        NodeOutputBP(),
    ]

    init_outputs = [
        NodeOutputBP(),
    ]

    def place_event(self):
        self.update()

    def update_event(self, inp=-1):
        self.set_output_val(0, self.input(0))

        self.val = self.input(0)
        if self.session.gui:
            self.main_widget().show_val(self.val)


# class IFC_Node(IFCNode):

class combine_entities(NodeBase):
    title = 'Combine entities'
    init_inputs = [NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='IFCID')]

    init_outputs = [NodeOutputBP(label='IFCID')]
    color = '#aabb44'

    def __init__(self, params):
        super().__init__(params)
        self.val = ""

        self.num_inputs = 0
        self.actions['add input'] = {'method': self.add_operand_input}

    def place_event(self):
        self.actions['add input'] = {'method': self.add_operand_input}
        for i in range(len(self.inputs)):
            self.register_new_operand_input(i)
        self.update()

    def add_operand_input(self):
        self.create_input_dt(label='IFCID', dtype=dtypes.String(default="$", size='l'))
        self.register_new_operand_input(self.num_inputs)
        self.update()

    def remove_operand_input(self, index):
        self.delete_input(index)
        self.num_inputs -= 1
        # del self.actions[f'remove input {index}']
        self.rebuild_remove_actions()
        self.update()

    def register_new_operand_input(self, index):
        self.actions[f'remove input {index}'] = {
            'method': self.remove_operand_input,
            'data': index
        }
        self.num_inputs += 1

    def rebuild_remove_actions(self):

        remove_keys = []
        for k, v in self.actions.items():
            if k.startswith('remove input'):
                remove_keys.append(k)

        for k in remove_keys:
            del self.actions[k]

        for i in range(self.num_inputs):
            self.actions[f'remove input {i}'] = {'method': self.remove_operand_input, 'data': i}

    def update_event(self, inp=-1):
        values = [self.input(i) for i in range(0, len(self.inputs))]

        output = "("
        for i in range(len(values) - 1):
            output = output + values[i] + ","

        output = output + values[len(values) - 1] + ")"
        self.val = output
        self.set_output_val(0, output)
        if self.session.gui:
            self.main_widget().show_val(self.val)


# Infromation about project: IFCPROJECT, IFCOWNERHISTORY etc.

class IfcBuilding(IFCNode):
    title = 'IFCBUILDING'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectPlacement'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Representation'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LongName'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CompositionType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ElevationOfRefHeight'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ElevationOfTerrain'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='BuildingAddress'),
    ]
    init_outputs = [NodeOutputBP(label='OwnIFCID')
                    ]
    color = '#aabb44'

class IfcOwnerHistory(IFCNode):
    title = 'IFCOWNERHISTORY'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwningUser'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwningApplication'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='State'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ChangeAction'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LastModifiedDate'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LastModifyingUser'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LastModifyingApplication'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CreationDate'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'

    # def update_event(self, inp=-1):
    #     if self.input(0):
    #         OwnIFCID = self.input(0)
    #         self.set_output_val(OwnIFCID)


class IfcPersonAndOrganization(IFCNode):
    title = 'IFCPERSONANDORGANIZATION'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ThePerson'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TheOrganization'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Roles')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcApplication(IFCNode):
    title = 'IFCAPPLICATION'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ApplicationDeveloper'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Version'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ApplicationFullName'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ApplicationIdentifier')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcPerson(IFCNode):
    title = 'IFCPERSON'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Identification'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='FamilyName'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GivenName'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='MiddleNames'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='PrefixTitles'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='SuffixTitles'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Roles'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Addresses')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcOrganization(IFCNode):
    title = 'IFCORGANIZATION'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Identification'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Roles'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Addresses')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcProject(IFCNode):
    title = 'IFCPROJECT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LongName'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Phase'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RepresentationContexts'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='UnitsInContext')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcGeometricRepresentationContext(IFCNode):
    title = 'IFCGEOMETRICREPRESENTATIONCONTEXT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ContextIdentifier'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ContextType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CoordinateSpaceDimension'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Precision'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='WorldCoordinateSystem'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TrueNorth')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcGeometricRepresentationSubContext(IFCNode):
    title = 'IFCGEOMETRICREPRESENTATIONSUBCONTEXT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ContextIdentifier'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ContextType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CoordinateSpaceDimension'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Precision'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='WorldCoordinateSystem'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TrueNorth'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ParentContext'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TargetScale'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TargetView'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='UserDefinedTargetView')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcShapeRepresentation(IFCNode):
    title = 'IFCSHAPEREPRESENTATION'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ContextOfItems'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RepresentationIdentifier'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RepresentationType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Items')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcProductDefinitionShape(IFCNode):
    title = 'IFCPRODUCTDEFINITIONSHAPE'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Representations'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcRelAggregates(IFCNode):
    title = 'IFCRELAGGREGATES'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RelatingObject'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RelatedObjects'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcBuildingElementProxy(IFCNode):
    title = 'IFCBUILDINGELEMENTPROXY'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectPlacement'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Representation'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Tag'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='PredefinedType'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcRelContainedInSpatialStructure(IFCNode):
    title = 'IFCRELCONTAINEDINSPATIALSTRUCTURE'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RelatedElements'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RelatingStructure'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


# Units


class IfcUnitAssignment(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCUNITASSIGNMENT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Units')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcSIUnit(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCSIUNIT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Dimensions'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='UnitType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Prefix'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcConversionBasedUnit(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCCONVERSIONBASEDUNIT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Dimensions'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='UnitType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ConversionFactor')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcMeasureWithUnit(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCMEASUREWITHUNIT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ValueComponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='UnitComponent'),
    ]
    # Something is wrong
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


# Placements

class IfcAxis2Placement3D(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCAXIS2PLACEMENT3D'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Location'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Axis'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RefDirection')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcLocalPlacement(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCLOCALPLACEMENT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='PlacementRelTo'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RelativePlacement')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcDirection(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCDIRECTION'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='scale'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='scale'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='scale'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'

    def __init__(self, params):
        super().__init__(params)
        self.val = ""

        self.num_inputs = 0
        self.actions['add input'] = {'method': self.add_operand_input}

    def place_event(self):
        self.actions['add input'] = {'method': self.add_operand_input}
        for i in range(len(self.inputs)):
            self.register_new_operand_input(i)
        self.update()

    def add_operand_input(self):
        self.create_input_dt(label='scale', dtype=dtypes.String(default="$", size='l'))
        self.register_new_operand_input(self.num_inputs)
        self.update()

    def remove_operand_input(self, index):
        self.delete_input(index)
        self.num_inputs -= 1
        # del self.actions[f'remove input {index}']
        self.rebuild_remove_actions()
        self.update()

    def register_new_operand_input(self, index):
        self.actions[f'remove input {index}'] = {
            'method': self.remove_operand_input,
            'data': index
        }
        self.num_inputs += 1

    def rebuild_remove_actions(self):

        remove_keys = []
        for k, v in self.actions.items():
            if k.startswith('remove input'):
                remove_keys.append(k)

        for k in remove_keys:
            del self.actions[k]

        for i in range(self.num_inputs):
            self.actions[f'remove input {i}'] = {'method': self.remove_operand_input, 'data': i}


class IfcCartesianPoint(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCCARTESIANPOINT'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Coordinates'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID'),
    ]
    color = '#aabb44'


class IfcCartesianPointList3D(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCCARTESIANPOINTLIST3D'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CoordList'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TagList'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID'),
    ]
    color = '#aabb44'


class IfcDimensionalExponents(IFCNode):
    """Generate a random number in a given range"""
    # this __doc__ string will be displayed as tooltip in the editor

    title = 'IFCDIMENSIONALEXPONENTS'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LengthExponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='MassExponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='TimeExponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ElectricCurrentExponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ThermodynamicTemperatureExponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='AmountOfSubstanceExponent'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LuminousIntensityExponent'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID'),
    ]
    color = '#aabb44'


class IfcPolylop(IFCNode):
    title = 'IFCPOLYLOOP'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='IFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='IFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='IFCID')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcTriangulatedFaceSet(IFCNode):
    title = 'IFCTRIANGULATEDFACESET'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Coordinates'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Normals'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Closed'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CoordIndex'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='PnIndex')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcColumn(IFCNode):
    title = 'IFCCOLUMN'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectPlacement'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Representation'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Tag'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='PredefinedType'),
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


class IfcSite(IFCNode):
    title = 'IFCCOLUMN'
    init_inputs = [
        NodeInputBP(dtype=dtypes.String(default="#", size='m'), label='OwnIFCID'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='GlobalId'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='OwnerHistory'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Name'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Description'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='ObjectPlacement'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='Representation'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LongName'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='CompositionType'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RefLatitude'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RefLongitude'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='RefElevation'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='LandTitleNumber'),
        NodeInputBP(dtype=dtypes.String(default="$", size='l'), label='SiteAddress')
    ]
    init_outputs = [
        NodeOutputBP(label='OwnIFCID')
    ]
    color = '#aabb44'


export_nodes(
    combine_entities,

    IfcBuilding,
    IfcOwnerHistory,
    IfcPersonAndOrganization,
    IfcApplication,
    IfcPerson,
    IfcOrganization,
    IfcProject,
    IfcGeometricRepresentationContext,
    IfcGeometricRepresentationSubContext,
    IfcShapeRepresentation,
    IfcProductDefinitionShape,
    IfcRelAggregates,
    IfcBuildingElementProxy,
    IfcRelContainedInSpatialStructure,

    IfcUnitAssignment,
    IfcSIUnit,
    IfcConversionBasedUnit,
    IfcMeasureWithUnit,

    IfcAxis2Placement3D,
    IfcLocalPlacement,
    IfcDirection,
    IfcCartesianPoint,
    IfcCartesianPointList3D,
    IfcDimensionalExponents,
    IfcPolylop,
    IfcTriangulatedFaceSet,

    IfcColumn,
    IfcSite,
)
