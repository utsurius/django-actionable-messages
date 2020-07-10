from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import Submit, OpenUrl
from django_actionable_messages.adaptive_card.elements import TextBlock, Image, RichTextBlock
from django_actionable_messages.adaptive_card.inputs import (
    TextInput, NumberInput, DateInput, TimeInput, ToggleInput, InputChoice, ChoiceSetInput
)
from django_actionable_messages.adaptive_card.utils import (
    ChoiceInputStyle, FallbackOption, SpacingStyle, TextInputStyle
)
from django_actionable_messages.exceptions import CardException

URL = "https://www.example.com/"


class InputsTestCase(TestCase):
    requires = {
        "parameter1": "foo",
        "parameter2": "bar",
        "parameter3": 1337
    }

    def test_input_text(self):
        inline_action = Submit(title="Submit", icon_url="http://www.example.com/1.png")
        input_text = TextInput(is_multiline=True, max_length=128, placeholder="Morbi in ipsum sit amet pede facilisis",
                               style=TextInputStyle.EMAIL, inline_action=inline_action, label="Curabitur convallis",
                               value="Class aptent taciti sociosqu ad", fallback=FallbackOption.DROP, separator=True,
                               spacing=SpacingStyle.SMALL, item_id="id_text", is_visible=True, requires=self.requires)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "isMultiline": True,
            "maxLength": 128,
            "style": "email",
            "inlineAction": {
                "type": "Action.Submit",
                "iconUrl": "http://www.example.com/1.png",
                "title": "Submit"
            },
            "value": "Class aptent taciti sociosqu ad",
            "placeholder": "Morbi in ipsum sit amet pede facilisis",
            "fallback": "drop",
            "separator": True,
            "spacing": "small",
            "id": "id_text",
            "isVisible": True,
            "requires": self.requires,
            "label": "Curabitur convallis"
        })

    def test_input_text_set_is_multiline(self):
        input_text = TextInput()
        input_text.set_is_multiline(False)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "isMultiline": False
        })
        input_text.set_is_multiline(True)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "isMultiline": True
        })
        input_text.set_is_multiline()
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "isMultiline": True
        })

    def test_input_text_set_max_length(self):
        input_text = TextInput()
        input_text.set_max_length(12345)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "maxLength": 12345
        })

    def test_input_text_set_placeholder(self):
        input_text = TextInput()
        input_text.set_placeholder("Integer euismod lacus luctus magna")
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "placeholder": "Integer euismod lacus luctus magna"
        })

    def test_input_text_set_style(self):
        input_text = TextInput()
        input_text.set_style(TextInputStyle.URL)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "style": "url"
        })

    def test_input_text_set_inline_action(self):
        input_text = TextInput()
        action = OpenUrl(URL, title="Click me")
        input_text.set_inline_action(action)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "inlineAction": {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "Click me"
            }
        })

    def test_input_text_set_value(self):
        input_text = TextInput()
        input_text.set_value("Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.")
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "value": "Curabitur sodales ligula in libero. Sed dignissim lacinia nunc."
        })

    def test_input_text_set_fallback(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "fallback": "drop"
        })
        input_text.set_fallback(Image(URL))
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            input_text.set_fallback(1234)

    def test_input_text_set_separator(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_separator(False)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "separator": False
        })
        input_text.set_separator(True)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "separator": True
        })
        input_text.set_separator()
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "separator": True
        })

    def test_input_text_set_spacing(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "spacing": "extraLarge"
        })

    def test_input_text_set_id(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_id("id_mnbv")
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_mnbv"
        })

    def test_input_text_set_is_visible(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_is_visible(False)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "isVisible": False
        })
        input_text.set_is_visible(True)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "isVisible": True
        })
        input_text.set_is_visible()
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "isVisible": True
        })

    def test_input_text_set_requires(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_requires(self.requires)
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "requires": self.requires
        })

    def test_input_text_set_label(self):
        input_text = TextInput(item_id="id_text")
        input_text.set_label("Cras id nibh")
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "label": "Cras id nibh"
        })
        input_text.set_label(TextBlock("Proin volutpat semper elit"))
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "label": {
                "type": "TextBlock",
                "text": "Proin volutpat semper elit"
            }
        })
        input_text.set_label(RichTextBlock(inlines=["Quisque porta placerat tristique", ]))
        self.assertDictEqual(input_text.as_data(), {
            "type": "Input.Text",
            "id": "id_text",
            "label": {
                "type": "RichTextBlock",
                "inlines": ["Quisque porta placerat tristique", ]
            }
        })

    def test_input_number(self):
        input_number = NumberInput(max_value=100, min_value=10, placeholder="Maecenas mattis", value=42,
                                   fallback=FallbackOption.DROP, separator=True, spacing=SpacingStyle.PADDING,
                                   item_id="id_number", is_visible=True, requires=self.requires, label="nisi felis")
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "max": 100,
            "min": 10,
            "placeholder": "Maecenas mattis",
            "value": 42,
            "fallback": "drop",
            "separator": True,
            "spacing": "padding",
            "id": "id_number",
            "isVisible": True,
            "requires": self.requires,
            "label": "nisi felis"
        })

    def test_input_number_set_max(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_max(64)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "max": 64
        })

    def test_input_number_set_min(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_min(0)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "min": 0
        })

    def test_input_number_set_placeholder(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_placeholder("Enter a number")
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "placeholder": "Enter a number"
        })

    def test_input_number_set_value(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_value(12589)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "value": 12589
        })

    def test_input_number_set_fallback(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "fallback": "drop"
        })
        input_number.set_fallback(Image(URL))
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            input_number.set_fallback(1234)

    def test_input_number_set_separator(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_separator(False)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "separator": False
        })
        input_number.set_separator(True)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "separator": True
        })
        input_number.set_separator()
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "separator": True
        })

    def test_input_number_set_spacing(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "spacing": "extraLarge"
        })

    def test_input_number_set_id(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_id("id_qwer")
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_qwer"
        })

    def test_input_number_set_is_visible(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_is_visible(False)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "isVisible": False
        })
        input_number.set_is_visible(True)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "isVisible": True
        })
        input_number.set_is_visible()
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "isVisible": True
        })

    def test_input_number_set_requires(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_requires(self.requires)
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "requires": self.requires
        })

    def test_input_number_set_label(self):
        input_number = NumberInput(item_id="id_number")
        input_number.set_label("Proin volutpat")
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "label": "Proin volutpat"
        })
        input_number.set_label(TextBlock("Cras in tortor sed"))
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "label": {
                "type": "TextBlock",
                "text": "Cras in tortor sed"
            }
        })
        input_number.set_label(RichTextBlock(inlines=["dui vulputate dignissim", ]))
        self.assertDictEqual(input_number.as_data(), {
            "type": "Input.Number",
            "id": "id_number",
            "label": {
                "type": "RichTextBlock",
                "inlines": ["dui vulputate dignissim", ]
            }
        })

    def test_input_date(self):
        input_date = DateInput(max_value="2020-10-25", min_value="2015-04-19", placeholder="Ne quo causae",
                               value="2017-11-01", fallback=FallbackOption.DROP, separator=True, label="Praesent",
                               spacing=SpacingStyle.MEDIUM, item_id="id_date", is_visible=True, requires=self.requires)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "max": "2020-10-25",
            "min": "2015-04-19",
            "placeholder": "Ne quo causae",
            "value": "2017-11-01",
            "fallback": "drop",
            "separator": True,
            "spacing": "medium",
            "id": "id_date",
            "isVisible": True,
            "requires": self.requires,
            "label": "Praesent"
        })

    def test_input_date_set_max(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_max("2020-09-26")
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "max": "2020-09-26"
        })

    def test_input_date_set_min(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_min("2010-01-15")
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "min": "2010-01-15"
        })

    def test_input_date_set_placeholder(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_placeholder("Enter a date")
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "placeholder": "Enter a date"
        })

    def test_input_date_set_value(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_value("2019-05-27")
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "value": "2019-05-27"
        })

    def test_input_date_set_fallback(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "fallback": "drop"
        })
        input_date.set_fallback(Image(URL))
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            input_date.set_fallback(1234)

    def test_input_date_set_separator(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_separator(False)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "separator": False
        })
        input_date.set_separator(True)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "separator": True
        })
        input_date.set_separator()
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "separator": True
        })

    def test_input_date_set_spacing(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_spacing(SpacingStyle.LARGE)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "spacing": "large"
        })

    def test_input_date_set_id(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_id("id_zxcv")
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_zxcv"
        })

    def test_input_date_set_is_visible(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_is_visible(False)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "isVisible": False
        })
        input_date.set_is_visible(True)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "isVisible": True
        })
        input_date.set_is_visible()
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "isVisible": True
        })

    def test_input_date_set_requires(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_requires(self.requires)
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "requires": self.requires
        })

    def test_input_date_set_label(self):
        input_date = DateInput(item_id="id_date")
        input_date.set_label("Etiam sed")
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "label": "Etiam sed"
        })
        input_date.set_label(TextBlock("ultricies leo"))
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "label": {
                "type": "TextBlock",
                "text": "ultricies leo"
            }
        })
        input_date.set_label(RichTextBlock(inlines=["Aliquam venenatis", ]))
        self.assertDictEqual(input_date.as_data(), {
            "type": "Input.Date",
            "id": "id_date",
            "label": {
                "type": "RichTextBlock",
                "inlines": ["Aliquam venenatis", ]
            }
        })

    def test_input_time(self):
        input_time = TimeInput(max_value="16:00", min_value="10:00", placeholder="bonorum", value="14:37",
                               fallback=FallbackOption.DROP, separator=True, spacing=SpacingStyle.MEDIUM,
                               item_id="id_time", is_visible=True, requires=self.requires, label="est sapien")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "max": "16:00",
            "min": "10:00",
            "placeholder": "bonorum",
            "value": "14:37",
            "fallback": "drop",
            "separator": True,
            "spacing": "medium",
            "id": "id_time",
            "isVisible": True,
            "requires": self.requires,
            "label": "est sapien"
        })

    def test_input_time_set_max(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_max("21:54")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "max": "21:54"
        })

    def test_input_time_set_min(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_min("9:01")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "min": "9:01"
        })

    def test_input_time_set_placeholder(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_placeholder("Ad simul choro inermis mel")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "placeholder": "Ad simul choro inermis mel"
        })

    def test_input_time_set_value(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_value("12:34")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "value": "12:34"
        })

    def test_input_time_set_fallback(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "fallback": "drop"
        })
        input_time.set_fallback(Image(URL))
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            input_time.set_fallback(1234)

    def test_input_time_set_separator(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_separator(False)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "separator": False
        })
        input_time.set_separator(True)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "separator": True
        })
        input_time.set_separator()
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "separator": True
        })

    def test_input_time_set_spacing(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "spacing": "extraLarge"
        })

    def test_input_time_set_id(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_id("id_asdf")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_asdf"
        })

    def test_input_time_set_is_visible(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_is_visible(False)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "isVisible": False
        })
        input_time.set_is_visible(True)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "isVisible": True
        })
        input_time.set_is_visible()
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "isVisible": True
        })

    def test_input_time_set_requires(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_requires(self.requires)
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "requires": self.requires
        })

    def test_input_time_set_label(self):
        input_time = TimeInput(item_id="id_time")
        input_time.set_label("dapibus massa")
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "label": "dapibus massa"
        })
        input_time.set_label(TextBlock("Quisque in dolor eget"))
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "label": {
                "type": "TextBlock",
                "text": "Quisque in dolor eget"
            }
        })
        input_time.set_label(RichTextBlock(inlines=["Nunc leo ligula", ]))
        self.assertDictEqual(input_time.as_data(), {
            "type": "Input.Time",
            "id": "id_time",
            "label": {
                "type": "RichTextBlock",
                "inlines": ["Nunc leo ligula", ]
            }
        })

    def test_input_toggle(self):
        input_toggle = ToggleInput(title="Usu paulo errem percipitur", value="true", value_off="false", value_on="true",
                                   wrap=True, fallback=FallbackOption.DROP, separator=True, spacing=SpacingStyle.SMALL,
                                   item_id="id_toggle", is_visible=True, requires=self.requires, label="Sed convallis")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Usu paulo errem percipitur",
            "value": "true",
            "valueOff": "false",
            "valueOn": "true",
            "wrap": True,
            "fallback": "drop",
            "separator": True,
            "spacing": "small",
            "id": "id_toggle",
            "isVisible": True,
            "requires": self.requires,
            "label": "Sed convallis"
        })

    def test_input_toggle_set_title(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_title("Mei congue appellantur in")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Mei congue appellantur in"
        })

    def test_input_toggle_set_value(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_value("true")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "value": "true"
        })

    def test_input_toggle_set_value_off(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_value_off("true")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "valueOff": "true"
        })

    def test_input_toggle_set_value_ov(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_value_on("false")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "valueOn": "false"
        })

    def test_input_toggle_set_wrap(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_wrap(False)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "wrap": False
        })
        input_toggle.set_wrap(True)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "wrap": True
        })
        input_toggle.set_wrap()
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "wrap": True
        })

    def test_input_toggle_set_fallback(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "fallback": "drop"
        })
        input_toggle.set_fallback(Image(URL))
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            input_toggle.set_fallback(1234)

    def test_input_toggle_set_separator(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_separator(False)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "separator": False
        })
        input_toggle.set_separator(True)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "separator": True
        })
        input_toggle.set_separator()
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "separator": True
        })

    def test_input_toggle_set_spacing(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "spacing": "extraLarge"
        })

    def test_input_toggle_set_id(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_id("id_image_3")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "id": "id_image_3"
        })

    def test_input_toggle_set_is_visible(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_is_visible(False)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "isVisible": False
        })
        input_toggle.set_is_visible(True)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "isVisible": True
        })
        input_toggle.set_is_visible()
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "isVisible": True
        })

    def test_input_toggle_set_requires(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_requires(self.requires)
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "requires": self.requires
        })

    def test_input_toggle_set_label(self):
        input_toggle = ToggleInput(title="Lorem ipsum")
        input_toggle.set_label("tellus sollicitudin")
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "label": "tellus sollicitudin"
        })
        input_toggle.set_label(TextBlock("Nunc semper at"))
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "label": {
                "type": "TextBlock",
                "text": "Nunc semper at"
            }
        })
        input_toggle.set_label(RichTextBlock(inlines=["Suspendisse ac posuere", ]))
        self.assertDictEqual(input_toggle.as_data(), {
            "type": "Input.Toggle",
            "title": "Lorem ipsum",
            "label": {
                "type": "RichTextBlock",
                "inlines": ["Suspendisse ac posuere", ]
            }
        })

    def test_input_choice(self):
        input_choice = InputChoice(title="Choro homero aliquando", value=1)
        self.assertDictEqual(input_choice.as_data(), {
            "title": "Choro homero aliquando",
            "value": 1
        })

    def test_input_choice_set(self):
        choices = [InputChoice("First name", "foo"), InputChoice("Last name", 5)]
        input_choice_set = ChoiceSetInput(choices=choices, is_multi_select=True, style=ChoiceInputStyle.EXPANDED,
                                          value="foo", wrap=True, fallback=FallbackOption.DROP, separator=True,
                                          spacing=SpacingStyle.LARGE, item_id="id_input_choice_set", is_visible=True,
                                          requires=self.requires, label="Cras nisi velit")
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "First name",
                "value": "foo"
            }, {
                "title": "Last name",
                "value": 5
            }],
            "isMultiSelect": True,
            "style": "expanded",
            "value": "foo",
            "wrap": True,
            "fallback": "drop",
            "separator": True,
            "spacing": "large",
            "id": "id_input_choice_set",
            "isVisible": True,
            "requires": self.requires,
            "label": "Cras nisi velit"
        })

    def test_input_choice_set_set_choices(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_choices([InputChoice("First", 1), InputChoice("Second", 2), InputChoice("Third", 3)])
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "First",
                "value": 1
            }, {
                "title": "Second",
                "value": 2
            }, {
                "title": "Third",
                "value": 3
            }]
        })

    def test_input_choice_set_set_is_multi_select(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_is_multi_select(False)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "isMultiSelect": False
        })
        input_choice_set.set_is_multi_select(True)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "isMultiSelect": True
        })
        input_choice_set.set_is_multi_select()
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "isMultiSelect": True
        })

    def test_input_choice_set_set_style(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_style(ChoiceInputStyle.COMPACT)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "style": "compact"
        })

    def test_input_choice_set_set_value(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_value("bar")
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "value": "bar"
        })

    def test_input_choice_set_set_wrap(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_wrap(False)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "wrap": False
        })
        input_choice_set.set_wrap(True)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "wrap": True
        })
        input_choice_set.set_wrap()
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "wrap": True
        })

    def test_input_choice_set_set_fallback(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "fallback": "drop"
        })
        input_choice_set.set_fallback(Image(URL))
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            input_choice_set.set_fallback(1234)

    def test_input_choice_set_set_separator(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_separator(False)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "separator": False
        })
        input_choice_set.set_separator(True)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "separator": True
        })
        input_choice_set.set_separator()
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "separator": True
        })

    def test_input_choice_set_set_spacing(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "spacing": "extraLarge"
        })

    def test_input_choice_set_set_id(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_id("id_input_choice_set_3")
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "id": "id_input_choice_set_3"
        })

    def test_input_choice_set_set_is_visible(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_is_visible(False)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "isVisible": False
        })
        input_choice_set.set_is_visible(True)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "isVisible": True
        })
        input_choice_set.set_is_visible()
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "isVisible": True
        })

    def test_input_choice_set_set_requires(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_requires(self.requires)
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "requires": self.requires
        })

    def test_input_choice_set_set_label(self):
        input_choice_set = ChoiceSetInput([InputChoice("foo", "bar"), ])
        input_choice_set.set_label("purus pretium")
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "label": "purus pretium"
        })
        input_choice_set.set_label(TextBlock("Aenean at neque"))
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "label": {
                "type": "TextBlock",
                "text": "Aenean at neque"
            }
        })
        input_choice_set.set_label(RichTextBlock(inlines=["pellentesque arcu", ]))
        self.assertDictEqual(input_choice_set.as_data(), {
            "type": "Input.ChoiceSet",
            "choices": [{
                "title": "foo",
                "value": "bar"
            }],
            "label": {
                "type": "RichTextBlock",
                "inlines": ["pellentesque arcu", ]
            }
        })
