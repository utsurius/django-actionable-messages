from django.conf import settings
from django.test import TestCase

from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.utils import BaseMixin


class TestTrans(BaseMixin):
    pass


class TestAdaptiveCard(AdaptiveCard):
    def get_signed_payload(self, payload):
        return "signed_payload_ac"

    def get_json_dump_kwargs(self):
        return {
            'indent': 2,
            'allow_nan': False
        }


class TestMessageCard(MessageCard):
    def get_signed_payload(self, payload):
        return "signed_payload_mc"


class UtilsTestCase(TestCase):
    def test_get_language(self):
        self.assertEqual(TestTrans().get_language_code(), settings.LANGUAGE_CODE)

    def test_get_signed_payload(self):
        with self.assertRaises(NotImplementedError):
            AdaptiveCard().get_signed_payload("{}")
        with self.assertRaises(NotImplementedError):
            MessageCard().get_signed_payload("{}")

    def test_signed_html_payload(self):
        signed_html = TestAdaptiveCard().signed_html_payload
        self.assertIn("http://schema.org/SignedAdaptiveCard", signed_html)
        self.assertIn("signed_payload_ac", signed_html)
        signed_html = TestMessageCard().signed_html_payload
        self.assertIn("http://schema.org/SignedMessageCard", signed_html)
        self.assertIn("signed_payload_mc", signed_html)

    def test_get_json_dump_kwargs(self):
        self.assertDictEqual(AdaptiveCard().get_json_dump_kwargs(), {})
        self.assertDictEqual(
            TestAdaptiveCard().get_json_dump_kwargs(),
            {
                'indent': 2,
                'allow_nan': False
            }
        )
