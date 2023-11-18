from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import (
    OpenUrl, Submit, ShowCard, TargetElement, ToggleVisibility, Execute
)
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.elements import TextBlock, Image
from django_actionable_messages.adaptive_card.outlook.actions import (
    METHODS, ActionHttp, InvokeAddInCommand, DisplayMessageForm, DisplayAppointmentForm,
    ToggleVisibility as oToggleVisibility
)
from django_actionable_messages.adaptive_card.utils import ActionStyle, FallbackOption, AssociatedInputs, ActionMode
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
        open_url = OpenUrl(URL, title="View", icon_url="www.asdf.com", style=ActionStyle.POSITIVE, is_enabled=True,
                           mode=ActionMode.PRIMARY, tooltip="Phasellus sodales leo", fallback=FallbackOption.DROP,
                           requires=requires)
        self.assertDictEqual(open_url.as_data(), {
            "type": "Action.OpenUrl",
            "url": URL,
            "title": "View",
            "iconUrl": "www.asdf.com",
            "style": "positive",
            "fallback": "drop",
            "mode": "primary",
            "isEnabled": True,
            "tooltip": "Phasellus sodales leo",
            "requires": requires
        })

    def test_open_url_set_tooltip(self):
        action = OpenUrl(URL)
        action.set_tooltip("Vivamus ornare elit")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.OpenUrl",
            "url": URL,
            "tooltip": "Vivamus ornare elit"
        })

    def test_open_url_set_is_enabled(self):
        action = OpenUrl(URL)
        action.set_is_enabled(False)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.OpenUrl",
            "url": URL,
            "isEnabled": False
        })

    def test_open_url_set_mode(self):
        action = OpenUrl(URL)
        action.set_mode(ActionMode.SECONDARY)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.OpenUrl",
            "url": URL,
            "mode": "secondary"
        })

    def test_show_card(self):
        adaptive_card = AdaptiveCard()
        adaptive_card.add_elements(TextBlock(text="Sample text"))
        adaptive_card.add_actions(Submit(title="Vote"))
        show_card = ShowCard(card=adaptive_card, tooltip="Etiam venenatis", is_enabled=True, mode=ActionMode.PRIMARY)
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
            },
            "tooltip": "Etiam venenatis",
            "mode": "primary",
            "isEnabled": True
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

    def test_show_card_set_tooltip(self):
        show_card = ShowCard()
        show_card.set_tooltip("Ligula malesuada")
        self.assertDictEqual(show_card.as_data(), {
            "type": "Action.ShowCard",
            "tooltip": "Ligula malesuada"
        })

    def test_show_card_set_is_enabled(self):
        show_card = ShowCard()
        show_card.set_is_enabled(False)
        self.assertDictEqual(show_card.as_data(), {
            "type": "Action.ShowCard",
            "isEnabled": False
        })

    def test_show_card_set_mode(self):
        show_card = ShowCard()
        show_card.set_mode(ActionMode.SECONDARY)
        self.assertDictEqual(show_card.as_data(), {
            "type": "Action.ShowCard",
            "mode": "secondary"
        })

    def test_submit(self):
        requires = {
            "parameter1": 1,
            "parameter2": "asdf"
        }
        submit = Submit({"x": 0, "y": 1, "z": "2"}, title="Submit me", icon_url=URL, style=ActionStyle.DESTRUCTIVE,
                        fallback=FallbackOption.DROP, tooltip="Morbi felis arcu", is_enabled=True,
                        mode=ActionMode.SECONDARY, requires=requires)
        self.assertDictEqual(submit.as_data(), {
            "type": "Action.Submit",
            "title": "Submit me",
            "iconUrl": URL,
            "style": "destructive",
            "fallback": "drop",
            "requires": requires,
            "data": {"x": 0, "y": 1, "z": "2"},
            "tooltip": "Morbi felis arcu",
            "mode": "secondary",
            "isEnabled": True
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

    def test_submit_set_tooltip(self):
        action = Submit()
        action.set_tooltip("Volutpat nec pharetra")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Submit",
            "tooltip": "Volutpat nec pharetra"
        })

    def test_submit_set_is_enabled(self):
        action = Submit()
        action.set_is_enabled(False)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Submit",
            "isEnabled": False
        })

    def test_submit_set_mode(self):
        action = Submit()
        action.set_mode(ActionMode.SECONDARY)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Submit",
            "mode": "secondary"
        })

    def test_target_element(self):
        target_element = TargetElement("sample_id", True)
        self.assertDictEqual(target_element.as_data(), {
            "elementId": "sample_id",
            "isVisible": True
        })

    def test_toggle_visibility(self):
        requires = {
            "parameter1": 1,
            "parameter2": "asdf"
        }
        toggle_visibility = ToggleVisibility(["target1", "target2"], title="Title", icon_url=URL,
                                             style=ActionStyle.DEFAULT, fallback=FallbackOption.DROP, is_enabled=True,
                                             tooltip="Faucibus orci luctus", mode=ActionMode.PRIMARY, requires=requires)
        self.assertDictEqual(toggle_visibility.as_data(), {
            "type": "Action.ToggleVisibility",
            "title": "Title",
            "iconUrl": URL,
            "style": "default",
            "fallback": "drop",
            "requires": requires,
            "targetElements": ["target1", "target2"],
            "tooltip": "Faucibus orci luctus",
            "mode": "primary",
            "isEnabled": True
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

    def test_toggle_visibility_set_target_elements_invalid_type(self):
        toggle_visibility = ToggleVisibility()
        with self.assertRaises(CardException):
            toggle_visibility.set_target_elements([1])

    def test_toggle_visibility_set_tooltip(self):
        toggle_visibility = ToggleVisibility()
        toggle_visibility.set_tooltip("Vestibulum ante ipsum")
        self.assertDictEqual(toggle_visibility.as_data(), {
            "type": "Action.ToggleVisibility",
            "tooltip": "Vestibulum ante ipsum"
        })

    def test_toggle_visibility_set_is_enabled(self):
        toggle_visibility = ToggleVisibility()
        toggle_visibility.set_is_enabled(False)
        self.assertDictEqual(toggle_visibility.as_data(), {
            "type": "Action.ToggleVisibility",
            "isEnabled": False
        })

    def test_toggle_visibility_set_mode(self):
        toggle_visibility = ToggleVisibility()
        toggle_visibility.set_mode(ActionMode.SECONDARY)
        self.assertDictEqual(toggle_visibility.as_data(), {
            "type": "Action.ToggleVisibility",
            "mode": "secondary"
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

    def test_outlook_action_http_minimal(self):
        action = ActionHttp(method="GET", url=URL)
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "method": "GET",
                "url": URL
            }
        )

    def test_outlook_action_http_set_title(self):
        action = ActionHttp(method="GET", url=URL)
        action.set_title("Praesent a consectetur")
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "method": "GET",
                "url": URL,
                "title": "Praesent a consectetur"
            }
        )

    def test_outlook_action_http_add_headers_as_list(self):
        action = ActionHttp(method="GET", url=URL)
        action.add_headers([
            Header("Proxy-Authorization", "Basic YWxhZGRpbjpvcGVuc2VzYW1l"),
            Header("Connection", "close")
        ])
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "method": "GET",
                "url": URL,
                "headers": [{
                    "name": "Proxy-Authorization",
                    "value": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"
                }, {
                    "name": "Connection",
                    "value": "close"
                }]
            }
        )

    def test_outlook_action_http_add_headers_object(self):
        action = ActionHttp(method="GET", url=URL)
        action.add_headers(Header("Connection", "close"))
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "method": "GET",
                "url": URL,
                "headers": [{
                    "name": "Connection",
                    "value": "close"
                }]
            }
        )

    def test_outlook_action_http_set_body(self):
        action = ActionHttp(method="GET", url=URL)
        action.set_body("bar")
        self.assertDictEqual(
            action.as_data(),
            {
                "type": "Action.Http",
                "method": "GET",
                "url": URL,
                "body": "bar"
            }
        )

    def test_outlook_invoke_add_in_command_minimal(self):
        action = InvokeAddInCommand(add_in_id="id_qwerty", desktop_command_id="cmd_id",
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
                "isVisible": True
            }
        )

    def test_outlook_invoke_add_in_command(self):
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

    def test_execute(self):
        action = Execute(verb="verb", data="data", associated_inputs=AssociatedInputs.AUTO, title="title",
                         icon_url=URL + "image.bmp", style=ActionStyle.DESTRUCTIVE, fallback=FallbackOption.DROP,
                         tooltip="Fusce eget rutrum", is_enabled=True, mode=ActionMode.PRIMARY, requires={"foo": "bar"})
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "verb": "verb",
            "data": "data",
            "associatedInputs": "Auto",
            "title": "title",
            "iconUrl": URL + "image.bmp",
            "style": "destructive",
            "fallback": "drop",
            "tooltip": "Fusce eget rutrum",
            "isEnabled": True,
            "mode": "primary",
            "requires": {
                "foo": "bar"
            }
        })

    def test_execute_empty(self):
        action = Execute()
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute"
        })

    def test_execute_set_verb(self):
        action = Execute()
        action.set_verb("foo")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "verb": "foo"
        })

    def test_execute_set_data(self):
        action = Execute()
        action.set_data("foo")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "data": "foo"
        })

    def test_execute_set_associated_inputs(self):
        action = Execute()
        action.set_associated_inputs(AssociatedInputs.NONE)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "associatedInputs": "None"
        })

    def test_execute_set_title(self):
        action = Execute()
        action.set_title("foo")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "title": "foo"
        })

    def test_execute_set_icon_url(self):
        action = Execute()
        action.set_icon_url(URL + "image.bmp")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "iconUrl": URL + "image.bmp"
        })

    def test_execute_set_style(self):
        action = Execute()
        action.set_style(ActionStyle.POSITIVE)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "style": "positive"
        })

    def test_execute_set_set_fallback_fallback_option(self):
        action = Execute()
        action.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "fallback": "drop"
        })

    def test_execute_set_set_fallback_element_type(self):
        action = Execute()
        action.set_fallback(Image(URL))
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })

    def test_execute_set_set_fallback_invalid_type(self):
        action = Execute()
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            action.set_fallback(1)

    def test_execute_set_tooltip(self):
        action = Execute()
        action.set_tooltip("Maecenas consequat")
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "tooltip": "Maecenas consequat"
        })

    def test_execute_set_is_enabled(self):
        action = Execute()
        action.set_is_enabled(False)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "isEnabled": False
        })

    def test_execute_set_mode(self):
        action = Execute()
        action.set_mode(ActionMode.SECONDARY)
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "mode": "secondary"
        })

    def test_execute_set_requires(self):
        action = Execute()
        action.set_requires({
            "foo": "bar"
        })
        self.assertDictEqual(action.as_data(), {
            "type": "Action.Execute",
            "requires": {
                "foo": "bar"
            }
        })
