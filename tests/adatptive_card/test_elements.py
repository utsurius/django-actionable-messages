from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import OpenUrl
from django_actionable_messages.adaptive_card.elements import TextBlock, Image, MediaSource, Media, TextRun, RichTextBlock
from django_actionable_messages.adaptive_card.utils import (
    Color, FontType, HorizontalAlignment, FontSize, FallbackOption, FontWeight, SpacingStyle, ImageSize, ImageStyle,
    BlockElementHeight
)
from django_actionable_messages.utils import CardException

URL = "https://www.example.com/"


class ElementsTestCase(TestCase):
    requires = {
        "parameter1": "foo",
        "parameter2": "bar",
        "parameter3": 1337
    }

    def test_text_block(self):
        text_block = TextBlock(text="Lorem ipsum dolor sit amet", color=Color.ATTENTION, font_type=FontType.MONOSPACE,
                               horizontal_alignment=HorizontalAlignment.CENTER, is_subtle=True, max_lines=32,
                               size=FontSize.LARGE, weight=FontWeight.LIGHTER, wrap=True, fallback=FallbackOption.DROP,
                               separator=True, spacing=SpacingStyle.LARGE, item_id="id_text_block", is_visible=True,
                               requires=self.requires)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "Lorem ipsum dolor sit amet",
            "color": "attention",
            "fontType": "monospace",
            "horizontalAlignment": "center",
            "isSubtle": True,
            "maxLines": 32,
            "size": "large",
            "weight": "lighter",
            "wrap": True,
            "fallback": "drop",
            "separator": True,
            "spacing": "large",
            "id": "id_text_block",
            "isVisible": True,
            "requires": self.requires
        })

    def test_text_block_set_text(self):
        text_block = TextBlock(text="asdf")
        text_block.set_text("Ut enim ad minim veniam")
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "Ut enim ad minim veniam"
        })

    def test_text_block_set_color(self):
        text_block = TextBlock(text="asdf")
        text_block.set_color(Color.DEFAULT)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "color": "default"
        })

    def test_text_block_set_font_type(self):
        text_block = TextBlock(text="asdf")
        text_block.set_font_type(FontType.DEFAULT)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "fontType": "default"
        })

    def test_text_block_set_horizontal_alignment(self):
        text_block = TextBlock(text="asdf")
        text_block.set_horizontal_alignment(HorizontalAlignment.LEFT)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "horizontalAlignment": "left"
        })

    def test_text_block_set_is_subtle(self):
        text_block = TextBlock(text="asdf")
        text_block.set_is_subtle(False)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "isSubtle": False
        })
        text_block.set_is_subtle(True)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "isSubtle": True
        })
        text_block.set_is_subtle()
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "isSubtle": True
        })

    def test_text_block_set_max_lines(self):
        text_block = TextBlock(text="asdf")
        text_block.set_max_lines(1235)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "maxLines": 1235
        })

    def test_text_block_set_size(self):
        text_block = TextBlock(text="asdf")
        text_block.set_size(FontSize.MEDIUM)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "size": "medium"
        })

    def test_text_block_set_weight(self):
        text_block = TextBlock(text="asdf")
        text_block.set_weight(FontWeight.BOLDER)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "weight": "bolder"
        })

    def test_text_block_set_wrap(self):
        text_block = TextBlock(text="asdf")
        text_block.set_wrap(False)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "wrap": False
        })
        text_block.set_wrap(True)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "wrap": True
        })
        text_block.set_wrap()
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "wrap": True
        })

    def test_text_block_set_fallback(self):
        text_block = TextBlock(text="asdf")
        text_block.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "fallback": "drop"
        })
        text_block.set_fallback(Image(URL))
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            text_block.set_fallback(1234)

    def test_text_block_set_separator(self):
        text_block = TextBlock(text="asdf")
        text_block.set_separator(False)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "separator": False
        })
        text_block.set_separator(True)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "separator": True
        })
        text_block.set_separator()
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "separator": True
        })

    def test_text_block_set_spacing(self):
        text_block = TextBlock(text="asdf")
        text_block.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "spacing": "extraLarge"
        })

    def test_text_block_set_id(self):
        text_block = TextBlock(text="asdf")
        text_block.set_id("id_text_block_3")
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "id": "id_text_block_3"
        })

    def test_text_block_set_is_visible(self):
        text_block = TextBlock(text="asdf")
        text_block.set_is_visible(False)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "isVisible": False
        })
        text_block.set_is_visible(True)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "isVisible": True
        })
        text_block.set_is_visible()
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "isVisible": True
        })

    def test_text_block_set_requires(self):
        text_block = TextBlock(text="asdf")
        text_block.set_requires(self.requires)
        self.assertDictEqual(text_block.as_data(), {
            "type": "TextBlock",
            "text": "asdf",
            "requires": self.requires
        })

    def test_image(self):
        image = Image(URL, alternate_text="Ut enim ad minim veniam", background_color="0f0f0f", height="50px",
                      horizontal_alignment=HorizontalAlignment.LEFT, select_action=OpenUrl("www.sample.com"),
                      size=ImageSize.SMALL, style=ImageStyle.PERSON, width="100px", fallback=FallbackOption.DROP,
                      separator=True, spacing=SpacingStyle.SMALL, item_id="id_image", is_visible=True,
                      requires=self.requires)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "altText": "Ut enim ad minim veniam",
            "backgroundColor": "0f0f0f",
            "height": "50px",
            "horizontalAlignment": "left",
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": "www.sample.com"
            },
            "size": "small",
            "style": "person",
            "width": "100px",
            "fallback": "drop",
            "separator": True,
            "spacing": "small",
            "id": "id_image",
            "isVisible": True,
            "requires": self.requires
        })

    def test_image_set_url(self):
        image = Image(URL)
        image.set_url("www.qwerty.com/image.bmp")
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": "www.qwerty.com/image.bmp"
        })

    def test_image_set_alternate_text(self):
        image = Image(URL)
        image.set_alternate_text("Duis aute irure")
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "altText": "Duis aute irure"
        })

    def test_image_set_background_color(self):
        image = Image(URL)
        image.set_background_color("abcdef")
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "backgroundColor": "abcdef"
        })

    def test_image_set_height(self):
        image = Image(URL)
        image.set_height("42px")
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "height": "42px"
        })
        image.set_height(BlockElementHeight.STRETCH)
        with self.assertRaisesMessage(CardException, "Invalid height type"):
            image.set_height(1234)

    def test_image_set_horizontal_alignment(self):
        image = Image(URL)
        image.set_horizontal_alignment(HorizontalAlignment.RIGHT)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "horizontalAlignment": "right"
        })

    def test_image_set_select_action(self):
        image = Image(URL)
        image.set_select_action(OpenUrl("www.click.me"))
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": "www.click.me"
            }
        })

    def test_image_set_size(self):
        image = Image(URL)
        image.set_size(ImageSize.LARGE)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "size": "large"
        })

    def test_image_set_style(self):
        image = Image(URL)
        image.set_style(ImageStyle.DEFAULT)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "style": "default"
        })

    def test_image_set_width(self):
        image = Image(URL)
        image.set_width("128px")
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "width": "128px"
        })

    def test_image_set_fallback(self):
        image = Image(URL)
        image.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "fallback": "drop"
        })
        image.set_fallback(Image(URL))
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            image.set_fallback(1234)

    def test_image_set_separator(self):
        image = Image(URL)
        image.set_separator(False)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "separator": False
        })
        image.set_separator(True)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "separator": True
        })
        image.set_separator()
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "separator": True
        })

    def test_image_set_spacing(self):
        image = Image(URL)
        image.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "spacing": "extraLarge"
        })

    def test_image_set_id(self):
        image = Image(URL)
        image.set_id("id_image_3")
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "id": "id_image_3"
        })

    def test_image_set_is_visible(self):
        image = Image(URL)
        image.set_is_visible(False)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "isVisible": False
        })
        image.set_is_visible(True)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "isVisible": True
        })
        image.set_is_visible()
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "isVisible": True
        })

    def test_image_set_requires(self):
        image = Image(URL)
        image.set_requires(self.requires)
        self.assertDictEqual(image.as_data(), {
            "type": "Image",
            "url": URL,
            "requires": self.requires
        })

    def test_media_source(self):
        media_source = MediaSource("image/svg+xml", URL)
        self.assertDictEqual(media_source.as_data(), {
            "mimeType": "image/svg+xml",
            "url": URL
        })

    def test_media(self):
        sources = [
            MediaSource("application/gzip", "www.source.com/1"),
            MediaSource("text/calendar", "www.source.com/2")
        ]
        media = Media(sources=sources, poster="Excepteur sint occaecat cupidatat non proident",
                      alternate_text="sunt in culpa", fallback=FallbackOption.DROP, separator=True,
                      spacing=SpacingStyle.MEDIUM, item_id="id_image", is_visible=True, requires=self.requires)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "application/gzip",
                "url": "www.source.com/1"
            }, {
                "mimeType": "text/calendar",
                "url": "www.source.com/2"
            }],
            "poster": "Excepteur sint occaecat cupidatat non proident",
            "altText": "sunt in culpa",
            "fallback": "drop",
            "separator": True,
            "spacing": "medium",
            "id": "id_image",
            "isVisible": True,
            "requires": self.requires
        })

    def test_media_add_sources(self):
        media = Media(sources=[MediaSource("audio/mpeg", "www.url.com"), ])
        media.add_sources([MediaSource("application/php", "www.php.com"), MediaSource("image/gif", "www.gif.com")])
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "audio/mpeg",
                "url": "www.url.com"
            }, {
                "mimeType": "application/php",
                "url": "www.php.com"
            }, {
                "mimeType": "image/gif",
                "url": "www.gif.com"
            }]
        })

    def test_media_add_source(self):
        media = Media(sources=[MediaSource("audio/mpeg", "www.url.com"), MediaSource("application/php", "www.php.com")])
        media.add_source(MediaSource("image/gif", "www.gif.com"))
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "audio/mpeg",
                "url": "www.url.com"
            }, {
                "mimeType": "application/php",
                "url": "www.php.com"
            }, {
                "mimeType": "image/gif",
                "url": "www.gif.com"
            }]
        })

    def test_media_set_poster(self):
        media = Media(sources=[MediaSource("audio/mpeg", "www.url.com"), ])
        media.set_poster("His ei quod fastidii quaestio")
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "audio/mpeg",
                "url": "www.url.com"
            }],
            "poster": "His ei quod fastidii quaestio"
        })

    def test_media_set_alternate_text(self):
        media = Media(sources=[MediaSource("audio/mpeg", "www.url.com"), ])
        media.set_alternate_text("Sale civibus suavitate vix eu")
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "audio/mpeg",
                "url": "www.url.com"
            }],
            "altText": "Sale civibus suavitate vix eu"
        })

    def test_media_set_fallback(self):
        media = Media(sources=[MediaSource("text/html", "www.url.com"), ])
        media.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "fallback": "drop"
        })
        media.set_fallback(Image(URL))
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            media.set_fallback(1234)

    def test_media_set_separator(self):
        media = Media(sources=[MediaSource("text/html", "www.url.com"), ])
        media.set_separator(False)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "separator": False
        })
        media.set_separator(True)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "separator": True
        })
        media.set_separator()
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "separator": True
        })

    def test_media_set_spacing(self):
        media = Media(sources=[MediaSource("text/html", "www.url.com"), ])
        media.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "spacing": "extraLarge"
        })

    def test_media_set_id(self):
        media = Media(sources=[MediaSource("text/html", "www.url.com"), ])
        media.set_id("id_image_3")
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "id": "id_image_3"
        })

    def test_media_set_is_visible(self):
        media = Media(sources=[MediaSource("text/html", "www.url.com"), ])
        media.set_is_visible(False)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "isVisible": False
        })
        media.set_is_visible(True)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "isVisible": True
        })
        media.set_is_visible()
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "isVisible": True
        })

    def test_media_set_requires(self):
        media = Media(sources=[MediaSource("text/html", "www.url.com"), ])
        media.set_requires(self.requires)
        self.assertDictEqual(media.as_data(), {
            "type": "Media",
            "sources": [{
                "mimeType": "text/html",
                "url": "www.url.com"
            }],
            "requires": self.requires
        })

    def test_text_run(self):
        text_run = TextRun(text="Choro homero aliquando te vis", color=Color.ATTENTION, font_type=FontType.MONOSPACE,
                           highlight=True, is_subtle=True, italic=True, select_action=OpenUrl(URL), size=FontSize.SMALL,
                           strike_through=True, weight=FontWeight.BOLDER)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "Choro homero aliquando te vis",
            "color": "attention",
            "fontType": "monospace",
            "highlight": True,
            "isSubtle": True,
            "italic": True,
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": URL
            },
            "size": "small",
            "strikethrough": True,
            "weight": "bolder"
        })

    def test_text_run_set_text(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_text("At sed sumo temporibus omittantur")
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "At sed sumo temporibus omittantur"
        })

    def test_text_run_set_color(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_color(Color.ACCENT)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "color": "accent"
        })

    def test_text_run_set_font_type(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_font_type(FontType.DEFAULT)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "fontType": "default"
        })

    def test_text_run_set_highlight(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_highlight(False)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "highlight": False
        })
        text_run.set_highlight(True)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "highlight": True
        })
        text_run.set_highlight()
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "highlight": True
        })

    def test_text_run_set_is_subtle(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_is_subtle(False)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "isSubtle": False
        })
        text_run.set_is_subtle(True)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "isSubtle": True
        })
        text_run.set_is_subtle()
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "isSubtle": True
        })

    def test_text_run_set_italic(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_italic(False)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "italic": False
        })
        text_run.set_italic(True)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "italic": True
        })
        text_run.set_italic()
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "italic": True
        })

    def test_text_run_set_select_action(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_select_action(OpenUrl(URL))
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": URL
            }
        })

    def test_text_run_set_size(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_size(FontSize.LARGE)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "size": "large"
        })

    def test_text_run_set_strike_through(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_strike_through(False)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "strikethrough": False
        })
        text_run.set_strike_through(True)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "strikethrough": True
        })
        text_run.set_strike_through()
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "strikethrough": True
        })

    def test_text_run_set_weight(self):
        text_run = TextRun(text="lorem ipsum")
        text_run.set_weight(FontWeight.LIGHTER)
        self.assertDictEqual(text_run.as_data(), {
            "type": "TextRun",
            "text": "lorem ipsum",
            "weight": "lighter"
        })

    def test_rich_text_block(self):
        inlines = ["Odio adipisci honestatis sea ad", TextRun(text="Ad duo graecis hendrerit", color=Color.ATTENTION)]
        rich_text_block = RichTextBlock(inlines=inlines, horizontal_alignment=HorizontalAlignment.CENTER,
                                        fallback=FallbackOption.DROP, separator=True, spacing=SpacingStyle.MEDIUM,
                                        item_id="id_image", is_visible=True, requires=self.requires)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": [
                "Odio adipisci honestatis sea ad",
                {
                    "type": "TextRun",
                    "text": "Ad duo graecis hendrerit",
                    "color": "attention"
                }
            ],
            "horizontalAlignment": "center",
            "fallback": "drop",
            "separator": True,
            "spacing": "medium",
            "id": "id_image",
            "isVisible": True,
            "requires": self.requires
        })

    def test_rich_text_block_set_inlines(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_inlines([TextRun("Sed ea quod nominati, at vel", color=Color.GOOD), "Eos saepe phaedrum"])
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": [
                {
                    "type": "TextRun",
                    "text": "Sed ea quod nominati, at vel",
                    "color": "good"
                },
                "Eos saepe phaedrum"
            ]
        })
        with self.assertRaisesMessage(CardException, "Invalid inline type"):
            rich_text_block.set_inlines([1234, ])

    def test_rich_text_block_set_horizontal_alignment(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_horizontal_alignment(HorizontalAlignment.RIGHT)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "horizontalAlignment": "right"
        })

    def test_rich_text_block_set_fallback(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "fallback": "drop"
        })
        rich_text_block.set_fallback(Image(URL))
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            rich_text_block.set_fallback(1234)

    def test_rich_text_block_set_separator(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_separator(False)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "separator": False
        })
        rich_text_block.set_separator(True)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "separator": True
        })
        rich_text_block.set_separator()
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "separator": True
        })

    def test_rich_text_block_set_spacing(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_spacing(SpacingStyle.EXTRA_LARGE)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "spacing": "extraLarge"
        })

    def test_rich_text_block_set_id(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_id("id_image_3")
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "id": "id_image_3"
        })

    def test_rich_text_block_set_is_visible(self):
        rich_text_block = RichTextBlock(inlines=["lorem ipsum", ])
        rich_text_block.set_is_visible(False)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "isVisible": False
        })
        rich_text_block.set_is_visible(True)
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "isVisible": True
        })
        rich_text_block.set_is_visible()
        self.assertDictEqual(rich_text_block.as_data(), {
            "type": "RichTextBlock",
            "inlines": ["lorem ipsum", ],
            "isVisible": True
        })
