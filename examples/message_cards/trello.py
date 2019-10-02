from django_actionable_messages.message_card.actions import OpenUri, HttpPOST, ActionCard
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.message_card.elements import Fact, InputChoice, ActionTarget
from django_actionable_messages.message_card.inputs import TextInput, DateInput, MultiChoiceInput
from django_actionable_messages.message_card.sections import Section
from django_actionable_messages.message_card.utils import OSType

"""
Trello - card created
https://messagecardplayground.azurewebsites.net/
"""


trello_card = MessageCard(title="Card created: \"Name of card\"", summary="Card \"Test card\"", theme_color="0078D7")
trello_card.add_sections([
    Section(
        activity_title="Miguel Garcia",
        activity_subtitle="9/13/2016, 3:34pm",
        activity_image="https://connectorsdemo.azurewebsites.net/images/MSC12_Oscar_002.jpg",
        facts=[
            Fact("Board:", "Name of board"),
            Fact("List:", "Name of list"),
            Fact("Assigned to:", "(none)"),
            Fact("Due date:", "(none)")
        ]
    )
])
trello_card.add_actions([
    ActionCard(
        name="Set due date",
        inputs=[
            DateInput(input_id="dueDate", title="select a date")
        ],
        actions=[
            HttpPOST("OK", target="http://...")
        ]
    ),
    ActionCard(
        name="Move",
        inputs=[
            MultiChoiceInput(input_id="move", title="Pick a list", choices=[
                InputChoice("List 1", "l1"),
                InputChoice("List 2", "l2")
            ])
        ],
        actions=[
            HttpPOST("OK", target="http://...")
        ]
    ),
    ActionCard(
        name="Add a comment",
        inputs=[
            TextInput(input_id="comment", is_multiline=True, title="Enter your comment")
        ],
        actions=[
            HttpPOST("OK", target="http://...")
        ]
    ),
    OpenUri("View in Trello", targets=[
        ActionTarget(OSType.DEFAULT, "http://...")
    ])
])
