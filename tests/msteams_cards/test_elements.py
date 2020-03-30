from django.test import TestCase

from django_actionable_messages.msteams_cards.elements import OpenUrl, Image


class ActionsTestCase(TestCase):
    def test_open_url_action(self):
        action = OpenUrl(title="View", url="https://www.example.com/")
        self.assertDictEqual(action.as_data(), {
            "type": "openUrl",
            "title": "View",
            "value": "https://www.example.com/"
        })

    def test_image1(self):
        image = Image("https://www.example.com/", alt="no_image")
        self.assertDictEqual(image.as_data(), {
            "url": "https://www.example.com/",
            "alt": "no_image"
        })

    def test_image2(self):
        image = Image("https://www.example.com/")
        image.set_alt("no-image")
        self.assertDictEqual(image.as_data(), {
            "url": "https://www.example.com/",
            "alt": "no-image"
        })
