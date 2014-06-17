
class UnrecognizedFieldType(Exception) :
    def __init__(self,field_type,field_name) :
        self.name = field_name
        self.type = field_type
    def __str__(self) :
        return "%s : Unrecongnized type for the field %s" % (self.type,self.name)

class SectionFieldInSectionField(Exception) :
    def __str__(self) :
        return "Cannot put a Section field inside a Section field"
