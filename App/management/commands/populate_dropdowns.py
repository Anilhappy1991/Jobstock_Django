from django.core.management.base import BaseCommand
from App.models import DropdownGroup, DropdownMaster


class Command(BaseCommand):
    help = 'Populate dropdown groups and master data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating dropdown data...')

        # Clear existing data
        DropdownMaster.objects.all().delete()
        DropdownGroup.objects.all().delete()

        # Job Category Group
        job_category_group = DropdownGroup.objects.create(
            text='Job Category',
            value='job_category'
        )
        job_category_items = [
            ('Web & Application Development', 'web_application_development', 1),
            ('Banking Services', 'banking_services', 2),
            ('UI/UX Design', 'ui_ux_design', 3),
            ('IOS/App Application', 'ios_app_application', 4),
            ('Education & Training', 'education_training', 5),
            ('Healthcare', 'healthcare', 6),
            ('Marketing & Sales', 'marketing_sales', 7),
            ('Data Science & Analytics', 'data_science_analytics', 8),
            ('Customer Support', 'customer_support', 9),
            ('Human Resources', 'human_resources', 10),
        ]
        for text, value, order in job_category_items:
            DropdownMaster.objects.create(
                group=job_category_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Job Category group with {len(job_category_items)} items'))

        # Job Type Group
        job_type_group = DropdownGroup.objects.create(
            text='Job Type',
            value='job_type'
        )
        job_type_items = [
            ('Full Time', 'full_time', 1),
            ('Part Time', 'part_time', 2),
            ('Freelance', 'freelance', 3),
            ('Internship', 'internship', 4),
            ('Contract', 'contract', 5),
        ]
        for text, value, order in job_type_items:
            DropdownMaster.objects.create(
                group=job_type_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Job Type group with {len(job_type_items)} items'))

        # Job Level Group
        job_level_group = DropdownGroup.objects.create(
            text='Job Level',
            value='job_level'
        )
        job_level_items = [
            ('Entry Level', 'entry_level', 1),
            ('Junior', 'junior', 2),
            ('Mid Level', 'mid_level', 3),
            ('Senior', 'senior', 4),
            ('Team Leader', 'team_leader', 5),
            ('Manager', 'manager', 6),
            ('Director', 'director', 7),
            ('Executive', 'executive', 8),
        ]
        for text, value, order in job_level_items:
            DropdownMaster.objects.create(
                group=job_level_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Job Level group with {len(job_level_items)} items'))

        # Experience Group
        experience_group = DropdownGroup.objects.create(
            text='Experience',
            value='experience'
        )
        experience_items = [
            ('Fresher', 'fresher', 1),
            ('1+ Years', '1plus_years', 2),
            ('2+ Years', '2plus_years', 3),
            ('3+ Years', '3plus_years', 4),
            ('4+ Years', '4plus_years', 5),
            ('5+ Years', '5plus_years', 6),
            ('6+ Years', '6plus_years', 7),
            ('7+ Years', '7plus_years', 8),
            ('8+ Years', '8plus_years', 9),
            ('9+ Years', '9plus_years', 10),
            ('10+ Years', '10plus_years', 11),
        ]
        for text, value, order in experience_items:
            DropdownMaster.objects.create(
                group=experience_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Experience group with {len(experience_items)} items'))

        # Qualification Group
        qualification_group = DropdownGroup.objects.create(
            text='Qualification',
            value='qualification'
        )
        qualification_items = [
            ('High School', 'high_school', 1),
            ('10th Class', '10th_class', 2),
            ('12th Class', '12th_class', 3),
            ('Diploma', 'diploma', 4),
            ("Bachelor's Degree", 'bachelors_degree', 5),
            ("Master's Degree", 'masters_degree', 6),
            ('Post Graduate', 'post_graduate', 7),
            ('PhD', 'phd', 8),
            ('Professional Certification', 'professional_certification', 9),
            ('Any Other', 'any_other', 10),
        ]
        for text, value, order in qualification_items:
            DropdownMaster.objects.create(
                group=qualification_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Qualification group with {len(qualification_items)} items'))

        # Gender Group
        gender_group = DropdownGroup.objects.create(
            text='Gender',
            value='gender'
        )
        gender_items = [
            ('Male', 'male', 1),
            ('Female', 'female', 2),
            ('Other', 'other', 3),
            ('Prefer not to say', 'prefer_not_to_say', 4),
        ]
        for text, value, order in gender_items:
            DropdownMaster.objects.create(
                group=gender_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Gender group with {len(gender_items)} items'))

        # Total Openings Group
        total_openings_group = DropdownGroup.objects.create(
            text='Total Openings',
            value='total_openings'
        )
        total_openings_items = [
            ('01', '01', 1),
            ('02', '02', 2),
            ('03', '03', 3),
            ('04', '04', 4),
            ('05', '05', 5),
            ('06', '06', 6),
            ('07', '07', 7),
            ('08', '08', 8),
            ('09', '09', 9),
            ('10', '10', 10),
            ('10+', '10plus', 11),
        ]
        for text, value, order in total_openings_items:
            DropdownMaster.objects.create(
                group=total_openings_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Total Openings group with {len(total_openings_items)} items'))

        # Job Fee Type Group
        job_fee_type_group = DropdownGroup.objects.create(
            text='Job Fee Type',
            value='job_fee_type'
        )
        job_fee_type_items = [
            ('Free', 'free', 1),
            ('Premium', 'premium', 2),
            ('Urgent', 'urgent', 3),
            ('Featured', 'featured', 4),
        ]
        for text, value, order in job_fee_type_items:
            DropdownMaster.objects.create(
                group=job_fee_type_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Job Fee Type group with {len(job_fee_type_items)} items'))

        # Country Group
        country_group = DropdownGroup.objects.create(
            text='Country',
            value='country'
        )
        country_items = [
            ('United States', 'united_states', 1),
            ('United Kingdom', 'united_kingdom', 2),
            ('Canada', 'canada', 3),
            ('Australia', 'australia', 4),
            ('India', 'india', 5),
            ('Germany', 'germany', 6),
            ('France', 'france', 7),
            ('Singapore', 'singapore', 8),
            ('UAE', 'uae', 9),
            ('Russia', 'russia', 10),
            ('China', 'china', 11),
            ('Japan', 'japan', 12),
            ('Brazil', 'brazil', 13),
            ('Mexico', 'mexico', 14),
            ('Netherlands', 'netherlands', 15),
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
        state_city_group = DropdownGroup.objects.create(
            text='State/City',
            value='state_city'
        )
        state_city_items = [
            ('California', 'california', 1),
            ('New York', 'new_york', 2),
            ('Texas', 'texas', 3),
            ('Florida', 'florida', 4),
            ('Illinois', 'illinois', 5),
            ('Pennsylvania', 'pennsylvania', 6),
            ('Ohio', 'ohio', 7),
            ('Georgia', 'georgia', 8),
            ('Michigan', 'michigan', 9),
            ('North Carolina', 'north_carolina', 10),
            ('Washington', 'washington', 11),
            ('Colorado', 'colorado', 12),
            ('Massachusetts', 'massachusetts', 13),
            ('Arizona', 'arizona', 14),
            ('Tennessee', 'tennessee', 15),
        ]
        for text, value, order in state_city_items:
            DropdownMaster.objects.create(
                group=state_city_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created State/City group with {len(state_city_items)} items'))

        # Education Group (for backward compatibility)
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

        self.stdout.write(self.style.SUCCESS('\n=== Successfully populated all dropdown data! ==='))
        
        # Display summary
        total_groups = DropdownGroup.objects.filter(is_active=True).count()
        total_items = DropdownMaster.objects.filter(is_active=True).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(f'Total Groups Created: {total_groups}')
        self.stdout.write(f'Total Items Created: {total_items}')

