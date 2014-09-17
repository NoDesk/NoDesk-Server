from django import forms
from nodesk_server import settings
import yaml


class TemplateConfigForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(attrs={'class':'', 'required':'true'}))
    name = forms.CharField(
            label='Template name',
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
    visible = forms.BooleanField(
            label='Visible',
            required=False,
            widget=forms.CheckboxInput(attrs={'class':''})
            )

class TemplateFieldForm(forms.Form):
    field_name = forms.CharField(
            label='Field name',
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
    field_type = forms.ChoiceField(
            label='Field type',
            choices=(
                ('TextArea','TextArea'),
                ('TextLine','TextLine'),
                ('Image','Image'),
                ('Sound','Sound'),
                ('Video','Video'),
                ('Coordinates','Coordinates'),
                ('Date','Date'),
                ('Time','Time'),
                ('User','User'),
                ('Creator','Creator'),
                ('Email','Email'),
                ('Phone','Phone'),
                ('Radiobox','Radiobox'),
                ('Checkbox','Checkbox'),
                ('Number','Number'),
                ),
            widget=forms.Select(attrs={'class':'', 'required':'true'})
            )
    field_value = forms.CharField(
            required = False,
            label='Value(s)',
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField'})
            )
    field_options = forms.MultipleChoiceField(
            required = False,
            label='Field options',
            choices=(
                ('left','left'),
                ('right','right'),
                ('center','center'),
                ('required','required'),
                ),
            widget=forms.CheckboxSelectMultiple(attrs={'class':''})
            )
    def toNoDeskYAML(self):
        content = """\
    type : {field_type}
    name : {field_name}
    value : {field_value}
    options : {field_options}"""
        value = self.cleaned_data['field_value']
        if ',' in value : value = '[' + value + ']'
        content = content.format(
                field_type=self.cleaned_data['field_type'],
                field_name=self.cleaned_data['field_name'],
                field_options=yaml.safe_dump(self.cleaned_data['field_options']),
                field_value=value)
        return content

class TemplateSaveForm(forms.Form):
    name = "NoDesk Template Creation"
    template_name = forms.CharField(
            label='Template name',
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
    template_content = forms.CharField(
            label='Template content (YAML)',
            widget=forms.Textarea(attrs={'class':'vLargeTextField', 'required':'true'})
            )

class ConfigLDAPForm(forms.Form):
    name = "LDAP Configuration"
    AUTH_LDAP_SERVER_URI = forms.CharField(
            label='LDAP Server URI',
            initial=settings.AUTH_LDAP_SERVER_URI,
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
    AUTH_LDAP_BIND_DN = forms.CharField(
            label='LDAP Bind DN',
            initial=settings.AUTH_LDAP_BIND_DN,
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
    AUTH_LDAP_BIND_PASSWORD = forms.CharField(
            label='LDAP Bind Password',
            initial=settings.AUTH_LDAP_BIND_PASSWORD,
            max_length=256,
            widget=forms.PasswordInput(render_value = True,attrs={'class':'vLargeTextField', 'required':'true'})
            )
    AUTH_LDAP_USER_SEARCH = forms.CharField(
            label='LDAP User Search',
            initial=settings.AUTH_LDAP_USER_SEARCH.base_dn,
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
#    AUTH_LDAP_USER_SEARCH_FILTER = forms.CharField(
#            label='LDAP User Search Filter',
#            initial=settings.AUTH_LDAP_USER_SEARCH.filterstr,
#            max_length=256,
#            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
#            )
    AUTH_LDAP_GROUP_SEARCH = forms.CharField(
            label='LDAP Groups Search',
            initial=settings.AUTH_LDAP_GROUP_SEARCH.base_dn,
            max_length=256,
            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
            )
#    AUTH_LDAP_GROUP_TYPE = forms.CharField(
#            label='LDAP Group type',
#            initial=settings.AUTH_LDAP_GROUP_TYPE.name_attr,
#            max_length=256,
#            widget=forms.TextInput(attrs={'class':'vLargeTextField', 'required':'true'})
#            )
