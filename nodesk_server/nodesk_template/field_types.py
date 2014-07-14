from .constants import INDENTATION
from .exceptions import SectionFieldInSectionField


def simple_field(field):
    def func(name, value):
        return INDENTATION + "%s = models.%s(default='%s')\n" % (
            name,
            field,
            value)
    return func

def media_field(field):
    def func(name, value):
        return INDENTATION + "%s = models.%s(default='%s',upload_to='{classname}')\n" % (
            name,
            field,
            value)
    return func

def radiobox_field():
    # FIXME: add choices argument (from value)
    def func(name, value):
        field_string = INDENTATION + 'models.CharField(choices=CHOICES_%s)\n' % name
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
            fields += INDENTATION + name + '_' + value + ' = '
            fields += 'models.BooleanField()\n'
        if isinstance(value, list):
            for v in value:
                fields += INDENTATION + name + '_' + v + ' = '
                fields += 'models.BooleanField()\n'
        return fields

    return func

def raise_exception(e):
    def func(name, value):
        raise e
    return func


field_types_dict = {
    'TextArea' : simple_field('TextField'),
    'TextLine' : simple_field('CharField'),
    'Image' : media_field('ImageField'),
    'Sound' : media_field('FileField'),
    'Video' : media_field('FileField'),
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
    'Section' : raise_exception(SectionFieldInSectionField), # TESTME
}

