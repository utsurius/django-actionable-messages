from django_actionable_messages.adaptive_card.actions import ShowCard, Submit
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.containers import Column, ColumnSet, FactSet, Fact
from django_actionable_messages.adaptive_card.elements import TextBlock, Image
from django_actionable_messages.adaptive_card.inputs import DateInput, TextInput
from django_actionable_messages.adaptive_card.utils import (
    SCHEMA, FontSize, FontWeight, Width, ImageSize, ImageStyle, SpacingStyle
)

"""
https://adaptivecards.io/samples/ActivityUpdate.html
"""


activity_update = AdaptiveCard(version="1.0", schema=SCHEMA)
activity_update.add_element(TextBlock("Publish Adaptive Card schema", size=FontSize.MEDIUM, weight=FontWeight.BOLDER))
activity_update.add_element(ColumnSet([
    Column(
        width=Width.AUTO,
        items=[
            Image(url="https://pbs.twimg.com/profile_images/3647943215/d7f12830b3c17a5a9e4afcc370e3a37e_400x400.jpeg",
                  size=ImageSize.SMALL, style=ImageStyle.PERSON)
        ]
    ),
    Column(
        width=Width.STRETCH,
        items=[
            TextBlock("Matt Hidinger", weight=FontWeight.BOLDER, wrap=True),
            TextBlock("Created {{DATE(2017-02-14T06:08:39Z, SHORT)}", spacing=SpacingStyle.NONE, is_subtle=True,
                      wrap=True)
        ]
    )
]))
activity_update.add_element(TextBlock(
    "Now that we have defined the main rules and features of the format, we need to produce a schema and publish it "
    "to GitHub. The schema will be the starting point of our reference documentation.",
    wrap=True
))
activity_update.add_element(FactSet([
    Fact("Board:", "Adaptive card"),
    Fact("List:", "Backing"),
    Fact("Assigned to:",  "Matt Hidinger"),
    Fact("Due date:", "Not set")
]))
activity_update.add_action(ShowCard(
    title="Set due date",
    card=AdaptiveCard(
        inputs=[
            DateInput(item_id="dueDate")
        ],
        actions=[
            Submit(title="OK")
        ]
    )
))
activity_update.add_action(ShowCard(
    title="Comment",
    card=AdaptiveCard(
        inputs=[
            TextInput(item_id="comment", is_multiline=True, placeholder="Enter your comment")
        ],
        actions=[
            Submit(title="OK")
        ]
    )
))
