from django_actionable_messages.message_card.actions import OpenUri, HttpPOST, ActionCard
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.message_card.elements import Fact, ActionTarget
from django_actionable_messages.message_card.inputs import TextInput
from django_actionable_messages.message_card.sections import Section
from django_actionable_messages.message_card.utils import OSType

"""
Github - issue opened
https://messagecardplayground.azurewebsites.net/
"""


issue_opened = MessageCard(title="Issue opened: \"Push notifications not working\"", summary="Issue 176715375",
                           theme_color="0078D7")
issue_opened.add_section(
    Section(
        activity_title="Miguel Garcie",
        activity_subtitle="9/13/2016, 11:46am",
        activity_image="https://connectorsdemo.azurewebsites.net/images/MSC12_Oscar_002.jpg",
        text="There is a problem with Push notifications, they don't seem to be picked up by the connector.",
        facts=[
            Fact("Repository:", "mgarcia\\test"),
            Fact("Issue #:", "176715375")
        ]
    )
)
issue_opened.add_actions([
    ActionCard(
        name="Add a comment",
        inputs=[
            TextInput(input_id="comment", title="Enter a comment", is_multiline=True)
        ],
        actions=[
            HttpPOST("OK", target="http://...")
        ]
    ),
    HttpPOST("Close", target="http://..."),
    OpenUri("View in Github", targets=[
        ActionTarget(OSType.DEFAULT, "http://...")
    ])
])
