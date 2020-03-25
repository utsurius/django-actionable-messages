from json import JSONEncoder

from django.conf import settings
from django.test import TestCase, override_settings

from django_actionable_messages.encoders import BaseEncoder
from django_actionable_messages.settings import CardSettings, card_settings


class CustomJSONEncoder(JSONEncoder):
    pass


class SettingsTestCase(TestCase):
    def test_reload_settings(self):
        self.assertEqual(card_settings.JSON_ENCODER, BaseEncoder)
        self.assertEqual(card_settings.LANGUAGE_CODE, settings.LANGUAGE_CODE)
        with override_settings(ACTIONABLE_MESSAGES={
            "JSON_ENCODER": CustomJSONEncoder,
            "LANGUAGE_CODE": "us"
        }):
            self.assertEqual(card_settings.JSON_ENCODER, CustomJSONEncoder)
            self.assertEqual(card_settings.LANGUAGE_CODE, "us")

    @override_settings(ACTIONABLE_MESSAGES={"JSON_ENCODER": "invalid"})
    def test_invalid_encoder_path(self):
        with self.assertRaises(ImportError):
            self.assertIsNone(card_settings.JSON_ENCODER)

    def test_invalid_setting(self):
        with self.assertRaisesMessage(AttributeError, "Invalid setting: 'INVALID_SETTING'"):
            card_test_settings = CardSettings()
            self.assertIsNone(card_test_settings.INVALID_SETTING)

    @override_settings(ACTIONABLE_MESSAGES={"JSON_ENCODER": None})
    def test_null_setting(self):
        self.assertIsNone(card_settings.JSON_ENCODER)
