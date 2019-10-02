from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import OpenUrl, Submit, ShowCard, TargetElement, ToggleVisibility
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.elements import TextBlock
from django_actionable_messages.adaptive_card.utils import ActionStyle, FallbackOption
from django_actionable_messages.utils import CardException

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
        adaptive_card.add_element(TextBlock(text="Sample text"))
        adaptive_card.add_action(Submit(title="Vote"))
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
        adaptive_card.add_action(Submit(title="Something"))
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

    def test_target_element(self):
        target_element = TargetElement("sample_id", True)
        self.assertDictEqual(target_element.as_data(), {
            "elementId": "sample_id",
            "isVisible": True
        })

    def test_target_element_set_element_id(self):
        target_element = TargetElement("sample_id", True)
        target_element.set_element_id("asdf")
        self.assertDictEqual(target_element.as_data(), {
            "elementId": "asdf",
            "isVisible": True
        })

    def test_target_element_set_is_visible(self):
        target_element = TargetElement("sample_id")
        target_element.set_is_visible(False)
        self.assertDictEqual(target_element.as_data(), {
            "elementId": "sample_id",
            "isVisible": False
        })
        target_element.set_is_visible()
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
        with self.assertRaisesMessage(CardException, "Invalid target element type"):
            toggle_visibility.set_target_elements([1234, ])
