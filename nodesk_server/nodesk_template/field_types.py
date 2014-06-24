from nodesk_template.exceptions import Section_fieldInSection_field
from nodesk_templates.constants import INDENTATION
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

def simple_field(field, value):
    return '    models.%s(default=%s)' % (field, value)

def choices_field(field, value):
    # FIXME: add choices argument (from value)
    return '    models.%s()' % field



field_types_dict = {
    'TextArea' : lambda value: simple_field('TextField', value),
    'TextLine' : lambda value: simple_field('TextLine', value),
    'Image' : lambda value: simple_field('models.ImageField', value),
    'Sound' : lambda value: simple_field('models.FileField', value),
    'Video' : lambda value: simple_field('models.FileField', value),
    'Coordinates' : lambda value: simple_field('models.CharField', value),
    'Date' : lambda value: simple_field('models.DateField', value),
    'Time' : lambda value: simple_field('models.TimeField', value),
    'User' : lambda value: simple_field('models.CharField', value),# FIXME foreign key?
    'Creator' : lambda value: simple_field('models.CharField', value), # FIXME foreign key?
    'Email' : lambda value: simple_field('models.EmailField', value),
    'Phone' : lambda value: simple_field('models.CharField', value),
    'Radiobox' : lambda value: choices_field('models.BooleanField', value), # FIXME
    'Checkbox' : lambda value: choices_field('models.BooleanField', value), # FIXME
    'Number' : lambda value: simple_field('models.FloatField', value),
#    'Section' : lambda value: raise Section_fieldInSection_field, # FIXME
}


def field_yaml_to_model(field, name, value) :
    return '    {name} = {field}()\n'.format(
        name,
        field_types_dict[field])
