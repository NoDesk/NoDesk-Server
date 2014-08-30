from nodesk_template import model_manager
import nodesk_template.models
from django.core.management import call_command

model_manager.sync_model("./nodesk_template/template_yaml")
