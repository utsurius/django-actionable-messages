from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import Execute
from django_actionable_messages.adaptive_card.types import (
    BackgroundImage, Refresh, TokenExchangeResource, AuthCardButton, Authentication
)
from django_actionable_messages.adaptive_card.utils import FillMode, HorizontalAlignment, VerticalAlignment

URL = "https://www.example.com/"


class TypesTestCase(TestCase):
    def test_background_image(self):
        background_image = BackgroundImage(URL, FillMode.COVER, HorizontalAlignment.LEFT, VerticalAlignment.BOTTOM)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "fillMode": "cover",
            "horizontalAlignment": "left",
            "verticalAlignment": "bottom"
        })

    def test_background_image_set_url(self):
        background_image = BackgroundImage(URL)
        background_image.set_url("www.zxcv.com")
        self.assertDictEqual(background_image.as_data(), {
            "url": "www.zxcv.com"
        })

    def test_background_image_set_fill_mode(self):
        background_image = BackgroundImage(URL)
        background_image.set_fill_mode(FillMode.REPEAT_VERTICALLY)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "fillMode": "repeatVertically"
        })

    def test_background_image_set_horizontal_alignment(self):
        background_image = BackgroundImage(URL)
        background_image.set_horizontal_alignment(HorizontalAlignment.CENTER)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "horizontalAlignment": "center"
        })

    def test_background_image_set_vertical_alignment(self):
        background_image = BackgroundImage(URL)
        background_image.set_vertical_alignment(VerticalAlignment.TOP)
        self.assertDictEqual(background_image.as_data(), {
            "url": URL,
            "verticalAlignment": "top"
        })

    def test_refresh(self):
        refresh = Refresh(
            action=Execute(),
            user_ids=["user_1", "user_2"]
        )
        self.assertDictEqual(refresh.as_data(), {
            "action": {
                "type": "Action.Execute"
            },
            "userIds": ["user_1", "user_2"]
        })

    def test_refresh_set_action(self):
        refresh = Refresh()
        refresh.set_action(Execute())
        self.assertDictEqual(refresh.as_data(), {
            "action": {
                "type": "Action.Execute"
            }
        })

    def test_refresh_set_user_ids(self):
        refresh = Refresh()
        refresh.set_user_ids(['user_1', "user_2"])
        self.assertDictEqual(refresh.as_data(), {
            "userIds": ["user_1", "user_2"]
        })

    def test_token_exchange_resource(self):
        token = TokenExchangeResource(
            token_id="token_1",
            uri=URL,
            provider_id="provider_id"
        )
        self.assertDictEqual(token.as_data(), {
            "id": "token_1",
            "uri": URL,
            "providerId": "provider_id"
        })

    def test_token_exchange_resource_set_id(self):
        token = TokenExchangeResource(
            token_id="token_1",
            uri=URL,
            provider_id="provider_id"
        )
        token.set_id("token_2")
        self.assertDictEqual(token.as_data(), {
            "id": "token_2",
            "uri": URL,
            "providerId": "provider_id"
        })

    def test_token_exchange_resource_set_uri(self):
        token = TokenExchangeResource(
            token_id="token_1",
            uri=URL,
            provider_id="provider_id"
        )
        token.set_uri("https://www.test.com")
        self.assertDictEqual(token.as_data(), {
            "id": "token_1",
            "uri": "https://www.test.com",
            "providerId": "provider_id"
        })

    def test_token_exchange_resource_set_provider_id(self):
        token = TokenExchangeResource(
            token_id="token_1",
            uri=URL,
            provider_id="provider_id"
        )
        token.set_provider_id("provider_1")
        self.assertDictEqual(token.as_data(), {
            "id": "token_1",
            "uri": URL,
            "providerId": "provider_1"
        })

    def test_auth_card_button(self):
        auth_card_btn = AuthCardButton(
            btn_type="btn_submit",
            value="submit",
            title="sample_title",
            image=URL + "image.bmp"
        )
        self.assertDictEqual(auth_card_btn.as_data(), {
            "type": "btn_submit",
            "value": "submit",
            "title": "sample_title",
            "image": URL + "image.bmp"
        })

    def test_auth_card_button_set_title(self):
        auth_card_btn = AuthCardButton(
            btn_type="btn_submit",
            value="submit"
        )
        auth_card_btn.set_title("title")
        self.assertDictEqual(auth_card_btn.as_data(), {
            "type": "btn_submit",
            "value": "submit",
            "title": "title"
        })

    def test_auth_card_button_set_image(self):
        auth_card_btn = AuthCardButton(
            btn_type="btn_submit",
            value="submit"
        )
        auth_card_btn.set_image(URL + "image.bmp")
        self.assertDictEqual(auth_card_btn.as_data(), {
            "type": "btn_submit",
            "value": "submit",
            "image": URL + "image.bmp"
        })

    def test_authentication(self):
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
        self.assertDictEqual(authentication.as_data(), {
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
        })

    def test_authentication_set_text(self):
        authentication = Authentication()
        authentication.set_text("text")
        self.assertDictEqual(authentication.as_data(), {
            "text": "text"
        })

    def test_authentication_set_connection_name(self):
        authentication = Authentication()
        authentication.set_connection_name("connection")
        self.assertDictEqual(authentication.as_data(), {
            "connectionName": "connection"
        })

    def test_authentication_set_token_exchange_resource(self):
        authentication = Authentication()
        authentication.set_token_exchange_resource(TokenExchangeResource(
            token_id="token_1",
            uri=URL,
            provider_id="provider_id"
        ))
        self.assertDictEqual(authentication.as_data(), {
            "tokenExchangeResource": {
                "id": "token_1",
                "uri": URL,
                "providerId": "provider_id"
            }
        })

    def test_authentication_set_buttons(self):
        authentication = Authentication()
        authentication.set_buttons([
            AuthCardButton(
                btn_type="btn_submit",
                value="submit",
                title="submit_title",
                image=URL + "image1.bmp"
            ),
            AuthCardButton(
                btn_type="btn_view",
                value="view",
                title="view_title",
                image=URL + "image2.bmp"
            )
        ])
        self.assertDictEqual(authentication.as_data(), {
            "buttons": [{
                "type": "btn_submit",
                "value": "submit",
                "title": "submit_title",
                "image": URL + "image1.bmp"
            }, {
                "type": "btn_view",
                "value": "view",
                "title": "view_title",
                "image": URL + "image2.bmp"
            }]
        })
