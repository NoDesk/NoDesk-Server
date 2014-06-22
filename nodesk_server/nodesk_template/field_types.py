#FIXME remove the try/catch block -> it's only used for debug purpose
try:
    from nodesk_template.constants import *
except ImportError :
    IDENTATION = ' '*4


def get_TextArea_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.TextField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_TextLine_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Image_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.ImageField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Sound_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.FileField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Video_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.FileField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Coordinates_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Date_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.DateField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Time_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.TimeField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_User_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(\n")
#    file.write("models.ForeignKey('User'") #XXX Maybe use a user reference

    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Creator_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(\n")
#    file.write("models.ForeignKey('User'") #XXX Maybe use a user reference
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Email_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.EmailField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Phone_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")

def get_Radiobox_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + '_choices_NODESK' + "=(\n")
    if hasattr(yaml['value'],'__iter__') :
        for value in yaml['value'] :
            file.write(IDENTATION*2 + "('%s','%s'),\n" % (value,value))
    else :
        file.write(IDENTATION*2 + "('%s','%s')\n" % (yaml['value'],yaml['value']))
    file.write(IDENTATION + ')\n')

    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.CharField(\n")
    file.write(IDENTATION*2 + "choices=" + yaml['name'] + '_choices_NODESK' + ',\n')
    

    #Add here the option of the django Field
    
    
    file.write(IDENTATION + ")\n")

def get_Checkbox_field(yaml,file) :
    if hasattr(yaml['value'],'__iter__') :
        for value in yaml['value'] :
            file.write(IDENTATION + yaml['name'] + '_' + value + "=")
            file.write("models.BooleanField(\n")
    
            #Add here the option of the django Field
    
            file.write(IDENTATION + ")\n")
    else :
        file.write(IDENTATION + yaml['name'] + '_' + yaml['value'] + "=")
        file.write("models.BooleanField(\n")
    
        #Add here the option of the django Field
    
        file.write(IDENTATION + ")\n")

def get_Number_field(yaml,file) :
    file.write(IDENTATION + yaml['name'] + "=")
    file.write("models.FloatField(\n")
    
    #Add here the option of the django Field
    
    file.write(IDENTATION + ")\n")


    
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
