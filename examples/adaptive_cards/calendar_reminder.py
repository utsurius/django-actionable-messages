from django_actionable_messages.adaptive_card.actions import Submit
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.elements import TextBlock
from django_actionable_messages.adaptive_card.inputs import InputChoice, ChoiceSetInput
from django_actionable_messages.adaptive_card.utils import SCHEMA, FontSize, FontWeight, SpacingStyle, ChoiceInputStyle

"""
https://adaptivecards.io/samples/CalendarReminder.html
"""


calendar_reminder = AdaptiveCard(version="1.0", schema=SCHEMA)
calendar_reminder.set_speak("Your  meeting about \"Adaptive Card design session\" is starting at 12:30pm"
                            "Do you want to snooze  or do you want to send a late notification to the attendees?")
calendar_reminder.add_element(TextBlock("Adaptive Card design session", size=FontSize.LARGE, weight=FontWeight.BOLDER))
calendar_reminder.add_elements([
    TextBlock("Conf Room 112/3377 (10)", is_subtle=True),
    TextBlock("12:30 PM - 1:30 PM", is_subtle=True, spacing=SpacingStyle.NONE),
    TextBlock("Snooze for")
])
calendar_reminder.add_element(ChoiceSetInput(
    item_id="snooze", style=ChoiceInputStyle.COMPACT, value="5", choices=[
        InputChoice("5 minutes", "5"),
        InputChoice("15 minutes", "15"),
        InputChoice("30 minutes", "30")
    ]
))
calendar_reminder.add_actions([
    Submit(title="Snooze", data={
        "x": "snooze"
    }),
    Submit(title="I'll be late", data={
        "x": "late"
    })
])
