from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.containers import Column, ColumnSet
from django_actionable_messages.adaptive_card.elements import TextBlock, Image
from django_actionable_messages.adaptive_card.utils import (
    SCHEMA,FontSize, FontWeight, SpacingStyle, Width, ImageSize, HorizontalAlignment, Color
)

"""
https://adaptivecards.io/samples/FlightItinerary.html
"""


column_plane = Column(
    width=Width.AUTO,
    items=[
        TextBlock(" "),
        Image(url="http://adaptivecards.io/content/airplane.png", size=ImageSize.SMALL, spacing=SpacingStyle.NONE)
    ]
)
column_san_francisco = Column(
    width=1,
    items=[
        TextBlock("San Francisco", horizontal_alignment=HorizontalAlignment.RIGHT, is_subtle=True),
        TextBlock("SFO", horizontal_alignment=HorizontalAlignment.RIGHT, size=FontSize.EXTRA_LARGE,
                  color=Color.ACCENT, spacing=SpacingStyle.NONE)
    ]
)
column_amsterdam = Column(
    width=1,
    items=[
        TextBlock("Amsterdam", is_subtle=True),
        TextBlock("AMS", size=FontSize.EXTRA_LARGE, color=Color.ACCENT, spacing=SpacingStyle.NONE)
    ]
)

flight_itinerary = AdaptiveCard(version="1.0", schema=SCHEMA)
flight_itinerary.set_speak("Your flight is confirmed for you and 3 other passengers from San Francisco "
                           "to Amsterdam on Friday, October 10 8:30 AM")
flight_itinerary.add_elements([
    TextBlock("Passengers", weight=FontWeight.BOLDER, is_subtle=True),
    TextBlock("Sarah Hum", separator=True),
    TextBlock("Jeremy Goldberg", spacing=SpacingStyle.NONE),
    TextBlock("Evan Litvak", spacing=SpacingStyle.NONE),
    TextBlock("2 Stops", weight=FontWeight.BOLDER, spacing=SpacingStyle.MEDIUM),
    TextBlock("Fri, October 10 8:30 AM", weight=FontWeight.BOLDER, spacing=SpacingStyle.NONE),
])
flight_itinerary.add_element(ColumnSet([
    column_san_francisco,
    column_plane,
    column_amsterdam
]))
flight_itinerary.add_elements([
    TextBlock("Non-Stop", weight=FontWeight.BOLDER, spacing=SpacingStyle.MEDIUM),
    TextBlock("Fri, October 18 9:50 PM", weight=FontWeight.BOLDER, spacing=SpacingStyle.NONE),
])
flight_itinerary.add_element(ColumnSet(
    spacing=SpacingStyle.MEDIUM,
    columns=[
        column_amsterdam,
        column_plane,
        column_san_francisco
    ]
))
flight_itinerary.add_element(ColumnSet([
        Column(
            width="1",
            items=[
                TextBlock("Total", size=FontSize.MEDIUM, is_subtle=True)
            ]
        ),
        Column(
            width=1,
            items=[
                TextBlock("$4,032.54", size=FontSize.MEDIUM, weight=FontWeight.BOLDER)
            ]
        )
]))
