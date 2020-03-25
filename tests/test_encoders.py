import json
import uuid

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from django_actionable_messages.encoders import BaseEncoder


class BaseEncoderTestCase(TestCase):
    def test_base_encoder_promise(self):
        data = json.loads(json.dumps({"text": _("test string")}, cls=BaseEncoder, lang_code='en'))
        self.assertEqual(data["text"], "test string")

    def test_base_encoder_uuid(self):
        value = uuid.uuid4()
        data = json.loads(json.dumps({"uuid": value}, cls=BaseEncoder))
        self.assertEqual(data["uuid"], str(value))
