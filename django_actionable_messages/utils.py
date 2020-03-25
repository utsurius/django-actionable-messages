import copy
import json

from django.template.loader import render_to_string

from django_actionable_messages.settings import card_settings

MESSAGE_CARD = 1
ADAPTIVE_CARD = 2


class BaseMixin:
    def __init__(self, *args, **kwargs):
        self.language_code = kwargs.pop("lang_code", card_settings.LANGUAGE_CODE)
        super().__init__()

    def get_language_code(self):
        return self.language_code

    def _get_items_list(self, items):
        return list([item.as_data() for item in items])


class CardElement(BaseMixin):
    _data = None

    def as_data(self):
        return self._data


class Card(BaseMixin):
    json_encoder = card_settings.JSON_ENCODER

    _payload = None
    card_type = None
    script_types = {
        MESSAGE_CARD: "application/ld+json",
        ADAPTIVE_CARD: "application/adaptivecard+json"
    }

    @property
    def payload(self):
        return self.get_payload()

    @property
    def json_payload(self):
        return self.get_payload(fmt="json")

    @property
    def html_payload(self):
        return self.get_payload(fmt="html")

    def get_payload(self, fmt=None):
        payload = copy.deepcopy(self._payload)
        if fmt == "json":
            payload = self._get_json_payload(payload)
        elif fmt == "html":
            payload = self._get_html_payload(payload)
        return payload

    def _get_json_payload(self, payload):
        return json.dumps(payload, cls=self.json_encoder, lang_code=self.get_language_code())

    def _get_html_payload(self, payload):
        context = {
            "script_type": self.script_types[self.card_type],
            "payload": self._get_json_payload(payload)
        }
        return render_to_string("django_actionable_messages/email.html", context=context)
