from json import JSONEncoder

from django.test import TestCase, override_settings

from django_actionable_messages.settings import CardSettings, card_settings


class CustomJSONEncoder(JSONEncoder):
    pass


class SettingsTestCase(TestCase):
    def test_reload_settings(self):
        self.assertIsNone(card_settings.JSON_ENCODER)
        with override_settings(ACTIONABLE_MESSAGES={"JSON_ENCODER": CustomJSONEncoder}):
            self.assertEqual(card_settings.JSON_ENCODER, CustomJSONEncoder)
        self.assertIsNone(card_settings.JSON_ENCODER)

    @override_settings(ACTIONABLE_MESSAGES={"JSON_ENCODER": "invalid"})
    def test_invalid_encoder_path(self):
        with self.assertRaises(ImportError):
            self.assertIsNone(card_settings.JSON_ENCODER)

    def test_invalid_setting(self):
        with self.assertRaisesMessage(AttributeError, "Invalid setting: 'INVALID_SETTING'"):
            settings = CardSettings()
            self.assertIsNone(settings.INVALID_SETTING)
