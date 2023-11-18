from django.test import TestCase

from django_actionable_messages.message_card.elements import Fact, HeroImage, InputChoice, ActionTarget
from django_actionable_messages.message_card.utils import OSType

URL = "https://www.example.com/"


class HelpersTestCase(TestCase):
    def test_fact(self):
        fact = Fact("First name", "Gal Anonim")
        self.assertDictEqual(fact.as_data(), {
            "name": "First name",
            "value": "Gal Anonim"
        })

    def test_hero_image(self):
        url = "{}image2.jpeg".format(URL)
        hero_image = HeroImage(url, title="Sample image")
        self.assertDictEqual(hero_image.as_data(), {
            "image": url,
            "title": "Sample image"
        })

    def test_hero_image_set_title(self):
        url = "{}image.jpeg".format(URL)
        hero_image = HeroImage(url)
        hero_image.set_title("Curabitur")
        self.assertDictEqual(hero_image.as_data(), {
            "image": url,
            "title": "Curabitur"
        })

    def test_input_choice(self):
        input_choice = InputChoice("Choice 1", "1")
        self.assertDictEqual(input_choice.as_data(), {
            "display": "Choice 1",
            "value": "1"
        })

    def test_input_choice_get_value(self):
        input_choice = InputChoice("Choice 1", "12")
        self.assertEqual(input_choice._get_value(), "12")

    def test_action_target(self):
        action_target = ActionTarget(OSType.WINDOWS, URL)
        self.assertDictEqual(action_target.as_data(), {
            "os": "windows",
            "uri": URL
        })

    def test_action_target_get_os(self):
        action_target = ActionTarget(OSType.ANDROID, URL)
        self.assertEqual(action_target._get_os(), "android")
