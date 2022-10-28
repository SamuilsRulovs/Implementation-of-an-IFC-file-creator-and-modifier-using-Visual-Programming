

def WriteIFCFile(file, ifc_instances):  # ,header, ISO):
    # ISO_line = "{};".format(ISO)
    ISO_line = "ISO-10303-21;\n"
    file.write(ISO_line)

    header = "HEADER;\n" \
             "FILE_DESCRIPTION((''),'2;1');\n" \
             "FILE_NAME('','2019-03-20T15:56:21',(''),(''),'BuildingSmart IfcKit by Constructivity','IfcDoc 12.0.0.0','');\n" \
             "FILE_SCHEMA(('IFC4X3_RC1'));\n" \
             "ENDSEC;\n"
    file.write(header)

    data = "\nDATA;\n\n"
    file.write(data)

    for instance in ifc_instances:
        ifc_line = instance.write_ifc_entity()
        file.write(ifc_line)
        print(instance)
        print(ifc_line)
    end = "ENDSEC;\n\n"
    # endISO = "END-{}".format(ISO)
    endISO = "END-ISO-10303-21;"
    file.write(end)
    file.write(endISO)
    return file
