from django_actionable_messages.message_card.actions import HttpPOST, ActionCard
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.message_card.elements import Fact, HeroImage
from django_actionable_messages.message_card.inputs import TextInput
from django_actionable_messages.message_card.sections import Section


"""
Microsoft - flow approval
https://messagecardplayground.azurewebsites.net/
"""


flow_approval = MessageCard(summary="This is the summary property", theme_color="0075FF")
flow_approval.add_sections([
    HeroImage("https://messagecardplayground.azurewebsites.net/assets/FlowLogo.png"),
    Section(
        start_group=True,
        title="**Pending approval**",
        activity_image="https://connectorsdemo.azurewebsites.net/images/MSC12_Oscar_002.jpg",
        activity_title="Requested by **Miguel Garcia**",
        activity_subtitle="m.garcia@contoso.com",
        facts=[
            Fact("Date submitted:", "06/27/2017, 2:44 PM"),
            Fact("Details:", "Please approve the awesome changes I made to this fantastic document."),
            Fact("Link:", "[Link to the awesome document.pptx](https://awesomedocument)"),
        ]
    ),
    Section(
        actions=[
            ActionCard(
                name="Approve",
                inputs=[
                    TextInput(input_id="comment", is_multiline=True, title="Reason (optional)")
                ],
                actions=[
                    HttpPOST("OK", target="http://...")
                ]
            ),
            ActionCard(
                name="Reject",
                inputs=[
                    TextInput(input_id="comment", is_multiline=True, title="Reason (optional)")
                ],
                actions=[
                    HttpPOST("OK", target="http://...")
                ]
            )
        ]
    ),
    Section(
        start_group=True,
        activity_subtitle="Grant approvals directly from your mobile device with the Microsoft Flow app. "
                          "[Learn more](https://learnmode)\n\nThis message was created by an automated workflow "
                          "in Microsoft Flow. Do not reply."
    )
])
