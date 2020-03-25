from django_actionable_messages.adaptive_card.actions import OpenUrl
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.containers import ColumnSet, Column
from django_actionable_messages.adaptive_card.elements import TextBlock, Image
from django_actionable_messages.adaptive_card.utils import SCHEMA, FontSize, FontWeight, SpacingStyle, ImageSize

"""
https://adaptivecards.io/samples/Restaurant.html
"""


restaurant = AdaptiveCard(version="1.0", schema=SCHEMA)
restaurant.add_elements([
    ColumnSet(columns=[
        Column(
            width=2,
            items=[
                TextBlock("Pizza"),
                TextBlock("Tom's Pie", weight=FontWeight.BOLDER, size=FontSize.EXTRA_LARGE, spacing=SpacingStyle.NONE),
                TextBlock("4.2 ★★★☆ (93) · $$", is_subtle=True, spacing=SpacingStyle.NONE),
                TextBlock("**Matt H. said** \"I'm compelled to give this place 5 stars due to the number of times "
                          "I've chosen to eat here this past year!\"", size=FontSize.SMALL, wrap=True)
            ]
        ),
        Column(
            width=1,
            items=[
                Image("https://picsum.photos/300?image=882", size=ImageSize.AUTO)
            ]
        )
    ])
])
restaurant.add_actions(
    OpenUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ", title="More info")
)
