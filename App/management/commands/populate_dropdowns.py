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
            ('Mobile App Development', 'mobile_app_development', 4),
            ('Education & Training', 'education_training', 5),
            ('Healthcare & Medical', 'healthcare_medical', 6),
            ('Marketing & Sales', 'marketing_sales', 7),
            ('Data Science & Analytics', 'data_science_analytics', 8),
            ('Customer Support', 'customer_support', 9),
            ('Human Resources', 'human_resources', 10),
            ('Finance & Accounting', 'finance_accounting', 11),
            ('DevOps & Cloud Computing', 'devops_cloud_computing', 12),
            ('Cybersecurity', 'cybersecurity', 13),
            ('Artificial Intelligence & Machine Learning', 'ai_machine_learning', 14),
            ('Blockchain & Cryptocurrency', 'blockchain_cryptocurrency', 15),
            ('Quality Assurance & Testing', 'qa_testing', 16),
            ('Project Management', 'project_management', 17),
            ('Business Analysis', 'business_analysis', 18),
            ('Legal & Compliance', 'legal_compliance', 19),
            ('Architecture & Engineering', 'architecture_engineering', 20),
            ('Content Writing & Copywriting', 'content_writing', 21),
            ('Graphic Design & Multimedia', 'graphic_design', 22),
            ('Video Production & Editing', 'video_production', 23),
            ('Supply Chain & Logistics', 'supply_chain_logistics', 24),
            ('Real Estate', 'real_estate', 25),
            ('Hospitality & Tourism', 'hospitality_tourism', 26),
            ('Retail & E-commerce', 'retail_ecommerce', 27),
            ('Manufacturing & Production', 'manufacturing_production', 28),
            ('Telecommunications', 'telecommunications', 29),
            ('Energy & Utilities', 'energy_utilities', 30),
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
            ('Temporary', 'temporary', 6),
            ('Remote', 'remote', 7),
            ('Hybrid', 'hybrid', 8),
            ('Consultant', 'consultant', 9),
            ('Volunteer', 'volunteer', 10),
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
            ('Lead', 'lead', 5),
            ('Team Leader', 'team_leader', 6),
            ('Manager', 'manager', 7),
            ('Senior Manager', 'senior_manager', 8),
            ('Director', 'director', 9),
            ('Senior Director', 'senior_director', 10),
            ('Vice President', 'vice_president', 11),
            ('Senior Vice President', 'senior_vice_president', 12),
            ('Executive', 'executive', 13),
            ('C-Level (CEO, CTO, CFO)', 'c_level', 14),
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
            ('Less than 1 Year', 'less_than_1_year', 2),
            ('1+ Years', '1plus_years', 3),
            ('2+ Years', '2plus_years', 4),
            ('3+ Years', '3plus_years', 5),
            ('4+ Years', '4plus_years', 6),
            ('5+ Years', '5plus_years', 7),
            ('6+ Years', '6plus_years', 8),
            ('7+ Years', '7plus_years', 9),
            ('8+ Years', '8plus_years', 10),
            ('9+ Years', '9plus_years', 11),
            ('10+ Years', '10plus_years', 12),
            ('12+ Years', '12plus_years', 13),
            ('15+ Years', '15plus_years', 14),
            ('20+ Years', '20plus_years', 15),
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
            ('No Formal Education', 'no_formal_education', 1),
            ('High School', 'high_school', 2),
            ('10th Class', '10th_class', 3),
            ('12th Class', '12th_class', 4),
            ('Diploma', 'diploma', 5),
            ('Associate Degree', 'associate_degree', 6),
            ("Bachelor's Degree (BA/BS/BTech)", 'bachelors_degree', 7),
            ("Master's Degree (MA/MS/MTech)", 'masters_degree', 8),
            ('MBA', 'mba', 9),
            ('Post Graduate Diploma', 'post_graduate_diploma', 10),
            ('PhD/Doctorate', 'phd', 11),
            ('Professional Certification (PMP, AWS, etc.)', 'professional_certification', 12),
            ('Medical Degree (MD/MBBS)', 'medical_degree', 13),
            ('Law Degree (LLB/JD)', 'law_degree', 14),
            ('Engineering Degree', 'engineering_degree', 15),
            ('Vocational Training', 'vocational_training', 16),
            ('Trade School Certificate', 'trade_school', 17),
            ('Any Graduate', 'any_graduate', 18),
            ('Any Post Graduate', 'any_post_graduate', 19),
            ('Other', 'other', 20),
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
            ('United Arab Emirates', 'uae', 9),
            ('Russia', 'russia', 10),
            ('China', 'china', 11),
            ('Japan', 'japan', 12),
            ('Brazil', 'brazil', 13),
            ('Mexico', 'mexico', 14),
            ('Netherlands', 'netherlands', 15),
            ('Spain', 'spain', 16),
            ('Italy', 'italy', 17),
            ('South Korea', 'south_korea', 18),
            ('Switzerland', 'switzerland', 19),
            ('Sweden', 'sweden', 20),
            ('Norway', 'norway', 21),
            ('Denmark', 'denmark', 22),
            ('Ireland', 'ireland', 23),
            ('New Zealand', 'new_zealand', 24),
            ('South Africa', 'south_africa', 25),
            ('Israel', 'israel', 26),
            ('Saudi Arabia', 'saudi_arabia', 27),
            ('Malaysia', 'malaysia', 28),
            ('Thailand', 'thailand', 29),
            ('Indonesia', 'indonesia', 30),
            ('Philippines', 'philippines', 31),
            ('Vietnam', 'vietnam', 32),
            ('Poland', 'poland', 33),
            ('Turkey', 'turkey', 34),
            ('Argentina', 'argentina', 35),
            ('Chile', 'chile', 36),
            ('Colombia', 'colombia', 37),
            ('Egypt', 'egypt', 38),
            ('Pakistan', 'pakistan', 39),
            ('Bangladesh', 'bangladesh', 40),
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
            # US States
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
            ('Virginia', 'virginia', 16),
            ('New Jersey', 'new_jersey', 17),
            ('Maryland', 'maryland', 18),
            ('Wisconsin', 'wisconsin', 19),
            ('Minnesota', 'minnesota', 20),
            # Major Indian Cities
            ('Mumbai', 'mumbai', 21),
            ('Delhi', 'delhi', 22),
            ('Bangalore', 'bangalore', 23),
            ('Hyderabad', 'hyderabad', 24),
            ('Chennai', 'chennai', 25),
            ('Pune', 'pune', 26),
            ('Kolkata', 'kolkata', 27),
            ('Ahmedabad', 'ahmedabad', 28),
            ('Gurugram', 'gurugram', 29),
            ('Noida', 'noida', 30),
            # UK Cities
            ('London', 'london', 31),
            ('Manchester', 'manchester', 32),
            ('Birmingham', 'birmingham', 33),
            ('Edinburgh', 'edinburgh', 34),
            # Other Major Cities
            ('Toronto', 'toronto', 35),
            ('Vancouver', 'vancouver', 36),
            ('Sydney', 'sydney', 37),
            ('Melbourne', 'melbourne', 38),
            ('Dubai', 'dubai', 39),
            ('Singapore City', 'singapore_city', 40),
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

        # Skills Group
        skills_group = DropdownGroup.objects.create(
            text='Skills',
            value='skills'
        )
        skills_items = [
            ('JavaScript', 'javascript', 1),
            ('Python', 'python', 2),
            ('Java', 'java', 3),
            ('C#', 'csharp', 4),
            ('C++', 'cplusplus', 5),
            ('PHP', 'php', 6),
            ('Ruby', 'ruby', 7),
            ('Go', 'go', 8),
            ('Swift', 'swift', 9),
            ('Kotlin', 'kotlin', 10),
            ('React.js', 'reactjs', 11),
            ('Angular', 'angular', 12),
            ('Vue.js', 'vuejs', 13),
            ('Node.js', 'nodejs', 14),
            ('Django', 'django', 15),
            ('Flask', 'flask', 16),
            ('Spring Boot', 'spring_boot', 17),
            ('ASP.NET', 'aspnet', 18),
            ('SQL', 'sql', 19),
            ('MongoDB', 'mongodb', 20),
            ('PostgreSQL', 'postgresql', 21),
            ('MySQL', 'mysql', 22),
            ('Redis', 'redis', 23),
            ('AWS', 'aws', 24),
            ('Azure', 'azure', 25),
            ('Google Cloud', 'google_cloud', 26),
            ('Docker', 'docker', 27),
            ('Kubernetes', 'kubernetes', 28),
            ('Git', 'git', 29),
            ('CI/CD', 'cicd', 30),
            ('Machine Learning', 'machine_learning', 31),
            ('Deep Learning', 'deep_learning', 32),
            ('Data Analysis', 'data_analysis', 33),
            ('Power BI', 'power_bi', 34),
            ('Tableau', 'tableau', 35),
            ('Excel', 'excel', 36),
            ('Project Management', 'project_management', 37),
            ('Agile/Scrum', 'agile_scrum', 38),
            ('Communication', 'communication', 39),
            ('Leadership', 'leadership', 40),
        ]
        for text, value, order in skills_items:
            DropdownMaster.objects.create(
                group=skills_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Skills group with {len(skills_items)} items'))

        # Salary Range Group
        salary_range_group = DropdownGroup.objects.create(
            text='Salary Range',
            value='salary_range'
        )
        salary_range_items = [
            ('Below $20,000', 'below_20k', 1),
            ('$20,000 - $30,000', '20k_30k', 2),
            ('$30,000 - $40,000', '30k_40k', 3),
            ('$40,000 - $50,000', '40k_50k', 4),
            ('$50,000 - $60,000', '50k_60k', 5),
            ('$60,000 - $70,000', '60k_70k', 6),
            ('$70,000 - $80,000', '70k_80k', 7),
            ('$80,000 - $90,000', '80k_90k', 8),
            ('$90,000 - $100,000', '90k_100k', 9),
            ('$100,000 - $120,000', '100k_120k', 10),
            ('$120,000 - $150,000', '120k_150k', 11),
            ('$150,000 - $200,000', '150k_200k', 12),
            ('$200,000 - $250,000', '200k_250k', 13),
            ('$250,000+', '250k_plus', 14),
            ('Negotiable', 'negotiable', 15),
        ]
        for text, value, order in salary_range_items:
            DropdownMaster.objects.create(
                group=salary_range_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Salary Range group with {len(salary_range_items)} items'))

        # Work Mode Group
        work_mode_group = DropdownGroup.objects.create(
            text='Work Mode',
            value='work_mode'
        )
        work_mode_items = [
            ('Work from Office', 'work_from_office', 1),
            ('Work from Home', 'work_from_home', 2),
            ('Hybrid', 'hybrid', 3),
            ('Remote', 'remote', 4),
            ('Flexible', 'flexible', 5),
        ]
        for text, value, order in work_mode_items:
            DropdownMaster.objects.create(
                group=work_mode_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Work Mode group with {len(work_mode_items)} items'))

        # Company Size Group
        company_size_group = DropdownGroup.objects.create(
            text='Company Size',
            value='company_size'
        )
        company_size_items = [
            ('Startup (1-10 employees)', 'startup', 1),
            ('Small (11-50 employees)', 'small', 2),
            ('Medium (51-200 employees)', 'medium', 3),
            ('Large (201-500 employees)', 'large', 4),
            ('Enterprise (501-1000 employees)', 'enterprise', 5),
            ('Corporation (1000+ employees)', 'corporation', 6),
        ]
        for text, value, order in company_size_items:
            DropdownMaster.objects.create(
                group=company_size_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Company Size group with {len(company_size_items)} items'))

        # Industry Type Group
        industry_type_group = DropdownGroup.objects.create(
            text='Industry Type',
            value='industry_type'
        )
        industry_type_items = [
            ('Information Technology', 'information_technology', 1),
            ('Software Services', 'software_services', 2),
            ('Financial Services', 'financial_services', 3),
            ('Healthcare & Pharmaceuticals', 'healthcare_pharmaceuticals', 4),
            ('E-commerce & Retail', 'ecommerce_retail', 5),
            ('Education & E-learning', 'education_elearning', 6),
            ('Manufacturing', 'manufacturing', 7),
            ('Telecommunications', 'telecommunications', 8),
            ('Consulting', 'consulting', 9),
            ('Media & Entertainment', 'media_entertainment', 10),
            ('Real Estate', 'real_estate', 11),
            ('Automotive', 'automotive', 12),
            ('Energy & Utilities', 'energy_utilities', 13),
            ('Transportation & Logistics', 'transportation_logistics', 14),
            ('Hospitality & Travel', 'hospitality_travel', 15),
            ('Agriculture', 'agriculture', 16),
            ('Construction', 'construction', 17),
            ('Government & Public Sector', 'government_public_sector', 18),
            ('Non-Profit', 'non_profit', 19),
            ('Other', 'other', 20),
        ]
        for text, value, order in industry_type_items:
            DropdownMaster.objects.create(
                group=industry_type_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Industry Type group with {len(industry_type_items)} items'))

        # Notice Period Group
        notice_period_group = DropdownGroup.objects.create(
            text='Notice Period',
            value='notice_period'
        )
        notice_period_items = [
            ('Immediate Joiner', 'immediate', 1),
            ('15 Days', '15_days', 2),
            ('30 Days', '30_days', 3),
            ('45 Days', '45_days', 4),
            ('60 Days', '60_days', 5),
            ('90 Days', '90_days', 6),
            ('Negotiable', 'negotiable', 7),
        ]
        for text, value, order in notice_period_items:
            DropdownMaster.objects.create(
                group=notice_period_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Notice Period group with {len(notice_period_items)} items'))

        # Language Proficiency Group
        language_group = DropdownGroup.objects.create(
            text='Languages',
            value='languages'
        )
        language_items = [
            ('English', 'english', 1),
            ('Spanish', 'spanish', 2),
            ('French', 'french', 3),
            ('German', 'german', 4),
            ('Chinese (Mandarin)', 'chinese_mandarin', 5),
            ('Hindi', 'hindi', 6),
            ('Arabic', 'arabic', 7),
            ('Portuguese', 'portuguese', 8),
            ('Russian', 'russian', 9),
            ('Japanese', 'japanese', 10),
            ('Korean', 'korean', 11),
            ('Italian', 'italian', 12),
            ('Dutch', 'dutch', 13),
            ('Swedish', 'swedish', 14),
            ('Polish', 'polish', 15),
        ]
        for text, value, order in language_items:
            DropdownMaster.objects.create(
                group=language_group,
                text=text,
                value=value,
                sort_order=order
            )
        self.stdout.write(self.style.SUCCESS(f'Created Languages group with {len(language_items)} items'))

        self.stdout.write(self.style.SUCCESS('\n=== Successfully populated all dropdown data! ==='))
        
        # Display summary
        total_groups = DropdownGroup.objects.filter(is_active=True).count()
        total_items = DropdownMaster.objects.filter(is_active=True).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(f'Total Groups Created: {total_groups}')
        self.stdout.write(f'Total Items Created: {total_items}')

