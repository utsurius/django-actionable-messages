import json
import uuid

from django.test import TestCase

from django_actionable_messages.message_card.actions import (
    OpenUri, ActionTarget, HttpPOST, Header, InvokeAddInCommand, ActionCard
)
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.message_card.elements import HeroImage, Fact
from django_actionable_messages.message_card.inputs import TextInput
from django_actionable_messages.message_card.sections import Section
from django_actionable_messages.message_card.utils import OSType

URL = "https://www.example.com/"


class MessageCardTestCase(TestCase):
    def assertUUID4(self, value):
        valid = True
        try:
            uuid.UUID(value, version=4)
        except (AttributeError, ValueError):
            valid = False
        self.assertTrue(valid, "{} is not a valid UUID4".format(value))

    def test_message_card(self):
        url1, url2 = "https://www.example.com", "www.sample.com"
        hero_image1, hero_image2 = HeroImage("www.sample.com", "image1"), HeroImage("www.asdf.com", title="image2")
        fact1, fact2 = Fact("Value", "5"), Fact("Name", "lorem")
        action1 = OpenUri("View", targets=[ActionTarget(OSType.ANDROID, "http://www.android.com/"), ])
        action2 = HttpPOST("Send", URL, headers=[Header("Content-Length", 128), ], body="post body",
                           body_content_type="content type")
        action3 = InvokeAddInCommand("Command", "id_cmd", "show", initialization_context={
            "parameter1": 1,
            "parameter2": "blah"
        })
        inputs = [TextInput(input_id="id_text", max_length=128, is_multiline=True, is_required=True), ]
        actions = [OpenUri("Open", targets=[ActionTarget(OSType.WINDOWS, URL), ]), ]
        action4 = ActionCard("Action card", inputs=inputs, actions=actions)
        section1 = Section(title="Section first", activity_image=url1, activity_title="Activity 1",
                           activity_subtitle="activity subtitle", activity_text="asdf", hero_image=hero_image1,
                           facts=[fact1, fact2], actions=[action1, action3])
        section2 = Section(start_group=False, title="Section second", activity_image=url2, activity_title="Activity 2",
                           activity_subtitle="sample subtitle", activity_text="zxcv", hero_image=hero_image2,
                           facts=[fact2, ], actions=[action2, action1, action4])
        correlation_id = str(uuid.uuid4())
        message_card = MessageCard(title="Message card", text="asdf", summary="sample summary", originator="asdf",
                                   theme_color="0faabbff", correlation_id=correlation_id, auto_correlation_id=False,
                                   expected_actors=["a@a.com", "b@b.com"], hide_original_body=True,
                                   sections=[section1, section2], actions=[action1, ])
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "title": "Message card",
            "text": "asdf",
            "summary": "sample summary",
            "themeColor": "0faabbff",
            "correlationId": correlation_id,
            "expectedActors": ["a@a.com", "b@b.com"],
            "hideOriginalBody": True,
            "originator": "asdf",
            "sections": [{
                "title": "Section first",
                "activityImage": url1,
                "activityTitle": "Activity 1",
                "activitySubtitle": "activity subtitle",
                "activityText": "asdf",
                "heroImage": {
                    "image": "www.sample.com",
                    "title": "image1"
                },
                "facts": [
                    {"name": "Value", "value": "5"},
                    {"name": "Name", "value": "lorem"}
                ],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "View",
                    "targets": [
                        {"os": "android", "uri": "http://www.android.com/"}
                    ]
                }, {
                    "@type": "InvokeAddInCommand",
                    "name": "Command",
                    "addInId": "id_cmd",
                    "desktopCommandId": "show",
                    "initializationContext": {
                        "parameter1": 1,
                        "parameter2": "blah"
                    }
                }]
            }, {
                "title": "Section second",
                "activityImage": url2,
                "activityTitle": "Activity 2",
                "activitySubtitle": "sample subtitle",
                "activityText": "zxcv",
                "heroImage": {
                    "image": "www.asdf.com",
                    "title": "image2"
                },
                "facts": [
                    {"name": "Name", "value": "lorem"}
                ],
                "potentialAction": [{
                    "@type": "HttpPOST",
                    "name": "Send",
                    "target": URL,
                    "headers": [
                        {"name": "Content-Length", "value": 128}
                    ],
                    "body": "post body",
                    "bodyContentType": "content type"
                }, {
                    "@type": "OpenUri",
                    "name": "View",
                    "targets": [
                        {"os": "android", "uri": "http://www.android.com/"}
                    ]
                }, {
                    "@type": "ActionCard",
                    "name": "Action card",
                    "inputs": [{
                        "@type": "TextInput",
                        "id": "id_text",
                        "isRequired": True,
                        "isMultiline": True,
                        "maxLength": 128
                    }],
                    "actions": [{
                        "@type": "OpenUri",
                        "name": "Open",
                        "targets": [
                            {"os": "windows", "uri": URL}
                        ]
                    }]
                }]
            }],
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "View",
                "targets": [
                    {"os": "android", "uri": "http://www.android.com/"}
                ]
            }]
        })
        self.assertDictEqual(json.loads(message_card.json_payload), message_card.payload)
        self.assertIn("application/ld+json", message_card.html_payload)

    def test_message_card_auto_correlation_id(self):
        message_card = MessageCard(auto_correlation_id=True)
        payload = message_card.payload
        self.assertListEqual(sorted(list(payload.keys())), sorted(["@context", "@type", "correlationId"]))
        self.assertUUID4(payload["correlationId"])

    def test_message_card_set_title(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_title("Lorem ipsum")
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "title": "Lorem ipsum"
        })

    def test_message_card_set_text(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_text("dolor sit amet")
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "text": "dolor sit amet"
        })

    def test_message_card_set_originator(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_originator("ullamco")
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "originator": "ullamco"
        })

    def test_message_card_set_summary(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_summary("Excepteur sint occaecat cupidatat non proident")
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": "Excepteur sint occaecat cupidatat non proident"
        })

    def test_message_card_set_theme_color(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_theme_color("aabbccff")
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "themeColor": "aabbccff"
        })

    def test_message_card_set_correlation_id(self):
        correlation_id = str(uuid.uuid4())
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_correlation_id(correlation_id)
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "correlationId": correlation_id
        })

    def test_message_card_set_expected_actors(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_expected_actors(["foo@example.com", "bar@example.com"])
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "expectedActors": ["foo@example.com", "bar@example.com"]
        })

    def test_message_card_set_hide_original_body(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.set_hide_original_body()
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "hideOriginalBody": True
        })

    def test_message_card_add_section(self):
        hero_image = HeroImage("www.zxcv.com", title="image2")
        fact1, fact2 = Fact("Value", "normal"), Fact("Lorem", "ipsum")
        action1 = OpenUri("View", targets=[ActionTarget(OSType.ANDROID, "http://www.android.com/"), ])
        action2 = HttpPOST("Send", URL, headers=[Header("Content-Length", 16), ], body="post body",
                           body_content_type="content type")
        section = Section(title="Sample section", activity_image="www.example.com", activity_title="Activity title",
                          activity_subtitle="activity subtitle", activity_text="zxcv", hero_image=hero_image,
                          facts=[fact1, fact2], actions=[action1, action2])
        message_card = MessageCard(auto_correlation_id=False)
        message_card.add_section(section)
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "sections": [{
                "title": "Sample section",
                "activityImage": "www.example.com",
                "activityTitle": "Activity title",
                "activitySubtitle": "activity subtitle",
                "activityText": "zxcv",
                "heroImage": {
                    "image": "www.zxcv.com",
                    "title": "image2"
                },
                "facts": [
                    {"name": "Value", "value": "normal"},
                    {"name": "Lorem", "value": "ipsum"}
                ],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "View",
                    "targets": [
                        {"os": "android", "uri": "http://www.android.com/"}
                    ]
                }, {
                    "@type": "HttpPOST",
                    "name": "Send",
                    "target": URL,
                    "headers": [
                        {"name": "Content-Length", "value": 16}
                    ],
                    "body": "post body",
                    "bodyContentType": "content type"
                }]
            }]
        })

    def test_message_card_add_sections(self):
        hero_image = HeroImage("www.zxcv.com", title="image2")
        fact1, fact2 = Fact("Value", "normal"), Fact("Lorem", "ipsum")
        action1 = OpenUri("View", targets=[ActionTarget(OSType.ANDROID, "http://www.android.com/"), ])
        action2 = HttpPOST("Send", URL, headers=[Header("Content-Length", 16), ], body="post body",
                           body_content_type="content type")
        action3 = OpenUri("Click", targets=[ActionTarget(OSType.DEFAULT, "http://www.example.com/"), ])
        section1 = Section(title="Sample section", activity_image="www.example.com", activity_title="Activity title",
                           activity_subtitle="activity subtitle", activity_text="zxcv", hero_image=hero_image,
                           facts=[fact1, fact2], actions=[action1, action2])
        section2 = Section(title="Section 9", activity_image="www.section.com", activity_title="Activity",
                           activity_subtitle="activity qwer", activity_text="asdf", hero_image=hero_image,
                           facts=[fact1, ], actions=[action3, ])
        message_card = MessageCard(auto_correlation_id=False)
        message_card.add_sections([section1, section2])
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "sections": [{
                "title": "Sample section",
                "activityImage": "www.example.com",
                "activityTitle": "Activity title",
                "activitySubtitle": "activity subtitle",
                "activityText": "zxcv",
                "heroImage": {
                    "image": "www.zxcv.com",
                    "title": "image2"
                },
                "facts": [
                    {"name": "Value", "value": "normal"},
                    {"name": "Lorem", "value": "ipsum"}
                ],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "View",
                    "targets": [
                        {"os": "android", "uri": "http://www.android.com/"}
                    ]
                }, {
                    "@type": "HttpPOST",
                    "name": "Send",
                    "target": URL,
                    "headers": [
                        {"name": "Content-Length", "value": 16}
                    ],
                    "body": "post body",
                    "bodyContentType": "content type"
                }]
            }, {
                "title": "Section 9",
                "activityImage": "www.section.com",
                "activityTitle": "Activity",
                "activitySubtitle": "activity qwer",
                "activityText": "asdf",
                "heroImage": {
                    "image": "www.zxcv.com",
                    "title": "image2"
                },
                "facts": [
                    {"name": "Value", "value": "normal"}
                ],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "Click",
                    "targets": [
                        {"os": "default", "uri": "http://www.example.com/"}
                    ]
                }]
            }]
        })

    def test_message_card_add_action(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.add_action(OpenUri("Click", targets=[ActionTarget(OSType.ANDROID, URL), ]))
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "Click",
                "targets": [
                    {"os": "android", "uri": URL}
                ]
            }]
        })
        message_card.add_action(HttpPOST("Send", URL, headers=[Header("Content-Length", 32), ],
                                         body="Duis aute irure dolor in reprehenderit",
                                         body_content_type="content_type"))
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "Click",
                "targets": [
                    {"os": "android", "uri": URL}
                ]
            }, {
                "@type": "HttpPOST",
                "name": "Send",
                "target": URL,
                "headers": [
                    {"name": "Content-Length", "value": 32}
                ],
                "body": "Duis aute irure dolor in reprehenderit",
                "bodyContentType": "content_type"
            }]
        })

    def test_message_card_add_actions(self):
        message_card = MessageCard(auto_correlation_id=False)
        message_card.add_actions([
            OpenUri("Click", targets=[ActionTarget(OSType.DEFAULT, URL), ]),
            HttpPOST("Post", URL, headers=[Header("Content-Length", 11), ],
                     body="quis nostrud exercitation ullamco", body_content_type="content_type")
        ])
        self.assertDictEqual(message_card.payload, {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "Click",
                "targets": [
                    {"os": "default", "uri": URL}
                ]
            }, {
                "@type": "HttpPOST",
                "name": "Post",
                "target": URL,
                "headers": [
                    {"name": "Content-Length", "value": 11}
                ],
                "body": "quis nostrud exercitation ullamco",
                "bodyContentType": "content_type"
            }]
        })

    def test_assert_uuid(self):
        self.assertUUID4(str(uuid.uuid4()))
        with self.assertRaisesMessage(AssertionError, "invalid is not a valid UUID4"):
            self.assertUUID4("invalid")
