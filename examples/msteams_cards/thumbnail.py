from django_actionable_messages.msteams_cards.cards import ThumbnailCard
from django_actionable_messages.msteams_cards.elements import OpenUrl, Image

"""
https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference#thumbnail-card
"""

thumbnail_card1 = ThumbnailCard(
    title="Task created: reminder to finish sales projections",
    subtitle="Assigned to: Claude Grady",
    text="Sint incidunt voluptates facilis",
    images=Image("???"),
    buttons=[
        OpenUrl(title="View task", url="???"),
        OpenUrl(title="Assign to me", url="???")
    ]
)

# the same card using functions
thumbnail_card2 = ThumbnailCard()
thumbnail_card2.set_title("Task created: reminder to finish sales projections")
thumbnail_card2.set_subtitle("Assigned to: Claude Grady")
thumbnail_card2.set_text("Sint incidunt voluptates facilis")
thumbnail_card2.add_images(Image("???"))
thumbnail_card2.add_buttons([
    OpenUrl(title="View task", url="???"),
    OpenUrl(title="Assign to me", url="???")
])
