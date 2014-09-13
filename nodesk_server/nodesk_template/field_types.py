from .constants import INDENTATION
from .exceptions import SectionFieldInSectionField


def simple_field(field):
    def func(name, value):
        return INDENTATION + "%s = models.%s(blank=True, null=True)\n" % (
            name,
            field)
    return func

def media_field(field):
    def func(name, value):
        return INDENTATION + "%s = models.%s(blank=True, null=True, upload_to=Template.upload_to_func('{classname}'))\n" % (
            name,
            field)
    return func

def radiobox_field():
    # FIXME: add choices argument (from value)
    def func(name, value):
        field_string = INDENTATION + 'models.CharField(blank=True, null=True,choices=CHOICES_%s)\n' % name
        choices_string = INDENTATION + 'CHOICES_' + name + ' = (\n'
        if isinstance(value, str):
            choices_string += INDENTATION*2 + "('%s','%s')\n" % (value, value)
        if isinstance(value, list):
            for choice in value:
                choices_string += INDENTATION*2 + "('%s','%s'),\n" % (choice, choice)
        choices_string += INDENTATION + ')\n'

        return choices_string + field_string

    return func

def checkbox_field():
    def func(name, value):
        fields = ''
        # FIXME: factor this
        # (with a inner function computing the string for a value)
        if isinstance(value, str):
            fields += INDENTATION + name + '_0' + ' = '
            fields += 'models.BooleanField(default=False)\n'
        if isinstance(value, list):
            for v in range(0,len(value)):
                fields += INDENTATION + name + '_' + str(v) + ' = '
                fields += 'models.BooleanField(default=False)\n'
        return fields

    return func

def raise_exception(e):
    def func(name, value):
        raise e
    return func


field_types_dict = {
    'TextArea' : simple_field('TextField'),
    'TextLine' : simple_field('TextField'),
    'Image' : media_field('FileField'),
    'Sound' : media_field('FileField'),
    'Video' : media_field('FileField'),
    'Coordinates' : simple_field('TextField'),
    'Date' : simple_field('DateField'),
    'Time' : simple_field('TimeField'),
    'User' : simple_field('TextField'), # FIXME: foreign key?
    'Creator' : simple_field('TextField'), # FIXME: foreign key?
    'Email' : simple_field('EmailField'),
    'Phone' : simple_field('TextField'),
    'Radiobox' : radiobox_field(),
    'Checkbox' : checkbox_field(),
    'Number' : simple_field('FloatField'),
    'Section' : raise_exception(SectionFieldInSectionField), # TESTME
}

