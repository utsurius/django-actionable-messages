from django.test import TestCase

from django_actionable_messages.message_card.inputs import TextInput, DateInput, InputChoice, MultiChoiceInput
from django_actionable_messages.message_card.utils import ChoiceStyle
from django_actionable_messages.utils import CardException


class InputsTestCase(TestCase):
    def test_text_input(self):
        text_input = TextInput(input_id="id_text", title="Title", value=5, is_required=True, max_length=8,
                               is_multiline=True)
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "id": "id_text",
            "title": "Title",
            "value": 5,
            "isRequired": True,
            "isMultiline": True,
            "maxLength": 8
        })

    def test_text_input_set_max_length(self):
        text_input = TextInput()
        text_input.set_max_length(19)
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "maxLength": 19
        })

    def test_text_input_set_is_multiline(self):
        text_input = TextInput()
        text_input.set_is_multiline()
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": True
        })

    def test_text_input_set_id(self):
        text_input = TextInput()
        text_input.set_id("id_text_input4")
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "id": "id_text_input4"
        })

    def test_text_input_set_title(self):
        text_input = TextInput()
        text_input.set_title("interdum")
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "title": "interdum"
        })

    def test_text_input_set_value(self):
        text_input = TextInput()
        text_input.set_value("accumsan")
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "value": "accumsan"
        })

    def test_text_input_set_is_required(self):
        text_input = TextInput()
        text_input.set_is_required(False)
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "isRequired": False
        })
        text_input.set_is_required(True)
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "isRequired": True
        })
        text_input.set_is_required()
        self.assertDictEqual(text_input.as_data(), {
            "@type": "TextInput",
            "isMultiline": False,
            "isRequired": True
        })

    def test_date_input(self):
        date_input = DateInput(input_id="id_date", title="Date", value=37, is_required=True, include_time=True)
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "id": "id_date",
            "title": "Date",
            "value": 37,
            "isRequired": True,
            "includeTime": True
        })

    def test_date_input_set_include_time(self):
        date_input = DateInput()
        date_input.set_include_time()
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "includeTime": True
        })

    def test_date_input_set_id(self):
        date_input = DateInput()
        date_input.set_id("id_date_input")
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "id": "id_date_input"
        })

    def test_date_input_set_title(self):
        date_input = DateInput()
        date_input.set_title("viverra")
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "title": "viverra"
        })

    def test_date_input_set_value(self):
        date_input = DateInput()
        date_input.set_value("mauris")
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "value": "mauris"
        })

    def test_date_input_set_is_required(self):
        date_input = DateInput()
        date_input.set_is_required(False)
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "isRequired": False
        })
        date_input.set_is_required(True)
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "isRequired": True
        })
        date_input.set_is_required()
        self.assertDictEqual(date_input.as_data(), {
            "@type": "DateInput",
            "isRequired": True
        })

    def test_multi_choice_input(self):
        choices = [InputChoice("Option 1", 1), InputChoice("Option 2", 2)]
        multi_choice_input = MultiChoiceInput(input_id="id_choice", title="Select something", value=0, is_required=True,
                                              choices=choices, is_multi_select=True, style=ChoiceStyle.EXPANDED)
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "id": "id_choice",
            "title": "Select something",
            "value": 0,
            "isRequired": True,
            "choices": [
                {"display": "Option 1", "value": 1},
                {"display": "Option 2", "value": 2}
            ],
            "isMultiSelect": True,
            "style": "expanded"
        })

    def test_multi_choice_input_add_choices(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.add_choices([InputChoice("Choice 1", "x"), InputChoice("Choice 2", "y")])
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "choices": [
                {"display": "Choice 1", "value": "x"},
                {"display": "Choice 2", "value": "y"}
            ]
        })

    def test_multi_choice_input_add_choice(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.add_choice(InputChoice("Blue", "b"))
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "choices": [
                {"display": "Blue", "value": "b"}
            ]
        })

    def test_multi_choice_input_set_is_multi_select(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.set_is_multi_select()
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "isMultiSelect": True
        })

    def test_multi_choice_input_set_style(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.set_style(ChoiceStyle.EXPANDED)
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "style": "expanded"
        })

    def test_multi_choice_input_choice_already_added(self):
        with self.assertRaisesMessage(CardException, "Choice with this 'value' [a] already added"):
            MultiChoiceInput(choices=[InputChoice("Name", "a"), InputChoice("Sample", "a")])

    def test_multi_choice_input_set_id(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.set_id("id_multi_choice_input")
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "id": "id_multi_choice_input"
        })

    def test_multi_choice_input_set_title(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.set_title("Aliquam")
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "title": "Aliquam"
        })

    def test_multi_choice_input_set_value(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.set_value("commodo")
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "value": "commodo"
        })

    def test_multi_choice_input_set_is_required(self):
        multi_choice_input = MultiChoiceInput()
        multi_choice_input.set_is_required(False)
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "isRequired": False
        })
        multi_choice_input.set_is_required(True)
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "isRequired": True
        })
        multi_choice_input.set_is_required()
        self.assertDictEqual(multi_choice_input.as_data(), {
            "@type": "MultichoiceInput",
            "isRequired": True
        })
