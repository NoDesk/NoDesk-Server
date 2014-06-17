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



def getTextAreaField() :
    pass

def getTextLineField() :
    pass

def getImageField() :
    pass

def getSoundField() :
    pass

def getVideoField() :
    pass

def getCoordinatesField() :
    pass

def getDateField() :
    pass

def getHourField() :
    pass

def getUserField() :
    pass

def getCreatorField() :
    pass

def getEmailField() :
    pass

def getPhoneField() :
    pass

def getRadioboxField() :
    pass

def getCheckboxField() :
    pass

def getNumberField() :
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
