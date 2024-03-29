import json

from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import OpenUrl, Submit, Execute
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.elements import Image, TextRun
from django_actionable_messages.adaptive_card.types import (
    Refresh, TokenExchangeResource, AuthCardButton, Authentication, Metadata
)
from django_actionable_messages.adaptive_card.utils import (
    VERSIONS, SCHEMA, Style, VerticalAlignment, Color, ActionStyle
)
from django_actionable_messages.exceptions import CardException

URL = "https://www.example.com/"


class CardsTestCase(TestCase):
    def test_adaptive_card(self):
        refresh = Refresh(
            action=Execute(),
            expires="2023-01-01T12:00:00Z",
            user_ids=["user_1", "user_2"]
        )
        authentication = Authentication(
            text="text",
            connection_name="conn_id_1",
            token_exchange_resource=TokenExchangeResource(
                token_id="token_1",
                uri=URL,
                provider_id="provider_id"
            ),
            buttons=[AuthCardButton(
                btn_type="btn_submit",
                value="submit",
                title="sample_title",
                image=URL + "image.bmp"
            )]
        )
        inputs = [
            TextRun(text="Curabitur consequat ac velit sed fermentum.", color=Color.ACCENT),
            Image("www.image.com/image1.jpeg", height="120px")
        ]
        actions = [
            Submit(title="Submit", style=ActionStyle.POSITIVE),
            OpenUrl(URL, title="Click")
        ]
        select_action, image = OpenUrl(URL), Image(URL + "bckg.bmp")
        metadata = Metadata(url="https://www.example.com")
        adaptive_card = AdaptiveCard(version="1.5", schema=SCHEMA, refresh=refresh, authentication=authentication,
                                     inputs=inputs, actions=actions, select_action=select_action, style=Style.GOOD,
                                     hide_original_body=True, fallback_text="Vestibulum sapien.",
                                     background_image=image, metadata=metadata, min_height="150px", lang="en",
                                     speak='<voice name="string">Sample text.</voice>', rtl=True,
                                     vertical_content_alignment=VerticalAlignment.CENTER)
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "version": "1.5",
            "$schema": SCHEMA,
            "refresh": {
                "action": {
                    "type": "Action.Execute"
                },
                "expires": "2023-01-01T12:00:00Z",
                "userIds": ["user_1", "user_2"]
            },
            "authentication": {
                "text": "text",
                "connectionName": "conn_id_1",
                "tokenExchangeResource": {
                    "id": "token_1",
                    "uri": URL,
                    "providerId": "provider_id"
                },
                "buttons": [{
                    "type": "btn_submit",
                    "value": "submit",
                    "title": "sample_title",
                    "image": URL + "image.bmp"
                }]
            },
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": URL
            },
            "style": "good",
            "hideOriginalBody": True,
            "fallbackText": "Vestibulum sapien.",
            "backgroundImage": {
                "type": "Image",
                "url": "https://www.example.com/bckg.bmp"
            },
            "metadata": {
                "webUrl": "https://www.example.com"
            },
            "minHeight": "150px",
            "speak": '<voice name="string">Sample text.</voice>',
            "lang": "en",
            "rtl": True,
            "verticalContentAlignment": "center",
            "body": [{
                "type": "TextRun",
                "text": "Curabitur consequat ac velit sed fermentum.",
                "color": "accent"
            }, {
                "type": "Image",
                "url": "www.image.com/image1.jpeg",
                "height": "120px"
            }],
            "actions": [{
                "type": "Action.Submit",
                "style": "positive",
                "title": "Submit"
            }, {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "Click"
            }]
        })
        self.assertDictEqual(json.loads(adaptive_card.json_payload), adaptive_card.payload)
        self.assertIn("application/adaptivecard+json", adaptive_card.html_payload)

    def test_adaptive_card_set_version(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_version("1.1")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "version": "1.1"
        })
        with self.assertRaisesMessage(CardException, "Invalid version. Supported versions are: {}".format(VERSIONS)):
            adaptive_card.set_version("99.0")

    def test_adaptive_card_set_schema(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_schema("https://www.example.com/schema")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "$schema": "https://www.example.com/schema"
        })

    def test_adaptive_card_set_refresh(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_refresh(Refresh(
            action=Execute(),
            user_ids=["user_1", "user_2"]
        ))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "refresh": {
                "action": {
                    "type": "Action.Execute"
                },
                "userIds": ["user_1", "user_2"]
            }
        })

    def test_adaptive_card_set_authentication(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_authentication(Authentication(
            text="text",
            connection_name="conn_id_1",
            token_exchange_resource=TokenExchangeResource(
                token_id="token_1",
                uri=URL,
                provider_id="provider_id"
            ),
            buttons=[AuthCardButton(
                btn_type="btn_submit",
                value="submit",
                title="sample_title",
                image=URL + "image.bmp"
            )]
        ))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "authentication": {
                "text": "text",
                "connectionName": "conn_id_1",
                "tokenExchangeResource": {
                    "id": "token_1",
                    "uri": URL,
                    "providerId": "provider_id"
                },
                "buttons": [{
                    "type": "btn_submit",
                    "value": "submit",
                    "title": "sample_title",
                    "image": URL + "image.bmp"
                }]
            }
        })

    def test_adaptive_card_set_select_action(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_select_action(OpenUrl(URL, title="Visit"))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "Visit"
            }
        })

    def test_adaptive_card_set_style(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_style(Style.EMPHASIS)
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "style": "emphasis"
        })

    def test_adaptive_card_set_hide_original_body(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_hide_original_body(False)
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "hideOriginalBody": False
        })
        adaptive_card.set_hide_original_body(True)
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "hideOriginalBody": True
        })
        adaptive_card.set_hide_original_body()
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "hideOriginalBody": True
        })

    def test_adaptive_card_set_fallback_text(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_fallback_text("Curabitur sodales ligula in libero.")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "fallbackText": "Curabitur sodales ligula in libero."
        })

    def test_adaptive_card_set_background_image(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_background_image("www.image.com")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "backgroundImage": "www.image.com"
        })
        adaptive_card.set_background_image(Image(URL, alternate_text="Sample image"))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "backgroundImage": {
                "type": "Image",
                "url": URL,
                "altText": "Sample image"
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid image type"):
            adaptive_card.set_background_image(1234)

    def test_adaptive_card_set_metadata(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_metadata(Metadata(url="https://www,example.com"))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "metadata": {
                "webUrl": "https://www,example.com"
            }
        })

    def test_adaptive_card_set_min_height(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_min_height("100px")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "minHeight": "100px"
        })

    def test_adaptive_card_set_speak(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_speak("Class aptent taciti sociosqu ad litora torquent per conubia nostra,")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "speak": "Class aptent taciti sociosqu ad litora torquent per conubia nostra,"
        })

    def test_adaptive_card_set_lang(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_lang("gb")
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "lang": "gb"
        })

    def test_adaptive_card_set_rtl(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_rtl(False)
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "rtl": False
        })

    def test_adaptive_card_set_vertical_content_alignment(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.set_vertical_content_alignment(VerticalAlignment.TOP)
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "verticalContentAlignment": "top"
        })

    def test_adaptive_card_add_elements(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.add_elements([
            Image(URL, alternate_text="elementum"),
            TextRun(text="Mauris vel commodo lorem. Mauris eu ex id sapien viverra elementum", color=Color.DEFAULT),
            Image("www.image.com/image1.jpeg", height="50px")
        ])
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "body": [{
                "type": "Image",
                "url": URL,
                "altText": "elementum"
            }, {
                "type": "TextRun",
                "text": "Mauris vel commodo lorem. Mauris eu ex id sapien viverra elementum",
                "color": "default"
            }, {
                "type": "Image",
                "url": "www.image.com/image1.jpeg",
                "height": "50px"
            }]
        })
        adaptive_card.add_elements(Image("www.image.com", height="24px"))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "body": [{
                "type": "Image",
                "url": URL,
                "altText": "elementum"
            }, {
                "type": "TextRun",
                "text": "Mauris vel commodo lorem. Mauris eu ex id sapien viverra elementum",
                "color": "default"
            }, {
                "type": "Image",
                "url": "www.image.com/image1.jpeg",
                "height": "50px"
            }, {
                "type": "Image",
                "url": "www.image.com",
                "height": "24px"
            }]
        })

    def test_adaptive_card_add_actions(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.add_actions([
            Submit(title="Submit", style=ActionStyle.POSITIVE),
            OpenUrl(URL, title="Click"),
            Submit(title="Post", style=ActionStyle.DEFAULT, icon_url="www.icons.com/1.png")
        ])
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "actions": [{
                "type": "Action.Submit",
                "style": "positive",
                "title": "Submit"
            }, {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "Click"
            }, {
                "type": "Action.Submit",
                "style": "default",
                "title": "Post",
                "iconUrl": "www.icons.com/1.png"
            }]
        })
        adaptive_card.add_actions(OpenUrl(URL, title="Open me please"))
        self.assertDictEqual(adaptive_card.payload, {
            "type": "AdaptiveCard",
            "actions": [{
                "type": "Action.Submit",
                "style": "positive",
                "title": "Submit"
            }, {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "Click"
            }, {
                "type": "Action.Submit",
                "style": "default",
                "title": "Post",
                "iconUrl": "www.icons.com/1.png"
            }, {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "Open me please"
            }]
        })
