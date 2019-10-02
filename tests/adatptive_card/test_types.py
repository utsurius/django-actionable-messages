from django.test import TestCase

from django_actionable_messages.adaptive_card.types import BackgroundImage
from django_actionable_messages.adaptive_card.utils import FillMode, HorizontalAlignment, VerticalAlignment

URL = "https://www.example.com/"


class TypesTestCase(TestCase):
    def test_background_image(self):
        background_image = BackgroundImage(URL, FillMode.COVER, HorizontalAlignment.LEFT, VerticalAlignment.BOTTOM)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "fillMode": "cover",
            "horizontalAlignment": "left",
            "verticalAlignment": "bottom"
        })

    def test_background_image_set_url(self):
        background_image = BackgroundImage(URL)
        background_image.set_url("www.zxcv.com")
        self.assertDictEqual(background_image.as_data(), {
            "url": "www.zxcv.com"
        })

    def test_background_image_set_fill_mode(self):
        background_image = BackgroundImage(URL)
        background_image.set_fill_mode(FillMode.REPEAT_VERTICALLY)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "fillMode": "repeatVertically"
        })

    def test_background_image_set_horizontal_alignment(self):
        background_image = BackgroundImage(URL)
        background_image.set_horizontal_alignment(HorizontalAlignment.CENTER)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "horizontalAlignment": "center"
        })

    def test_background_image_set_vertical_alignment(self):
        background_image = BackgroundImage(URL)
        background_image.set_vertical_alignment(VerticalAlignment.TOP)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "verticalAlignment": "top"
        })
