from django.test import TestCase

from django_actionable_messages.msteams_cards.cards import HeroCard, ThumbnailCard
from django_actionable_messages.msteams_cards.elements import OpenUrl, Image

URL1 = "https://www.example.com/1/"
URL2 = "https://www.example.com/2/"


class MsTeamsTestCase(TestCase):
    def test_hero_card1(self):
        card = HeroCard(
            title="Hero title", subtitle="test", text="lorem ipsum", images=[Image(URL1), Image(URL2)],
            buttons=[OpenUrl(title="View", url=URL1), OpenUrl(title="Click", url=URL2)]
        )
        self.assertDictEqual(card.payload, {
            "contentType": "application/vnd.microsoft.card.hero",
            "content": {
                "title": "Hero title",
                "subtitle": "test",
                "text": "lorem ipsum",
                "images": [{
                    "url": URL1
                }, {
                    "url": URL2
                }],
                "buttons": [{
                    "type": "openUrl",
                    "title": "View",
                    "value": URL1
                }, {
                    "type": "openUrl",
                    "title": "Click",
                    "value": URL2
                }]
            }
        })

    def test_hero_card2(self):
        card = HeroCard()
        card.set_title("Hero card")
        card.set_subtitle("Subtitle")
        card.set_text("Text")
        card.add_images([Image(URL1)])
        card.add_images(Image(URL2))
        card.add_buttons([OpenUrl(title="View", url=URL1)])
        card.add_buttons(OpenUrl(title="Click", url=URL2))
        self.assertDictEqual(card.payload, {
            "contentType": "application/vnd.microsoft.card.hero",
            "content": {
                "title": "Hero card",
                "subtitle": "Subtitle",
                "text": "Text",
                "images": [{
                    "url": URL1
                }, {
                    "url": URL2
                }],
                "buttons": [{
                    "type": "openUrl",
                    "title": "View",
                    "value": URL1
                }, {
                    "type": "openUrl",
                    "title": "Click",
                    "value": URL2
                }]
            }
        })

    def test_thumbnail_card1(self):
        card = ThumbnailCard(
            title="Thumbnail title", subtitle="smalll", text="lorem ipsum", images=[Image(URL1), Image(URL2)],
            buttons=[OpenUrl(title="View", url=URL1), OpenUrl(title="Open", url=URL2)]
        )
        self.assertDictEqual(card.payload, {
            "contentType": "application/vnd.microsoft.card.thumbnail",
            "content": {
                "title": "Thumbnail title",
                "subtitle": "smalll",
                "text": "lorem ipsum",
                "images": [{
                    "url": URL1
                }, {
                    "url": URL2
                }],
                "buttons": [{
                    "type": "openUrl",
                    "title": "View",
                    "value": URL1
                }, {
                    "type": "openUrl",
                    "title": "Open",
                    "value": URL2
                }]
            }
        })

    def test_thumbnail_card2(self):
        card = ThumbnailCard()
        card.set_title("Thumbnail card")
        card.set_subtitle("subtitle")
        card.set_text("text")
        card.add_images([Image(URL1)])
        card.add_images(Image(URL2))
        card.add_buttons([OpenUrl(title="View", url=URL1)])
        card.add_buttons(OpenUrl(title="Click", url=URL2))
        self.assertDictEqual(card.payload, {
            "contentType": "application/vnd.microsoft.card.thumbnail",
            "content": {
                "title": "Thumbnail card",
                "subtitle": "subtitle",
                "text": "text",
                "images": [{
                    "url": URL1
                }, {
                    "url": URL2
                }],
                "buttons": [{
                    "type": "openUrl",
                    "title": "View",
                    "value": URL1
                }, {
                    "type": "openUrl",
                    "title": "Click",
                    "value": URL2
                }]
            }
        })
