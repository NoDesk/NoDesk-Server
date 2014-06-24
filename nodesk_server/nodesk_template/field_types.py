from .constants import INDENTATION
#def get_Radiobox_field(yaml,file) :
#    file.write(INDENTATION + yaml['name'] + '_choices_NODESK' + "=(\n")
#    if hasattr(yaml['value'],'__iter__') :
#        for value in yaml['value'] :
#            file.write(INDENTATION*2 + "('%s','%s'),\n" % (value,value))
#    else :
#        file.write(INDENTATION*2 + "('%s','%s')\n" % (yaml['value'],yaml['value']))
#    file.write(INDENTATION + ')\n')

#    file.write(INDENTATION + yaml['name'] + "=")
#    file.write("models.CharField(\n")
#    file.write(INDENTATION*2 + "choices=" + yaml['name'] + '_choices_NODESK' + ',\n')


    #Add here the option of the django Field


#    file.write(INDENTATION + ")\n")

#def get_Checkbox_field(yaml,file) :
#    if hasattr(yaml['value'],'__iter__') :
#        for value in yaml['value'] :
#            file.write(INDENTATION + yaml['name'] + '_' + value + "=")
#            file.write("models.BooleanField(\n")

            #Add here the option of the django Field

#            file.write(INDENTATION + ")\n")
#    else :
#        file.write(INDENTATION + yaml['name'] + '_' + yaml['value'] + "=")
#        file.write("models.BooleanField(\n")

        #Add here the option of the django Field

#        file.write(INDENTATION + ")\n")


#def get_Section_field(yaml,file) :
#    raise Section_fieldInSection_field()

def simple_field(field):
    def func(name, value):
        return INDENTATION + "%s = models.%s(default='%s')" % (
            name,
            field,
            value)
    return func

def radiobox_field():
    # FIXME: add choices argument (from value)
    def func(name, value):
    return func

def checkbox_field():
    def func(name, value):
        pass
    return func



field_types_dict = {
    'TextArea' : simple_field('TextField'),
    'TextLine' : simple_field('CharField'),
    'Image' : simple_field('ImageField'),
    'Sound' : simple_field('FileField'),
    'Video' : simple_field('FileField'),
    'Coordinates' : simple_field('CharField'),
    'Date' : simple_field('DateField'),
    'Time' : simple_field('TimeField'),
    'User' : simple_field('CharField'), # FIXME: foreign key?
    'Creator' : simple_field('CharField'), # FIXME: foreign key?
    'Email' : simple_field('EmailField'),
    'Phone' : simple_field('CharField'),
    'Radiobox' : radiobox_field(),
    'Checkbox' : checkbox_field(),
    'Number' : simple_field('FloatField'),
#    'Section' : lambda value: raise Section_fieldInSection_field, # FIXME
}

