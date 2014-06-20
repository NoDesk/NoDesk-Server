#from django.db import models
from nodesk_template.constants import *

#field_types = {
#    'TextArea' : models.TextField,
#    'TextLine' : models.CharField,
#    'Image' : models.CharField, #
#    'Sound' : models.CharField, #
#    'Video' : models.CharField, #
#    'Coordinates' : models.CharField,
#    'Date' : models.DateField, 
#    'Time' : models.TimeField, #
#    'User' : models.CharField, #
#    'Creator' : models.CharField, #
#    'Email' : models.EmailField,
#    'Phone' : models.CharField,
#    'Radiobox' : models.CharField, #
#    'Checkbox' : models.BooleanField, #
#    'Number' : models.FloatField
#}



def get_TextArea_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.TextField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_TextLine_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Image_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.ImageField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Sound_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.FileField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Video_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.FileField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Coordinates_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Date_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.DateField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Time_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.TimeField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_User_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(")
#    file.write("models.ForeignKey('User'") #XXX Maybe use a user reference

    #Add here the option of the django Field
    
    file.write(")\n")

def get_Creator_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(")
#    file.write("models.ForeignKey('User'") #XXX Maybe use a user reference
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Email_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.EmailField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Phone_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Radiobox_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(")
    
    #Add here the option of the django Field
    
    #file.write("choices=")
    file.write(")\n")

def get_Checkbox_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.BooleanField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")

def get_Number_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.FloatField(")
    
    #Add here the option of the django Field
    
    file.write(")\n")


    
def get_Section_field(yaml,file) :
    raise Section_fieldInSection_field()



field_types = {
    'TextArea' : get_TextArea_field,
    'TextLine' : get_TextLine_field,
    'Image' : get_Image_field,
    'Sound' : get_Sound_field,
    'Video' : get_Video_field,
    'Coordinates' : get_Coordinates_field,
    'Date' : get_Date_field, 
    'Time' : get_Time_field,
    'User' : get_User_field,
    'Creator' : get_Creator_field,
    'Email' : get_Email_field,
    'Phone' : get_Phone_field,
    'Radiobox' : get_Radiobox_field,
    'Checkbox' : get_Checkbox_field,
    'Number' : get_Number_field,
    'Section' : get_Section_field
}
