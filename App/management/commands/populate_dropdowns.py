from django.core.management.base import BaseCommand
from App.models import DropdownGroup, DropdownMaster


class Command(BaseCommand):
    help = 'Populate dropdown groups and master data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating dropdown data...')

        # Clear existing data
        DropdownMaster.objects.all().delete()
        DropdownGroup.objects.all().delete()

        # Education Group
        education_group = DropdownGroup.objects.create(
            text='Education',
            value='Education'
        )
        education_items = [
            ('High School', 'High School', 1),
            ('Intermediate', 'Intermediate', 2),
            ("Bachelor's Degree", "Bachelor's Degree", 3),
            ("Master's Degree", "Master's Degree", 4),
            ('Post Graduate', 'Post Graduate', 5),
            ('PhD', 'PhD', 6),
        ]
        for text, value, order in education_items:
            DropdownMaster.objects.create(
                group=education_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Education group with {len(education_items)} items'))

        # Experience Group
        experience_group = DropdownGroup.objects.create(
            text='Experience',
            value='Experience'
        )
        experience_items = [
            ('Fresher', 'Fresher', 1),
            ('1+ Year', '1+ Year', 2),
            ('2+ Years', '2+ Years', 3),
            ('3+ Years', '3+ Years', 4),
            ('4+ Years', '4+ Years', 5),
            ('5+ Years', '5+ Years', 6),
            ('7+ Years', '7+ Years', 7),
            ('10+ Years', '10+ Years', 8),
        ]
        for text, value, order in experience_items:
            DropdownMaster.objects.create(
                group=experience_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Experience group with {len(experience_items)} items'))

        # Country Group
        country_group = DropdownGroup.objects.create(
            text='Country',
            value='Country'
        )
        country_items = [
            ('India', 'India', 1),
            ('United States', 'United States', 2),
            ('United Kingdom', 'United Kingdom', 3),
            ('Australia', 'Australia', 4),
            ('Russia', 'Russia', 5),
            ('Canada', 'Canada', 6),
            ('Germany', 'Germany', 7),
            ('France', 'France', 8),
            ('China', 'China', 9),
            ('Japan', 'Japan', 10),
        ]
        for text, value, order in country_items:
            DropdownMaster.objects.create(
                group=country_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Country group with {len(country_items)} items'))

        # State/City Group
        city_group = DropdownGroup.objects.create(
            text='State/City',
            value='State/City'
        )
        city_items = [
            ('California', 'California', 1),
            ('Denver', 'Denver', 2),
            ('New York', 'New York', 3),
            ('Toronto', 'Toronto', 4),
            ('Warsaw', 'Warsaw', 5),
            ('Mumbai', 'Mumbai', 6),
            ('Delhi', 'Delhi', 7),
            ('Bangalore', 'Bangalore', 8),
            ('London', 'London', 9),
            ('Sydney', 'Sydney', 10),
        ]
        for text, value, order in city_items:
            DropdownMaster.objects.create(
                group=city_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created State/City group with {len(city_items)} items'))

        self.stdout.write(self.style.SUCCESS('Successfully populated all dropdown data!'))
