from nodesk_templates import field_types
from nodesk_template.constants import INDENTATION

from django.test import TestCase

import yaml


class FieldTypeTestCase(TestCase):
    def setUp(self):
        with open('data/template_test.yaml', 'r') as template:
            self.template = yaml.load(template)

    def test_textarea(self):
        textarea = self.template[0]
        func = field_types.field_types_dict.get(textarea['type'], None)
        self.assertFalse(func is None)
        self.assertEqual(func(textarea['value']),
                         INDENTATION + 'models.TextField(default=%s)' % textarea['field'])

