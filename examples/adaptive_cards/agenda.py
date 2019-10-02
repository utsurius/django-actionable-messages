from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.containers import ColumnSet, Column, ImageSet
from django_actionable_messages.adaptive_card.elements import TextBlock, Image
from django_actionable_messages.adaptive_card.types import BackgroundImage
from django_actionable_messages.adaptive_card.utils import (
    SCHEMA, SpacingStyle, ImageSize, Width, FillMode, HorizontalAlignment
)

"""
https://adaptivecards.io/samples/Agenda.html
"""


column_set1 = ColumnSet(
    columns=[
        Column(
            items=[
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/LocationGreen_A.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("**Redmond**"),
                                TextBlock("8a - 12:30p", spacing=SpacingStyle.NONE)
                            ],
                            width=Width.AUTO
                        )
                    ]
                )
            ],
            width=1
        ),
        Column(
            items=[
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/LocationBlue_B.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("**Bellevue**"),
                                TextBlock("12:30p - 3p", spacing=SpacingStyle.NONE)
                            ],
                            width=Width.AUTO
                        )
                    ]
                )
            ],
            spacing=SpacingStyle.LARGE,
            separator=True,
            width=1
        ),
        Column(
            items=[
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/LocationRed_C.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("**Seattle**"),
                                TextBlock("8p", spacing=SpacingStyle.NONE)
                            ],
                            width=Width.AUTO
                        )
                    ]
                )
            ],
            spacing=SpacingStyle.LARGE,
            separator=True,
            width=1
        )
    ]
)
column_set2 = ColumnSet(
    columns=[
        Column(
            items=[
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image(
                                    "http://messagecardplayground.azurewebsites.net/assets/Conflict.png",
                                    horizontal_alignment=HorizontalAlignment.LEFT
                                )
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("2:00 PM")
                            ],
                            spacing=SpacingStyle.NONE,
                            width=Width.STRETCH
                        )
                    ]
                ),
                TextBlock("1hr", spacing=SpacingStyle.NONE, is_subtle=True)
            ],
            width="110px"
        ),
        Column(
            items=[
                Image(
                    "http://messagecardplayground.azurewebsites.net/assets/CircleGreen_coffee.png",
                    horizontal_alignment=HorizontalAlignment.CENTER, 
                )
            ],
            background_image=BackgroundImage(
                "http://messagecardplayground.azurewebsites.net/assets/SmallVerticalLineGray.png",
                fill_mode=FillMode.REPEAT_VERTICALLY, horizontal_alignment=HorizontalAlignment.CENTER
            ),
            width=Width.AUTO,
            spacing=SpacingStyle.NONE
        ),
        Column(
            items=[
                TextBlock("**Contoso Campaign Status Meeting**"),
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/location_gray.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("Conf Room Bravern-2/9050")
                            ],
                            width=Width.STRETCH
                        )
                    ],
                    spacing=SpacingStyle.NONE
                ),
                ImageSet(
                    images=[
                        Image("http://messagecardplayground.azurewebsites.net/assets/person_w1.png", size=ImageSize.SMALL),
                        Image("http://messagecardplayground.azurewebsites.net/assets/person_m1.png", size=ImageSize.SMALL),
                        Image("http://messagecardplayground.azurewebsites.net/assets/person_w2.png", size=ImageSize.SMALL),
                    ],
                    spacing=SpacingStyle.SMALL,
                    image_size=ImageSize.SMALL
                ),
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/power_point.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("**Contoso Brand Guidelines** shared by **Susan Metters**")
                            ],
                            width=Width.STRETCH
                        )
                    ],
                    spacing=SpacingStyle.SMALL
                )
            ],
            width=40
        )
    ]
)
column_set3 = ColumnSet(
    columns=[
        Column(width="110px"),
        Column(
            background_image=BackgroundImage(
                "http://messagecardplayground.azurewebsites.net/assets/SmallVerticalLineGray.png",
                fill_mode=FillMode.REPEAT_VERTICALLY, horizontal_alignment=HorizontalAlignment.CENTER
            ),
            items=[
                Image(
                    "http://messagecardplayground.azurewebsites.net/assets/Gray_Dot.png",
                    horizontal_alignment=HorizontalAlignment.CENTER
                )
            ],
            width=Width.AUTO,
            spacing=SpacingStyle.NONE
        ),
        Column(
            items=[
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/car.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("about 45 minutes", is_subtle=True)
                            ],
                            width=Width.STRETCH
                        )
                    ]
                )
            ],
            width=40
        )
    ]
)
column_set4 = ColumnSet(
    columns=[
        Column(
            items=[
                TextBlock("8:00 PM", spacing=SpacingStyle.NONE),
                TextBlock("1hr", spacing=SpacingStyle.NONE, is_subtle=True)
            ],
            width="110px"
        ),
        Column(
            items=[
                Image(
                    "http://messagecardplayground.azurewebsites.net/assets/CircleBlue_flight.png",
                    horizontal_alignment=HorizontalAlignment.CENTER
                )
            ],
            background_image=BackgroundImage(
                "http://messagecardplayground.azurewebsites.net/assets/SmallVerticalLineGray.png",
                fill_mode=FillMode.REPEAT_VERTICALLY, horizontal_alignment=HorizontalAlignment.CENTER
            ),
            width=Width.AUTO,
            spacing=SpacingStyle.NONE
        ),
        Column(
            items=[
                TextBlock("**Alaska Airlines AS1021 flight to Chicago**"),
                ColumnSet(
                    columns=[
                        Column(
                            items=[
                                Image("http://messagecardplayground.azurewebsites.net/assets/location_gray.png")
                            ],
                            width=Width.AUTO
                        ),
                        Column(
                            items=[
                                TextBlock("Seattle Tacoma International Airport (17801 International Blvd, "
                                          "Seattle, WA, United States)", wrap=True)
                            ],
                            width=Width.STRETCH
                        )
                    ],
                    spacing=SpacingStyle.NONE
                ),
                Image("http://messagecardplayground.azurewebsites.net/assets/SeaTacMap.png", size=ImageSize.STRETCH)
            ],
            width=40
        )
    ]
)

agenda = AdaptiveCard(version="1.0", schema=SCHEMA)
agenda.add_elements([
    column_set1,
    column_set2,
    column_set3,
    column_set4
])
