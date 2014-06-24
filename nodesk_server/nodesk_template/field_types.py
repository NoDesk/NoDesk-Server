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

def choices_field(field):
    # FIXME: add choices argument (from value)
    return INDENTATION + 'models.%s()' % field
    def func(name, value):
        return INDENTATION + 'models.%s()' % field
    return func



field_types_dict = {
    'TextArea' : simple_field('TextField'),
    'Image' : simple_field('models.ImageField'),
    'Sound' : simple_field('models.FileField'),
    'Video' : simple_field('models.FileField'),
    'Coordinates' : simple_field('models.CharField'),
    'Date' : simple_field('models.DateField'),
    'Time' : simple_field('models.TimeField'),
    'User' : simple_field('models.CharField'), # FIXME: foreign key?
    'Creator' : simple_field('models.CharField'), # FIXME: foreign key?
    'Email' : simple_field('models.EmailField'),
    'Phone' : simple_field('models.CharField'),
    'Radiobox' : choices_field('models.BooleanField'),
    'Checkbox' : choices_field('models.BooleanField'),
    'Number' : simple_field('models.FloatField'),
    'TextLine' : simple_field('CharField'),
#    'Section' : lambda value: raise Section_fieldInSection_field, # FIXME
}

