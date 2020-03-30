from django.test import TestCase

from django_actionable_messages.elements import Header
from django_actionable_messages.exceptions import CardException
from django_actionable_messages.message_card.actions import OpenUri, HttpPOST, InvokeAddInCommand, ActionCard
from django_actionable_messages.message_card.elements import ActionTarget
from django_actionable_messages.message_card.inputs import DateInput, TextInput
from django_actionable_messages.message_card.utils import OSType

URL = "https://www.example.com/"


class ActionsTestCase(TestCase):
    def test_open_uri1(self):
        url1, url2 = "{}first/".format(URL), "{}second/".format(URL)
        action = OpenUri("Open", targets=[ActionTarget(OSType.IOS, url1), ActionTarget(OSType.ANDROID, url2)])
        self.assertDictEqual(action.as_data(), {
            "@type": "OpenUri",
            "name": "Open",
            "targets": [
                {"os": "iOS", "uri": url1},
                {"os": "android", "uri": url2}
            ]
        })

    def test_open_uri2(self):
        url1, url2 = "{}first/".format(URL), "{}second/".format(URL)
        action = OpenUri("View")
        action.set_name("Click")
        action.add_target(ActionTarget(OSType.IOS, url1))
        action.add_targets([ActionTarget(OSType.ANDROID, url2)])
        self.assertDictEqual(action.as_data(), {
            "@type": "OpenUri",
            "name": "Click",
            "targets": [
                {"os": "iOS", "uri": url1},
                {"os": "android", "uri": url2}
            ]
        })

    def test_open_uri_target_already_added(self):
        action = OpenUri("Open", targets=[ActionTarget(OSType.WINDOWS, URL), ])
        with self.assertRaisesMessage(CardException, "Target already set for 'windows'"):
            action.add_target(ActionTarget(OSType.WINDOWS, "https://www.sample.com/"))

    def test_http_post(self):
        action = HttpPOST("Send", URL, headers=[Header("Content-Length", "42"), ], body="qwerty",
                          body_content_type="content_type")
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Send",
            "target": URL,
            "headers": [
                {"name": "Content-Length", "value": "42"}
            ],
            "body": "qwerty",
            "bodyContentType": "content_type"
        })

    def test_http_post_set_name(self):
        action = HttpPOST("Send", URL)
        action.set_name("Praesent")
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Praesent",
            "target": URL
        })

    def test_http_post_set_target(self):
        action = HttpPOST("Send", URL)
        action.set_target("https://www.sample.domain.com")
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Send",
            "target": "https://www.sample.domain.com"
        })

    def test_http_post_add_headers(self):
        action = HttpPOST("Send", URL)
        action.add_headers([Header("Transfer-Encoding", "chunked"), Header("Proxy-Authenticate", "Basic")])
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Send",
            "target": URL,
            "headers": [
                {"name": "Transfer-Encoding", "value": "chunked"},
                {"name": "Proxy-Authenticate", "value": "Basic"},
            ]
        })
        action.add_headers(Header("Trailer", "Expires"))
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Send",
            "target": URL,
            "headers": [
                {"name": "Transfer-Encoding", "value": "chunked"},
                {"name": "Proxy-Authenticate", "value": "Basic"},
                {"name": "Trailer", "value": "Expires"}
            ]
        })

    def test_http_post_set_body(self):
        action = HttpPOST("Post", URL)
        action.set_body("sample body")
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Post",
            "target": URL,
            "body": "sample body"
        })

    def test_http_post_set_body_content_type(self):
        action = HttpPOST("Post", URL)
        action.set_body_content_type("content_type")
        self.assertDictEqual(action.as_data(), {
            "@type": "HttpPOST",
            "name": "Post",
            "target": URL,
            "bodyContentType": "content_type"
        })

    def test_invoke_add_in_command(self):
        action = InvokeAddInCommand("Command", "id1", "show", initialization_context={"property1": True})
        self.assertDictEqual(action.as_data(), {
            "@type": "InvokeAddInCommand",
            "name": "Command",
            "addInId": "id1",
            "desktopCommandId": "show",
            "initializationContext": {
                "property1": True
            }
        })

    def test_invoke_add_in_command_set_name(self):
        action = InvokeAddInCommand("Command", "id1", "show")
        action.set_name("Vestibulum")
        self.assertDictEqual(action.as_data(), {
            "@type": "InvokeAddInCommand",
            "name": "Vestibulum",
            "addInId": "id1",
            "desktopCommandId": "show"
        })

    def test_invoke_add_in_command_set_add_in(self):
        action = InvokeAddInCommand("Command", "id1", "show")
        action.set_add_in_id("id_sample")
        self.assertDictEqual(action.as_data(), {
            "@type": "InvokeAddInCommand",
            "name": "Command",
            "addInId": "id_sample",
            "desktopCommandId": "show"
        })

    def test_invoke_add_in_command_set_desktop_command_id(self):
        action = InvokeAddInCommand("Command", "id1", "show")
        action.set_desktop_command_id("open")
        self.assertDictEqual(action.as_data(), {
            "@type": "InvokeAddInCommand",
            "name": "Command",
            "addInId": "id1",
            "desktopCommandId": "open"
        })

    def test_invoke_add_in_command_set_initialization_context(self):
        action = InvokeAddInCommand("Command", "id2", "open")
        action.set_initialization_context({"property1": "qwerty", "property2": 5})
        self.assertDictEqual(action.as_data(), {
            "@type": "InvokeAddInCommand",
            "name": "Command",
            "addInId": "id2",
            "desktopCommandId": "open",
            "initializationContext": {
                "property1": "qwerty",
                "property2": 5
            }
        })

    def test_action_card(self):
        inputs = [TextInput(input_id="id_text", max_length=128, is_multiline=True, is_required=True), ]
        actions = [OpenUri("Open", targets=[ActionTarget(OSType.DEFAULT, URL), ]), ]
        action_card = ActionCard("Actions", inputs=inputs, actions=actions)
        self.assertDictEqual(action_card.as_data(), {
            "@type": "ActionCard",
            "name": "Actions",
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
                    {"os": "default", "uri": URL}
                ]
            }]
        })

    def test_action_card_set_name(self):
        inputs = [TextInput(input_id="id_text", max_length=128, is_multiline=True), ]
        actions = [OpenUri("Open", targets=[ActionTarget(OSType.DEFAULT, URL), ]), ]
        action_card = ActionCard("Actions", inputs=inputs, actions=actions)
        action_card.set_name("Donec")
        self.assertDictEqual(action_card.as_data(), {
            "@type": "ActionCard",
            "name": "Donec",
            "inputs": [{
                "@type": "TextInput",
                "id": "id_text",
                "isMultiline": True,
                "maxLength": 128
            }],
            "actions": [{
                "@type": "OpenUri",
                "name": "Open",
                "targets": [
                    {"os": "default", "uri": URL}
                ]
            }]
        })

    def test_action_card_add_inputs(self):
        action_card = ActionCard("Inputs")
        action_card.add_inputs([
            DateInput(include_time=True),
            TextInput(input_id="id_text", max_length=16, is_multiline=True)
        ])
        self.assertDictEqual(action_card.as_data(), {
            "@type": "ActionCard",
            "name": "Inputs",
            "inputs": [{
                "@type": "DateInput",
                "includeTime": True
            }, {
                "@type": "TextInput",
                "id": "id_text",
                "isMultiline": True,
                "maxLength": 16
            }]
        })
        action_card.add_inputs(TextInput(max_length=64, is_multiline=True))
        self.assertDictEqual(action_card.as_data(), {
            "@type": "ActionCard",
            "name": "Inputs",
            "inputs": [{
                "@type": "DateInput",
                "includeTime": True
            }, {
                "@type": "TextInput",
                "id": "id_text",
                "isMultiline": True,
                "maxLength": 16
            }, {
                "@type": "TextInput",
                "isMultiline": True,
                "maxLength": 64
            }]
        })

    def test_action_card_add_actions(self):
        action_card = ActionCard("Actions")
        action_card.add_actions([
            OpenUri("Click", targets=[ActionTarget(OSType.IOS, URL)]),
            HttpPOST("Post", URL, headers=[Header("Cache-Control", "no-cache")],
                     body="sample", body_content_type="zxcv")
        ])
        self.assertDictEqual(action_card.as_data(), {
            "@type": "ActionCard",
            "name": "Actions",
            "actions": [{
                "@type": "OpenUri",
                "name": "Click",
                "targets": [
                    {"os": "iOS", "uri": URL}
                ]
            }, {
                "@type": "HttpPOST",
                "name": "Post",
                "target": URL,
                "headers": [
                    {"name": "Cache-Control", "value": "no-cache"}
                ],
                "body": "sample",
                "bodyContentType": "zxcv"
            }]
        })
        action_card.add_actions(OpenUri("View", targets=[ActionTarget(OSType.ANDROID, URL)]))
        self.assertDictEqual(action_card.as_data(), {
            "@type": "ActionCard",
            "name": "Actions",
            "actions": [{
                "@type": "OpenUri",
                "name": "Click",
                "targets": [
                    {"os": "iOS", "uri": URL}
                ]
            }, {
                "@type": "HttpPOST",
                "name": "Post",
                "target": URL,
                "headers": [
                    {"name": "Cache-Control", "value": "no-cache"}
                ],
                "body": "sample",
                "bodyContentType": "zxcv"
            }, {
                "@type": "OpenUri",
                "name": "View",
                "targets": [
                    {"os": "android", "uri": URL}
                ]
            }]
        })
