#Template HTTP API

The template API is accessible at the URL : http://<NODESK_URL>/template/<TEMPLATE_API>.
Depending on <TEMPLATE_API>, you can access the different part of the API (describe by a regex) :

##'^$' : nothing
###GET request
You will get the list of the templates stored by NoDesk-Server.
You can add to the GET request 2 parameters :
 * alive : 
    - If "true", the list served will only contained the template that are
    considered alive (the one in the template directory : nodesk-app can only create
    new dossier for alive template).
    - If "false", the list served will only contained the template that are
    considered dead (the contrary of alive).
    - If not added to the GET request, the list served by the server will contains
    all the template (both alive and dead). 
 * json :
    - If "true", the list served by the server will also contain the json equivalent
    to the YAML of the template.
    - If "false" or not added to the request, the list won't contain the json
    of the template.

The JSON served will look like :
```
{
    "name":<template_name>,
    "pk":<template_id>,
    "json":<template_description_in_JSON>
}
```
The field "json" is only present if the paramenter json=true has been added the the GET request.

##'[0-9]+/?' == '^\<template_id\>/?$'
###GET request
You will get the JSON equivalent to the YAML
describing the template.  
There is no argument for now.
