#from django.db import models

#field_types = {
#    'TextArea' : models.TextField,
#    'TextLine' : models.CharField,
#    'Image' : models.CharField, #
#    'Sound' : models.CharField, #
#    'Video' : models.CharField, #
#    'Coordinates' : models.CharField,
#    'Date' : models.DateField, 
#    'Hour' : models.TimeField, #
#    'User' : models.CharField, #
#    'Creator' : models.CharField, #
#    'Email' : models.EmailField,
#    'Phone' : models.CharField,
#    'Radiobox' : models.CharField, #
#    'Checkbox' : models.BooleanField, #
#    'Number' : models.FloatField
#}



def getTextAreaField(yaml,ident_space=4) :
    pass

def getTextLineField(yaml,ident_space=4) :
    pass

def getImageField(yaml,ident_space=4) :
    pass

def getSoundField(yaml,ident_space=4) :
    pass

def getVideoField(yaml,ident_space=4) :
    pass

def getCoordinatesField(yaml,ident_space=4) :
    pass

def getDateField(yaml,ident_space=4) :
    pass

def getHourField(yaml,ident_space=4) :
    pass

def getUserField(yaml,ident_space=4) :
    pass

def getCreatorField(yaml,ident_space=4) :
    pass

def getEmailField(yaml,ident_space=4) :
    pass

def getPhoneField(yaml,ident_space=4) :
    pass

def getRadioboxField(yaml,ident_space=4) :
    pass

def getCheckboxField(yaml,ident_space=4) :
    pass

def getNumberField(yaml,ident_space=4) :
    pass


field_types = {
    'TextArea' : getTextAreaField,
    'TextLine' : getTextLineField,
    'Image' : getImageField,
    'Sound' : getSoundField,
    'Video' : getVideoField,
    'Coordinates' : getCoordinatesField,
    'Date' : getDateField, 
    'Hour' : getHourField,
    'User' : getUserField,
    'Creator' : getCreatorField,
    'Email' : getEmailField,
    'Phone' : getPhoneField,
    'Radiobox' : getRadioboxField,
    'Checkbox' : getCheckboxField,
    'Number' : getNumberField
}
