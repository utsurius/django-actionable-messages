from django.conf import settings
from django.test import TestCase

from django_actionable_messages.utils import BaseMixin


class TestTrans(BaseMixin):
    pass


class TranslationsTestCase(TestCase):
    def test_get_language(self):
        self.assertEqual(TestTrans().get_language_code(), settings.LANGUAGE_CODE)
