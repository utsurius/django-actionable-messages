from typing import Union

from django_actionable_messages.adaptive_card.elements import Image
from django_actionable_messages.adaptive_card.types import Metadata
from django_actionable_messages.adaptive_card.utils import VERSIONS, Style, VerticalAlignment
from django_actionable_messages.exceptions import CardException
from django_actionable_messages.mixins import ADAPTIVE_CARD, Card


class AdaptiveCard(Card):
    card_type = ADAPTIVE_CARD

    def __init__(self, version: str = None, schema: str = None, refresh=None, authentication=None,
                 inputs: list = None, actions: list = None, select_action=None, style: Style = None,
                 hide_original_body: bool = None, fallback_text: str = None, background_image: Union[str, Image] = None,
                 metadata: Metadata = None, min_height: str = None, speak: str = None, lang: str = None,
                 rtl: bool = None, vertical_content_alignment: VerticalAlignment = None, **kwargs) -> None:
        self._payload = {
            "type": "AdaptiveCard"
        }
        super().__init__(**kwargs)
        if version is not None:
            self.set_version(version)
        if schema is not None:
            self.set_schema(schema)
        if refresh is not None:
            self.set_refresh(refresh)
        if authentication is not None:
            self.set_authentication(authentication)
        if inputs:
            self.add_elements(inputs)
        if actions:
            self.add_actions(actions)
        if select_action is not None:
            self.set_select_action(select_action)
        if style is not None:
            self.set_style(style)
        if hide_original_body is not None:
            self.set_hide_original_body(hide_original_body)
        if fallback_text is not None:
            self.set_fallback_text(fallback_text)
        if background_image is not None:
            self.set_background_image(background_image)
        if metadata is not None:
            self.set_metadata(metadata)
        if min_height is not None:
            self.set_min_height(min_height)
        if speak is not None:
            self.set_speak(speak)
        if lang is not None:
            self.set_lang(lang)
        if rtl is not None:
            self.set_rtl(rtl)
        if vertical_content_alignment is not None:
            self.set_vertical_content_alignment(vertical_content_alignment)

    def set_version(self, version: str) -> None:
        if version not in VERSIONS:
            raise CardException(f"Invalid version. Supported versions are: {VERSIONS}")
        self._payload["version"] = version

    def set_schema(self, schema: str) -> None:
        self._payload["$schema"] = schema

    def set_refresh(self, refresh) -> None:
        self._payload["refresh"] = refresh.as_data()

    def set_authentication(self, authentication) -> None:
        self._payload["authentication"] = authentication.as_data()

    def set_select_action(self, action) -> None:
        self._payload["selectAction"] = action.as_data()

    def set_style(self, style: Style) -> None:
        self._payload["style"] = style

    def set_hide_original_body(self, value=True) -> None:
        self._payload["hideOriginalBody"] = value

    def set_fallback_text(self, text: str) -> None:
        self._payload["fallbackText"] = text

    def set_background_image(self, image: Union[str, Image]) -> None:
        if isinstance(image, Image):
            self._payload["backgroundImage"] = image.as_data()
        elif isinstance(image, str):
            self._payload["backgroundImage"] = image
        else:
            raise CardException("Invalid image type")

    def set_metadata(self, metadata: Metadata) -> None:
        self._payload["metadata"] = metadata.as_data()

    def set_min_height(self, height: str) -> None:
        self._payload["minHeight"] = height

    def set_speak(self, text: str) -> None:
        self._payload["speak"] = text

    def set_lang(self, lang: str) -> None:
        self._payload["lang"] = lang

    def set_rtl(self, value: bool) -> None:
        self._payload["rtl"] = value

    def set_vertical_content_alignment(self, alignment: VerticalAlignment) -> None:
        self._payload["verticalContentAlignment"] = alignment

    def add_elements(self, elements):
        self._payload.setdefault("body", [])
        if isinstance(elements, (list, set, tuple)):
            self._payload["body"].extend(self._get_items_list(elements))
        else:
            self._payload["body"].append(elements.as_data())

    def add_actions(self, actions):
        self._payload.setdefault("actions", [])
        if isinstance(actions, (list, set, tuple)):
            self._payload["actions"].extend(self._get_items_list(actions))
        else:
            self._payload["actions"].append(actions.as_data())
