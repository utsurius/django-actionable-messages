from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import OpenUrl, Submit, ShowCard, TargetElement, ToggleVisibility
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.elements import TextBlock
from django_actionable_messages.adaptive_card.outlook.actions import (
    ActionHttp, InvokeAddInCommand, DisplayMessageForm, DisplayAppointmentForm, ToggleVisibility as oToggleVisibility,
    METHODS
)
from django_actionable_messages.adaptive_card.utils import ActionStyle, FallbackOption
from django_actionable_messages.elements import Header
from django_actionable_messages.exceptions import CardException

URL = "https://www.example.com/"


class ActionsTestCase(TestCase):
    def test_fallback_type(self):
        action = Submit(fallback=OpenUrl(URL))
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Submit",
            "fallback": {
                "type": "Action.OpenUrl",
                "url": URL
            }
        })
        action = Submit(fallback=FallbackOption.DROP)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Submit",
            "fallback": "drop"
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            Submit(fallback="invalid")

    def test_open_url(self):
        requires = {
            "parameter1": 1,
            "parameter2": "asdf"
        }
        open_url = OpenUrl(URL, title="View", icon_url="www.asdf.com", style=ActionStyle.POSITIVE,
                           fallback=FallbackOption.DROP, requires=requires)
        self.assertDictEqual(open_url.as_data(), {
            "type": "Action.OpenUrl",
            "url": URL,
            "title": "View",
            "iconUrl": "www.asdf.com",
            "style": "positive",
            "fallback": "drop",
            "requires": requires
        })

    def test_open_url_set_url(self):
        open_url = OpenUrl(URL)
        open_url.set_url("https://www.zxcv.com/1/")
        self.assertDictEqual(open_url.as_data(), {
            "type": "Action.OpenUrl",
            "url": "https://www.zxcv.com/1/"
        })

    def test_show_card(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.add_elements(TextBlock(text="Sample text"))
        adaptive_card.add_actions(Submit(title="Vote"))
        show_card = ShowCard(card=adaptive_card)
        self.assertDictEqual(show_card.as_data(), {
            "type": "Action.ShowCard",
            "card": {
                "type": "AdaptiveCard",
                "body": [{
                    "type": "TextBlock",
                    "text": "Sample text"
                }],
                "actions": [{
                    "type": "Action.Submit",
                    "title": "Vote"
                }]
            }
        })

    def test_show_card_set_card(self):
        show_card = ShowCard()
        self.assertDictEqual(show_card.as_data(), {
            "type": "Action.ShowCard"
        })
        adaptive_card = AdaptiveCard()
        adaptive_card.add_actions(Submit(title="Something"))
        show_card.set_card(adaptive_card)
        self.assertDictEqual(show_card.as_data(), {
            "type": "Action.ShowCard",
            "card": {
                "type": "AdaptiveCard",
                "actions": [{
                    "type": "Action.Submit",
                    "title": "Something"
                }]
            }
        })

    def test_submit(self):
        requires = {
            "parameter1": 1,
            "parameter2": "asdf"
        }
        submit = Submit({"x": 0, "y": 1, "z": "2"}, title="Submit me", icon_url=URL, style=ActionStyle.DESTRUCTIVE,
                        fallback=FallbackOption.DROP, requires=requires)
        self.assertDictEqual(submit.as_data(), {
            "type": "Action.Submit",
            "title": "Submit me",
            "iconUrl": URL,
            "style": "destructive",
            "fallback": "drop",
            "requires": requires,
            "data": {"x": 0, "y": 1, "z": "2"}
        })

    def test_submit_set_data(self):
        submit = Submit()
        data = {
            "name": "John",
            "age": 99,
            "city": "Nowhere"
        }
        submit.set_data(data)
        self.assertDictEqual(submit.as_data(), {
            "type": "Action.Submit",
            "data": data
        })

    def test_target_element1(self):
        target_element = TargetElement("sample_id", True)
        self.assertDictEqual(target_element.as_data(), {
            "elementId": "sample_id",
            "isVisible": True
        })

    def test_target_element2(self):
        target_element = TargetElement("sample_id")
        target_element.set_element_id("element4")
        target_element.set_is_visible(False)
        self.assertDictEqual(target_element.as_data(), {
            "elementId": "element4",
            "isVisible": False
        })

    def test_toggle_visibility(self):
        requires = {
            "parameter1": 1,
            "parameter2": "asdf"
        }
        toggle_visibility = ToggleVisibility(["target1", "target2"], title="Title", icon_url=URL,
                                             style=ActionStyle.DEFAULT, fallback=FallbackOption.DROP, requires=requires)
        self.assertDictEqual(toggle_visibility.as_data(), {
            "type": "Action.ToggleVisibility",
            "title": "Title",
            "iconUrl": URL,
            "style": "default",
            "fallback": "drop",
            "requires": requires,
            "targetElements": ["target1", "target2"]
        })

    def test_toggle_visibility_set_target_elements(self):
        toggle_visibility = ToggleVisibility()
        toggle_visibility.set_target_elements(["asdf", "zxcv", TargetElement(element_id="id_target1", is_visible=True)])
        self.assertDictEqual(toggle_visibility.as_data(), {
            "type": "Action.ToggleVisibility",
            "targetElements": [
                "asdf",
                "zxcv",
                {
                    "elementId": "id_target1",
                    "isVisible": True
                }
            ]
        })

    def test_outlook_action_http_invalid_method(self):
        with self.assertRaisesMessage(CardException, "Invalid method. Available methods are: {}".format(METHODS)):
            ActionHttp(method="invalid", url=URL)

    def test_outlook_action_http_no_body(self):
        with self.assertRaisesMessage(CardException, "If method is POST body must be provided"):
            ActionHttp(method="POST", url=URL)

    def test_outlook_action_http(self):
        action = ActionHttp(method="POST", url=URL, title="Action title", body="asdf", is_visible=False,
                            headers=[
                                Header("Proxy-Authorization", "Basic YWxhZGRpbjpvcGVuc2VzYW1l"),
                                Header("Connection", "close")
                            ])
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "title": "Action title",
                "method": "POST",
                "url": URL,
                "body": "asdf",
                "headers": [{
                    "name": "Proxy-Authorization",
                    "value": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"
                }, {
                    "name": "Connection",
                    "value": "close"
                }],
                "isVisible": False
            }
        )

    def test_outlook_action_http1(self):
        action = ActionHttp(method="POST", url=URL, body="asdf")
        action.add_headers(Header("Transfer-Encoding", "chunked"))
        action.set_title("Action title")
        action.set_body("zxcv")
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "method": "POST",
                "url": URL,
                "headers": [{
                    "name": "Transfer-Encoding",
                    "value": "chunked"
                }],
                "title": "Action title",
                "body": "zxcv"
            }
        )

    def test_outlook_invoke_add_in_command1(self):
        action = InvokeAddInCommand(add_in_id="id_qwerty", desktop_command_id="cmd_id", title="Sample title",
                                    initialization_context={"x": 1234, "y": "no"}, is_visible=True)
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.InvokeAddInCommand",
                "addInId": "id_qwerty",
                "desktopCommandId": "cmd_id",
                "initializationContext": {
                    "x": 1234,
                    "y": "no"
                },
                "title": "Sample title",
                "isVisible": True
            }
        )

    def test_outlook_invoke_add_in_command2(self):
        action = InvokeAddInCommand(add_in_id="id_qwerty", desktop_command_id="cmd_id", title="Sample title",
                                    initialization_context={"x": 1234, "y": "no"}, is_visible=True)
        action.set_add_in_id("id_zxcv")
        action.set_desktop_command_id("cmd_add")
        action.set_initialization_context({"x": 4, "y": 2})
        action.set_title("Command title")
        action.set_is_visible(False)
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.InvokeAddInCommand",
                "addInId": "id_zxcv",
                "desktopCommandId": "cmd_add",
                "initializationContext": {
                    "x": 4,
                    "y": 2
                },
                "title": "Command title",
                "isVisible": False
            }
        )

    def test_outlook_display_message_form1(self):
        action = DisplayMessageForm(title="Title", item_id="item_1")
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.DisplayMessageForm",
                "title": "Title",
                "itemId": "item_1"
            }
        )

    def test_outlook_display_message_form2(self):
        action = DisplayMessageForm()
        action.set_title("Title")
        action.set_item_id("item_2")
        action.set_is_visible(False)
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.DisplayMessageForm",
                "title": "Title",
                "itemId": "item_2",
                "isVisible": False
            }
        )

    def test_outlook_display_appointment_form1(self):
        action = DisplayAppointmentForm(title="Title", item_id="item_1")
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.DisplayAppointmentForm",
                "title": "Title",
                "itemId": "item_1"
            }
        )

    def test_outlook_display_appointment_form2(self):
        action = DisplayAppointmentForm()
        action.set_title("Title")
        action.set_item_id("item_3")
        action.set_is_visible(False)
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.DisplayAppointmentForm",
                "title": "Title",
                "itemId": "item_3",
                "isVisible": False
            }
        )

    def test_outlook_toggle_visibility1(self):
        action = oToggleVisibility(title="Title", target_elements=[
            TargetElement("sample_1", True),
            TargetElement("sample_2", False),
        ])
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.ToggleVisibility",
                "title": "Title",
                "targetElements": [{
                    "elementId": "sample_1",
                    "isVisible": True
                }, {
                    "elementId": "sample_2",
                    "isVisible": False
                }]
            }
        )

    def test_outlook_toggle_visibility2(self):
        action = oToggleVisibility(target_elements=[TargetElement("sample_x", False)])
        action.set_title("Title")
        action.add_target_elements(TargetElement("sample_y"))
        action.set_is_visible(False)
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.ToggleVisibility",
                "title": "Title",
                "targetElements": [{
                    "elementId": "sample_x",
                    "isVisible": False
                }, {
                    "elementId": "sample_y",
                }],
                "isVisible": False
            }
        )
