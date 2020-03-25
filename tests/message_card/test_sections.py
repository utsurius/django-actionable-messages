from django.test import TestCase

from django_actionable_messages.message_card.actions import OpenUri, HttpPOST
from django_actionable_messages.message_card.elements import HeroImage, Fact, ActionTarget
from django_actionable_messages.message_card.sections import Section
from django_actionable_messages.message_card.utils import OSType

URL = "https://www.example.com/"


class SectionTestCase(TestCase):
    def test_section(self):
        hero_image = HeroImage("https://www.example.com/image.png", "Image")
        facts = [Fact("First name", "John"), Fact("Last name", "Johnson")]
        actions = [OpenUri("Open", targets=[ActionTarget(OSType.DEFAULT, "https://www.sample.com/"), ]), ]
        section = Section(start_group=True, title="Section title", text="Duis aute irure dolor",  activity_image=URL,
                          activity_title="Activity", activity_subtitle="sample subtitle", activity_text="asdf",
                          hero_image=hero_image, facts=facts, actions=actions)
        self.assertDictEqual(section.as_data(), {
            "startGroup": True,
            "title": "Section title",
            "text": "Duis aute irure dolor",
            "activityImage": URL,
            "activityTitle": "Activity",
            "activitySubtitle": "sample subtitle",
            "activityText": "asdf",
            "heroImage": {
                "image": "https://www.example.com/image.png",
                "title": "Image"
            },
            "facts": [
                {"name": "First name", "value": "John"},
                {"name": "Last name", "value": "Johnson"}
            ],
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "Open",
                "targets": [
                    {"os": "default", "uri": "https://www.sample.com/"}
                ]
            }]
        })

    def test_section_start_group(self):
        section = Section()
        section.set_start_group()
        self.assertDictEqual(section.as_data(), {
            "startGroup": True
        })

    def test_section_set_title(self):
        section = Section()
        section.set_title("Section title")
        self.assertDictEqual(section.as_data(), {
            "title": "Section title"
        })

    def test_section_set_text(self):
        section = Section()
        section.set_text("Excepteur sint occaecat cupidatat non proident")
        self.assertDictEqual(section.as_data(), {
            "text": "Excepteur sint occaecat cupidatat non proident"
        })

    def test_section_set_activity(self):
        section = Section()
        section.set_activity(image=URL, title="Activity", subtitle="Activity subtitle", text="qwertz")
        self.assertDictEqual(section.as_data(), {
            "activityImage": URL,
            "activityTitle": "Activity",
            "activitySubtitle": "Activity subtitle",
            "activityText": "qwertz"
        })

    def test_section_set_activity_image(self):
        section = Section()
        section.set_activity_image("https://www.example.com/")
        self.assertDictEqual(section.as_data(), {
            "activityImage": "https://www.example.com/"
        })

    def test_section_set_activity_title(self):
        section = Section()
        section.set_activity_title("Example")
        self.assertDictEqual(section.as_data(), {
            "activityTitle": "Example"
        })

    def test_section_set_activity_subtitle(self):
        section = Section()
        section.set_activity_subtitle("Subtitle")
        self.assertDictEqual(section.as_data(), {
            "activitySubtitle": "Subtitle"
        })

    def test_section_set_activity_text(self):
        section = Section()
        section.set_activity_text("Asdf zxcv")
        self.assertDictEqual(section.as_data(), {
            "activityText": "Asdf zxcv"
        })

    def test_section_set_hero_image(self):
        section = Section()
        section.set_hero_image(HeroImage(URL, "Test"))
        self.assertDictEqual(section.as_data(), {
            "heroImage": {
                "image": URL,
                "title": "Test"
            }
        })

    def test_section_add_facts(self):
        section = Section()
        section.add_facts([Fact("first", "1st"), Fact("second", "2nd")])
        self.assertDictEqual(section.as_data(), {
            "facts": [
                {"name": "first", "value": "1st"},
                {"name": "second", "value": "2nd"}
            ]
        })
        section.add_facts(Fact("third", "3rd"))
        self.assertDictEqual(section.as_data(), {
            "facts": [
                {"name": "first", "value": "1st"},
                {"name": "second", "value": "2nd"},
                {"name": "third", "value": "3rd"}
            ]
        })

    def test_section_add_potential_actions(self):
        section = Section()
        actions = [HttpPOST("Open", target=URL), HttpPOST("Click", target="www.example.com", body="asdf")]
        section.add_potential_actions(actions)
        self.assertDictEqual(section.as_data(), {
            "potentialAction": [{
                "@type": "HttpPOST",
                "name": "Open",
                "target": URL
            }, {
                "@type": "HttpPOST",
                "name": "Click",
                "target": "www.example.com",
                "body": "asdf"
            }]
        })
        action = OpenUri("View", targets=[ActionTarget(OSType.IOS, "http://www.example.com/"), ])
        section.add_potential_actions(action)
        self.assertDictEqual(section.as_data(), {
            "potentialAction": [{
                "@type": "HttpPOST",
                "name": "Open",
                "target": URL
            }, {
                "@type": "HttpPOST",
                "name": "Click",
                "target": "www.example.com",
                "body": "asdf"
            }, {
                "@type": "OpenUri",
                "name": "View",
                "targets": [
                    {"os": "iOS", "uri": "http://www.example.com/"}
                ]
            }]
        })
