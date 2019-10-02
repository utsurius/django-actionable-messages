from django.test import TestCase

from django_actionable_messages.adaptive_card.actions import OpenUrl, Submit
from django_actionable_messages.adaptive_card.containers import (
    ActionSet, Container, Column, ColumnSet, Fact, FactSet, ImageSet
)
from django_actionable_messages.adaptive_card.elements import Image, TextBlock
from django_actionable_messages.adaptive_card.types import BackgroundImage
from django_actionable_messages.adaptive_card.utils import (
    SpacingStyle, FallbackOption, ImageSize, Style, VerticalAlignment, Width, BlockElementHeight, ActionStyle,
    ImageStyle, Color, FontType, FillMode, HorizontalAlignment
)
from django_actionable_messages.utils import CardException

URL = "https://www.example.com/"


class ContainersTestCase(TestCase):
    requires = {
        "parameter1": "foo",
        "parameter2": "bar",
        "parameter3": 1337
    }

    def test_action_set(self):
        actions = [OpenUrl(URL, title="View"), Submit(title="Submit")]
        action_set = ActionSet(actions=actions)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "View"
            }, {
                "type": "Action.Submit",
                "title": "Submit"
            }]
        })

    def test_action_set_add_actions(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.add_actions([OpenUrl("www.qwer.com", title="Click"), Submit(title="Submit", style=Style.DEFAULT)])
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }, {
                "type": "Action.OpenUrl",
                "url": "www.qwer.com",
                "title": "Click"
            }, {
                "type": "Action.Submit",
                "title": "Submit",
                "style": "default"
            }]
        })

    def test_action_set_add_action(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.add_action(OpenUrl("www.qwer.com", title="Click"))
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }, {
                "type": "Action.OpenUrl",
                "url": "www.qwer.com",
                "title": "Click"
            }]
        })

    def test_action_set_set_fallback(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "fallback": "drop"
        })
        action_set.set_fallback(Image(URL))
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            action_set.set_fallback(1234)

    def test_action_set_set_separator(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_separator(False)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "separator": False
        })
        action_set.set_separator(True)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "separator": True
        })
        action_set.set_separator()
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "separator": True
        })

    def test_action_set_set_spacing(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_spacing(SpacingStyle.LARGE)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "spacing": "large"
        })

    def test_action_set_set_id(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_id("id_actionset12")
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "id": "id_actionset12"
        })

    def test_action_set_set_is_visible(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_is_visible(False)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "isVisible": False
        })
        action_set.set_is_visible(True)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "isVisible": True
        })
        action_set.set_is_visible()
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "isVisible": True
        })

    def test_action_set_set_requires(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_requires(self.requires)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "requires": self.requires
        })

    def test_action_set_set_height(self):
        action_set = ActionSet(actions=[Submit(title="Submit"), ])
        action_set.set_height(BlockElementHeight.AUTO)
        self.assertDictEqual(action_set.as_data(), {
            "type": "ActionSet",
            "actions": [{
                "type": "Action.Submit",
                "title": "Submit"
            }],
            "height": "auto"
        })

    def test_container(self):
        items = [TextBlock(text="asdf", color=Color.GOOD), Image("www.qwer.com")]
        background_image = BackgroundImage("www.zxcv.com", fill_mode=FillMode.REPEAT_VERTICALLY)
        container = Container(items=items, select_action=OpenUrl(URL, title="View"), style=Style.ATTENTION,
                              vertical_content_alignment=VerticalAlignment.TOP, bleed=True,
                              background_image=background_image, min_height="50px", fallback=FallbackOption.DROP,
                              separator=True, spacing=SpacingStyle.MEDIUM, item_id="id_container1", is_visible=True,
                              requires=self.requires)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "asdf",
                "color": "good"
            }, {
                "type": "Image",
                "url": "www.qwer.com"
            }],
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": URL,
                "title": "View"
            },
            "style": "attention",
            "verticalContentAlignment": "top",
            "bleed": True,
            "backgroundImage": {
                "url": "www.zxcv.com",
                "fillMode": "repeatVertically"
            },
            "minHeight": "50px",
            "fallback": "drop",
            "separator": True,
            "spacing": "medium",
            "id": "id_container1",
            "isVisible": True,
            "requires": self.requires
        })

    def test_container_add_items(self):
        container = Container(items=[TextBlock(text="zxcv", color=Color.ACCENT), ])
        items = [
            Image(URL, alternate_text="image_none", height="32px"),
            TextBlock(text="asdf", color=Color.DEFAULT, font_type=FontType.MONOSPACE)
        ]
        container.add_items(items)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }, {
                "type": "Image",
                "url": URL,
                "altText": "image_none",
                "height": "32px"
            }, {
                "type": "TextBlock",
                "text": "asdf",
                "color": "default",
                "fontType": "monospace"
            }]
        })

    def test_container_add_item(self):
        container = Container(items=[TextBlock(text="zxcv", color=Color.ACCENT), ])
        container.add_item(Image(URL, alternate_text="image_none", height="32px"))
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }, {
                "type": "Image",
                "url": URL,
                "altText": "image_none",
                "height": "32px"
            }]
        })

    def test_container_set_select_action(self):
        container = Container(items=[TextBlock(text="sample text", color=Color.DEFAULT), ])
        container.set_select_action(OpenUrl("www.asdf.com", title="Click me!"))
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "sample text",
                "color": "default"
            }],
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": "www.asdf.com",
                "title": "Click me!"
            }
        })

    def test_container_set_style(self):
        container = Container(items=[TextBlock(text="asdf", color=Color.ACCENT), ])
        container.set_style(Style.EMPHASIS)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "asdf",
                "color": "accent"
            }],
            "style": "emphasis"
        })

    def test_container_set_vertical_content_alignment(self):
        container = Container(items=[TextBlock(text="zxcv", color=Color.ACCENT), ])
        container.set_vertical_content_alignment(VerticalAlignment.CENTER)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }],
            "verticalContentAlignment": "center"
        })

    def test_container_set_bleed(self):
        container = Container(items=[TextBlock(text="zxcv", color=Color.ACCENT), ])
        container.set_bleed(False)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }],
            "bleed": False
        })
        container.set_bleed(True)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }],
            "bleed": True
        })
        container.set_bleed()
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }],
            "bleed": True
        })

    def test_container_set_background_image(self):
        container = Container(items=[TextBlock(text="zxcv", color=Color.ACCENT), ])
        container.set_background_image(URL)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }],
            "backgroundImage": URL
        })
        container.set_background_image(BackgroundImage("www.example.com/image1.bmp",
                                                       horizontal_alignment=HorizontalAlignment.CENTER))
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "zxcv",
                "color": "accent"
            }],
            "backgroundImage": {
                "url": "www.example.com/image1.bmp",
                "horizontalAlignment": "center"
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid image type"):
            container.set_background_image(1234)

    def test_container_set_min_height(self):
        container = Container(items=[TextBlock(text="asdf", color=Color.GOOD), ])
        container.set_min_height("49px")
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "asdf",
                "color": "good"
            }],
            "minHeight": "49px"
        })

    def test_container_set_height(self):
        container = Container(items=[TextBlock(text="asdf", color=Color.GOOD), ])
        container.set_height(BlockElementHeight.AUTO)
        self.assertDictEqual(container.as_data(), {
            "type": "Container",
            "items": [{
                "type": "TextBlock",
                "text": "asdf",
                "color": "good"
            }],
            "height": "auto"
        })

    def test_column(self):
        items = [
            Image(URL, alternate_text="alt_img", height="48px", background_color="abcdef"),
            TextBlock(text="qwer", color=Color.DEFAULT, font_type=FontType.DEFAULT)
        ]
        action = OpenUrl("www.esample.com/click", title="View")
        column = Column(items=items, background_image=BackgroundImage("www.example.com"), bleed=True,
                        fallback=FallbackOption.DROP, min_height="100px", separator=True, spacing=SpacingStyle.MEDIUM,
                        select_action=action, style=Style.GOOD, vertical_content_alignment=VerticalAlignment.CENTER,
                        width=Width.AUTO, item_id="id_column", is_visible=True, requires=self.requires)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "items": [{
                "type": "Image",
                "url": URL,
                "height": "48px",
                "backgroundColor": "abcdef",
                "altText": "alt_img"
            }, {
                "type": "TextBlock",
                "text": "qwer",
                "color": "default",
                "fontType": "default"
            }],
            "backgroundImage": {
                "url": "www.example.com"
            },
            "bleed": True,
            "fallback": "drop",
            "minHeight": "100px",
            "separator": True,
            "spacing": "medium",
            "selectAction": {
                "type": "Action.OpenUrl",
                "url": "www.esample.com/click",
                "title": "View"
            },
            "style": "good",
            "verticalContentAlignment": "center",
            "width": "auto",
            "id": "id_column",
            "isVisible": True,
            "requires": self.requires
        })

    def test_column_add_items(self):
        column = Column()
        column.add_items([Image(URL, alternate_text="images"), TextBlock(text=" Sed sit amet sem", color=Color.ACCENT)])
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "items": [{
                "type": "Image",
                "url": URL,
                "altText": "images"
            }, {
                "type": "TextBlock",
                "text": " Sed sit amet sem",
                "color": "accent"
            }]
        })

    def test_column_add_item(self):
        column = Column()
        column.add_item(TextBlock(text="Integer et enim a sapien dapibus", color=Color.GOOD))
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "items": [{
                "type": "TextBlock",
                "text": "Integer et enim a sapien dapibus",
                "color": "good"
            }]
        })
        column.add_item(Image(URL, alternate_text="image1"))
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "items": [{
                "type": "TextBlock",
                "text": "Integer et enim a sapien dapibus",
                "color": "good"
            }, {
                "type": "Image",
                "url": URL,
                "altText": "image1"
            }]
        })

    def test_column_set_background_image(self):
        column = Column()
        column.set_background_image(URL)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "backgroundImage": URL
        })
        column.set_background_image(BackgroundImage(url="www.zxcv.com"))
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "backgroundImage": {
                "url": "www.zxcv.com"
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid image type"):
            column.set_background_image(1234)

    def test_column_set_bleed(self):
        column = Column()
        column.set_bleed(False)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "bleed": False
        })
        column.set_bleed(True)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "bleed": True
        })
        column.set_bleed()
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "bleed": True
        })

    def test_column_set_fallback(self):
        column = Column()
        column.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "fallback": "drop"
        })
        column.set_fallback(Column(style=Style.EMPHASIS))
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "fallback": {
                "type": "Column",
                "style": "emphasis"
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            column.set_fallback(1234)

    def test_column_set_separator(self):
        column = Column()
        column.set_separator(False)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "separator": False
        })
        column.set_separator()
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "separator": True
        })
        column.set_separator(True)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "separator": True
        })

    def test_column_set_spacing(self):
        column = Column()
        column.set_spacing(SpacingStyle.LARGE)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "spacing": "large"
        })

    def test_column_set_select_action(self):
        column = Column()
        column.set_select_action(Submit(title="Submit", style=ActionStyle.DESTRUCTIVE))
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "selectAction": {
                "type": "Action.Submit",
                "title": "Submit",
                "style": "destructive"
            }
        })

    def test_column_set_style(self):
        column = Column()
        column.set_style(Style.ATTENTION)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "style": "attention"
        })

    def test_column_set_vertical_content_alignment(self):
        column = Column()
        column.set_vertical_content_alignment(VerticalAlignment.BOTTOM)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "verticalContentAlignment": "bottom"
        })

    def test_column_set_width(self):
        column = Column()
        column.set_width("50px")
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "width": "50px"
        })
        column.set_width(Width.STRETCH)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "width": "stretch"
        })
        column.set_width(1234)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "width": 1234
        })
        with self.assertRaisesMessage(CardException, "Invalid width type"):
            column.set_width({})

    def test_column_set_id(self):
        column = Column()
        column.set_id("id15")
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "id": "id15"
        })

    def test_column_set_is_visible(self):
        column = Column()
        column.set_is_visible(False)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "isVisible": False
        })
        column.set_is_visible()
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "isVisible": True
        })
        column.set_is_visible(True)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "isVisible": True
        })

    def test_column_set_requires(self):
        column = Column()
        column.set_requires(self.requires)
        self.assertDictEqual(column.as_data(), {
            "type": "Column",
            "requires": self.requires
        })

    def test_column_set(self):
        action = Submit(title="Submit", style=ActionStyle.DESTRUCTIVE)
        columns = [Column(background_image=URL, bleed=True, separator=True), Column(style=Style.ACCENT, item_id="col2")]
        column_set = ColumnSet(columns=columns, select_action=action, style=Style.EMPHASIS, bleed=False,
                               min_height="20px", height=BlockElementHeight.AUTO, fallback=FallbackOption.DROP,
                               separator=True, spacing=SpacingStyle.LARGE, item_id="col_set1", is_visible=True,
                               requires=self.requires)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "columns": [{
                "type": "Column",
                "backgroundImage": URL,
                "bleed": True,
                "separator": True
            }, {
                "type": "Column",
                "style": "accent",
                "id": "col2"
            }],
            "selectAction": {
                "type": "Action.Submit",
                "title": "Submit",
                "style": "destructive"
            },
            "style": "emphasis",
            "bleed": False,
            "minHeight": "20px",
            "height": "auto",
            "fallback": "drop",
            "separator": True,
            "spacing": "large",
            "id": "col_set1",
            "isVisible": True,
            "requires": self.requires
        })

    def test_column_set_add_columns(self):
        column_set = ColumnSet()
        columns = [Column(style=Style.ACCENT, item_id="col"), Column(background_image=URL, bleed=True, separator=True)]
        column_set.add_columns(columns)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "columns": [{
                "type": "Column",
                "style": "accent",
                "id": "col"
            }, {
                "type": "Column",
                "backgroundImage": URL,
                "bleed": True,
                "separator": True
            }]
        })

    def test_column_set_add_column(self):
        column_set = ColumnSet(columns=[Column(style=Style.ACCENT, item_id="col"), Column(bleed=True)])
        column_set.add_column(Column(bleed=True, min_height="120px", spacing=SpacingStyle.DEFAULT))
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "columns": [{
                "type": "Column",
                "style": "accent",
                "id": "col"
            }, {
                "type": "Column",
                "bleed": True
            }, {
                "type": "Column",
                "bleed": True,
                "minHeight": "120px",
                "spacing": "default"
            }]
        })

    def test_column_set_set_select_action(self):
        column_set = ColumnSet()
        column_set.set_select_action(Submit(title="Post", style=ActionStyle.DEFAULT))
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "selectAction": {
                "type": "Action.Submit",
                "title": "Post",
                "style": "default"
            }
        })

    def test_column_set_set_style(self):
        column_set = ColumnSet()
        column_set.set_style(Style.ACCENT)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "style": "accent"
        })

    def test_column_set_set_bleed(self):
        column_set = ColumnSet()
        column_set.set_bleed(False)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "bleed": False
        })
        column_set.set_bleed(True)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "bleed": True
        })
        column_set.set_bleed()
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "bleed": True
        })

    def test_column_set_set_min_height(self):
        column_set = ColumnSet()
        column_set.set_min_height("50px")
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "minHeight": "50px"
        })

    def test_column_set_set_fallback(self):
        column_set = ColumnSet()
        column_set.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "fallback": "drop"
        })
        column_set.set_fallback(Image(URL))
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            column_set.set_fallback(1234)

    def test_column_set_set_separator(self):
        column_set = ColumnSet()
        column_set.set_separator(False)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "separator": False
        })
        column_set.set_separator(True)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "separator": True
        })
        column_set.set_separator()
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "separator": True
        })

    def test_column_set_set_spacing(self):
        column_set = ColumnSet()
        column_set.set_spacing(SpacingStyle.LARGE)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "spacing": "large"
        })

    def test_column_set_set_id(self):
        column_set = ColumnSet()
        column_set.set_id("id_columnset1")
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "id": "id_columnset1"
        })

    def test_column_set_set_is_visible(self):
        column_set = ColumnSet()
        column_set.set_is_visible(False)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "isVisible": False
        })
        column_set.set_is_visible(True)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "isVisible": True
        })
        column_set.set_is_visible()
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "isVisible": True
        })

    def test_column_set_set_requires(self):
        column_set = ColumnSet()
        column_set.set_requires(self.requires)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "requires": self.requires
        })

    def test_column_set_set_height(self):
        column_set = ColumnSet()
        column_set.set_height(BlockElementHeight.AUTO)
        self.assertDictEqual(column_set.as_data(), {
            "type": "ColumnSet",
            "height": "auto"
        })

    def test_fact(self):
        fact = Fact("foo", "bar")
        self.assertDictEqual(fact.as_data(), {
            "title": "foo",
            "value": "bar"
        })

    def test_fact_set(self):
        fact_set = FactSet([Fact("foo", "asdf"), Fact("bar", "zxcv"), Fact("name", "John")])
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "asdf"
            }, {
                "title": "bar",
                "value": "zxcv"
            }, {
                "title": "name",
                "value": "John"
            }]
        })

    def test_fact_set_add_facts(self):
        fact_set = FactSet([Fact("foo", "asdf")])
        fact_set.add_facts([Fact("bar", "zxcv"), Fact("name", "John")])
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "asdf"
            }, {
                "title": "bar",
                "value": "zxcv"
            }, {
                "title": "name",
                "value": "John"
            }]
        })

    def test_fact_set_add_fact(self):
        fact_set = FactSet([Fact("foo", "asdf")])
        fact_set.add_fact(Fact("bar", "zxcv"))
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "asdf"
            }, {
                "title": "bar",
                "value": "zxcv"
            }]
        })

    def test_fact_set_set_fallback(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "fallback": "drop"
        })
        fact_set.set_fallback(Image(URL))
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "fallback": {
                "type": "Image",
                "url": URL
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            fact_set.set_fallback(1234)

    def test_fact_set_set_separator(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_separator(False)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "separator": False
        })
        fact_set.set_separator(True)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "separator": True
        })
        fact_set.set_separator()
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "separator": True
        })

    def test_fact_set_set_spacing(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_spacing(SpacingStyle.DEFAULT)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "spacing": "default"
        })

    def test_fact_set_set_id(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_id("id_fact_set_3")
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "id": "id_fact_set_3"
        })

    def test_fact_set_set_is_visible(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_is_visible(False)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "isVisible": False
        })
        fact_set.set_is_visible(True)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "isVisible": True
        })
        fact_set.set_is_visible()
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "isVisible": True
        })

    def test_fact_set_set_requires(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_requires(self.requires)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "requires": self.requires
        })

    def test_fact_set_set_height(self):
        fact_set = FactSet([Fact("foo", "bar")])
        fact_set.set_height(BlockElementHeight.STRETCH)
        self.assertDictEqual(fact_set.as_data(), {
            "type": "FactSet",
            "facts": [{
                "title": "foo",
                "value": "bar"
            }],
            "height": "stretch"
        })

    def test_image_set(self):
        images = [Image(url="www.example.com/image1.jpeg"), Image(url="www.example.com/image2.png")]
        image_set = ImageSet(images=images, image_size=ImageSize.LARGE, height=BlockElementHeight.STRETCH,
                             fallback=FallbackOption.DROP, separator=True, spacing=SpacingStyle.DEFAULT, item_id="set1",
                             is_visible=False, requires=self.requires)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.example.com/image1.jpeg"
            }, {
                "type": "Image",
                "url": "www.example.com/image2.png"
            }],
            "imageSize": "large",
            "height": "stretch",
            "fallback": "drop",
            "separator": True,
            "spacing": "default",
            "id": "set1",
            "isVisible": False,
            "requires": self.requires
        })

    def test_image_set_add_images(self):
        images = [Image(url="www.example.com/image1.jpeg"), Image(url="www.example.com/image2.jpeg")]
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.add_images(images)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }, {
                "type": "Image",
                "url": "www.example.com/image1.jpeg"
            }, {
                "type": "Image",
                "url": "www.example.com/image2.jpeg"
            }]
        })

    def test_image_set_add_image(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.add_image(Image(url="www.example.com/image2.jpeg"))
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }, {
                "type": "Image",
                "url": "www.example.com/image2.jpeg"
            }]
        })

    def test_image_set_set_image_size(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_image_size(ImageSize.STRETCH)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "imageSize": "stretch"
        })

    def test_image_set_set_fallback(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_fallback(FallbackOption.DROP)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "fallback": "drop"
        })
        image_set.set_fallback(TextBlock("asdf", color=Color.ATTENTION))
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "fallback": {
                "type": "TextBlock",
                "text": "asdf",
                "color": "attention"
            }
        })
        with self.assertRaisesMessage(CardException, "Invalid fallback type"):
            image_set.set_fallback(1234)

    def test_image_set_set_separator(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_separator(False)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "separator": False
        })
        image_set.set_separator(True)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "separator": True
        })
        image_set.set_separator()
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "separator": True
        })

    def test_image_set_set_id(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_id("id_images")
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "id": "id_images"
        })

    def test_image_set_set_is_visible(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_is_visible(False)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "isVisible": False
        })
        image_set.set_is_visible(True)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "isVisible": True
        })
        image_set.set_is_visible()
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "isVisible": True
        })

    def test_image_set_set_requires(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_requires(self.requires)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "requires": self.requires
        })

    def test_image_set_set_height(self):
        image_set = ImageSet(images=[Image(url="www.sample.com/image.bmp"), ])
        image_set.set_height(BlockElementHeight.AUTO)
        self.assertDictEqual(image_set.as_data(), {
            "type": "ImageSet",
            "images": [{
                "type": "Image",
                "url": "www.sample.com/image.bmp"
            }],
            "height": "auto"
        })
