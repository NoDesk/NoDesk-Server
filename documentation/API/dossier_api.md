#Dossier HTTP API

The dossier API is accessible at the URL : http://\<NODESK_URL\>/dossier/\<DOSSIER_API\>.
Depending on <DOSSIER_API>, you can access the different part of the API :

##'^$'
Not used for now : will result in an code 404.

##'^[0-9]+/?$' == '^\<template_id\>/?$'
###GET request
You will get the list of dossier using the template with the ID <template_id>.
You won't receive the dossiers' content, just general informations about them
(like their ID) to get them later.
The server will serve the list in JSON with this format :
```
[
    DOSSIER_INFO,
    DOSSIER_INFO,
    ...
]
```

with DOSSIER_INFO being :
```
{
    "name":<name of the dossier>
    "date":<date of last update/creation of the dossier>
    "pk":<dossier ID>
}
```

###POST request
####Content-Type : "application/json"
If the Content-Type of the POST is "application/json", then the server will use the json to
create a new dossier, using the template with the ID <template_id>.  
The format of the JSON is simple : it's just an json object which keys are the name
of the template's fields and values are the fields' value.  
For example :
```
{
    "field_name_1" : <value_field_name_1>,
    "field_name_2" : <value_field_name_2>,
    "field_name_3" : <value_field_name_3>,
    ...
}
```

##'^[0-9]+/[0-9]+/?$' == '^\<template\_id\>/\<dossier_id\>/?$'
###GET request
You will get all the field value for the dossier using the template <template_id>
and with the ID <dossier_id>. The response will be in JSON, and it will look like :
```
{
    "pk": <dossier_id>,
    "model": <template_name>,
    "fields":
    {
        <field_1> : <value_field_1>,
        <field_2> : <value_field_2>,
        <field_3> : <value_field_3>,
        ...
    }
}
```

###POST request
####Content-Type : "application/json"
If the Content-Type of the POST is "application/json", then the server will use the json to
modify the fields' value of the dossier using the template with the ID <template_id>
and with the ID <dossier_id>.  
The format of the JSON is simple : it's just an json object which keys are the name
of the template's fields and values are the fields' value.  
For example :
```
{
    "field_name_1" : <value_field_name_1>,
    "field_name_2" : <value_field_name_2>,
    "field_name_3" : <value_field_name_3>,
    ...
}
```

####Content-Type : "multipart/form-data"
If the Content-Type is "multipart/form-data", the server FOR NOW (may change later)
will look in the body of the request for files (and nothing else : may change later).  
You can use that to upload files for a media field (like audio,video,photo...) of a dossier.
The files/fields of the "multipart/form-data" must have the same name as the
field name of the template used by the dossier you wish to upload to.  
You really just can think about it like if you submit an html <form> to upload files.


##'^[0-9]+/[0-9]+/.+/?$' == '^\<template\_id\>/\<dossier\_id\>/\<field\_name\>/?$'
For now, this URL is only used to get the media field of a dossier (audio, video, photo...)  
**The format of the URL may change in the future**

###GET request
You will get the file stored in the field <field_name> of the dossier <dossier_id>
that use the template <template_id>.
The type of the file will be **guessed** and put in Content-Type.
