from django_actionable_messages.msteams_cards.cards import HeroCard
from django_actionable_messages.msteams_cards.elements import OpenUrl, Image

"""
https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference#example-hero-card
"""

hero_card1 = HeroCard(
    title="Seattle Center Monorail",
    subtitle="Seattle Center Monorail",
    text="The Seattle Center Monorail is an elevated train line between Seattle Center (near the Space Needle) and "
         "downtown Seattle. It was built for the 1962 World's Fair. Its original two trains, completed in 1961, "
         "are still in service.",
    images=Image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Seattle_monorail01_2008-02-25.jpg/1024px-Seattle_monorail01_2008-02-25.jpg"),
    buttons=[
        OpenUrl(title="Official website", url="https://www.seattlemonorail.com"),
        OpenUrl(title="Wikipeda page", url="https://en.wikipedia.org/wiki/Seattle_Center_Monorail"),
    ]
)

# the same card using functions
hero_card2 = HeroCard()
hero_card2.set_title("Seattle Center Monorail")
hero_card2.set_subtitle("Seattle Center Monorail")
hero_card2.set_text("The Seattle Center Monorail is an elevated train line between Seattle Center "
                    "(near the Space Needle) and downtown Seattle. It was built for the 1962 World's Fair. "
                    "Its original two trains, completed in 1961, are still in service.")
hero_card2.add_images(Image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Seattle_monorail01_2008-02-25.jpg/1024px-Seattle_monorail01_2008-02-25.jpg"))
hero_card2.add_buttons([
    OpenUrl(title="Official website", url="https://www.seattlemonorail.com"),
    OpenUrl(title="Wikipeda page", url="https://en.wikipedia.org/wiki/Seattle_Center_Monorail")
])
