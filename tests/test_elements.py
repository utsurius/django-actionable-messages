from django.test import TestCase

from django_actionable_messages.elements import Header


class ElementsTestCase(TestCase):
    def test_header(self):
        header = Header("Accept-Encoding", "gzip,deflate")
        self.assertDictEqual(header.as_data(), {
            "name": "Accept-Encoding",
            "value": "gzip,deflate"
        })
