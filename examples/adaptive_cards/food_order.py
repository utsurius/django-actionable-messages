from django_actionable_messages.adaptive_card.actions import Submit, ShowCard
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.containers import ImageSet
from django_actionable_messages.adaptive_card.elements import TextBlock, Image
from django_actionable_messages.adaptive_card.inputs import TextInput, ToggleInput, InputChoice, ChoiceSetInput
from django_actionable_messages.adaptive_card.utils import SCHEMA, FontSize, FontWeight

"""
https://adaptivecards.io/samples/FoodOrder.html
"""


adaptive_card1 = AdaptiveCard()
adaptive_card1.add_elements([
    TextBlock("How would you like your steak prepared?", size=FontSize.MEDIUM, wrap=True),
    ChoiceSetInput(
        item_id="SteakTemp",
        choices=[
            InputChoice("Rare", "rare"),
            InputChoice("Medium-rare", "medium-rare"),
            InputChoice("Well-done", "well-done")
        ]
    ),
    TextInput(item_id="SteakOther", is_multiline=True, placeholder="Any other preparation requests?")
])
adaptive_card1.add_actions(Submit(title="OK", data={"FoodChoice": "Steak"}))
adaptive_card2 = AdaptiveCard()
adaptive_card2.add_elements([
    TextBlock("Do you have any allergies?", size=FontSize.MEDIUM, wrap=True),
    ChoiceSetInput(
        item_id="ChickenAllergy",
        choices=[
            InputChoice("I'm allergic to peanuts", "peanut")
        ]
    ),
    TextInput(item_id="ChickenOther", is_multiline=True, placeholder="Any other preparation requests?")
])
adaptive_card2.add_actions(Submit(title="OK", data={"FoodChoice": "Chicken"}))
adaptive_card3 = AdaptiveCard()
adaptive_card3.add_elements([
    TextBlock("Would you like it prepared vegan?", size=FontSize.MEDIUM, wrap=True),
    ToggleInput(item_id="Vegetarian", title="Please prepare it vegan", value_on="vegan", value_off="notVegan"),
    TextInput(item_id="VegOther", is_multiline=True, placeholder="Any other preparation requests?")
])
adaptive_card3.add_actions(Submit(title="OK", data={"FoodChoice": "Chicken"}))

food_order = AdaptiveCard(version="1.0", schema=SCHEMA)
food_order.add_elements([
    TextBlock("Your registration is almost complete", size=FontSize.MEDIUM, weight=FontWeight.BOLDER),
    TextBlock("What type of food do you prefer?", wrap=True),
    ImageSet(images=[
        Image("http://contososcubademo.azurewebsites.net/assets/steak.jpg"),
        Image("http://contososcubademo.azurewebsites.net/assets/chicken.jpg"),
        Image("http://contososcubademo.azurewebsites.net/assets/tofu.jpg")
    ])
])
food_order.add_actions([
    ShowCard(title="Steak", card=adaptive_card1),
    ShowCard(title="Chicken", card=adaptive_card2),
    ShowCard(title="Tofu", card=adaptive_card3)
])
