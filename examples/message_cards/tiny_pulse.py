from django_actionable_messages.message_card.actions import HttpPOST, ActionCard
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.message_card.elements import HeroImage
from django_actionable_messages.message_card.inputs import TextInput
from django_actionable_messages.message_card.sections import Section

"""
TINYPulse - engaged
https://messagecardplayground.azurewebsites.net/
"""


tiny_pulse = MessageCard(summary="Poll: What do you love about your job?", theme_color="E81123")
tiny_pulse.add_sections([
    HeroImage("https://messagecardplayground.azurewebsites.net/assets/TINYPulseEngageBanner.png"),
    Section(
        start_group=True,
        activity_title="*What do you love about your job?**",
        activity_text="It can be nothing, everything, and anything in between. Sharing is caring.",
        actions=[
            ActionCard(
                name="Yes",
                inputs=[
                    TextInput(input_id="comment", is_multiline=True, title="Feel free to elaborate")
                ],
                actions=[
                    HttpPOST("Answer anonymously", target="http://...", is_primary=True)
                ]
            )
        ]
    ),
    Section(
        activity_title="**Streak: 0** surveys in a row",
        activity_subtitle="Survey expires in 15 days on 4/6/2017"
    )
])
