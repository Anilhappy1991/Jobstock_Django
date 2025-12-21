"""
Generate 100 Diverse Job Posts for Jobstock Django
Inserts realistic job data into app_job table
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User
from App.models import Job, DropdownMaster
from django.utils.text import slugify

# Job Data Templates
JOB_TEMPLATES = [
    {
        'title': 'Senior Python Developer',
        'category': 'IT & Software',
        'type': 'Full Time',
        'level': 'Senior Level',
        'skills': 'Python, Django, Flask, PostgreSQL, Redis, Docker',
        'summary': 'We are looking for an experienced Python Developer to join our growing team. You will be responsible for developing high-quality applications using Python frameworks.',
        'responsibilities': '• Design and implement scalable Python applications\n• Write clean, maintainable code\n• Collaborate with cross-functional teams\n• Participate in code reviews\n• Troubleshoot and debug applications',
        'qualifications': '• 5+ years of Python development experience\n• Strong knowledge of Django/Flask\n• Experience with PostgreSQL and Redis\n• Understanding of Docker and containerization\n• Bachelor\'s degree in Computer Science or related field',
        'min_salary': 800000, 'max_salary': 1500000, 'experience': '5-7 Years'
    },
    {
        'title': 'Full Stack JavaScript Developer',
        'category': 'IT & Software',
        'type': 'Full Time',
        'level': 'Mid Level',
        'skills': 'JavaScript, React, Node.js, MongoDB, Express.js, TypeScript',
        'summary': 'Join our dynamic team as a Full Stack Developer. Work on cutting-edge web applications using modern JavaScript technologies.',
        'responsibilities': '• Develop frontend using React and TypeScript\n• Build backend APIs with Node.js and Express\n• Integrate with MongoDB databases\n• Implement responsive designs\n• Optimize application performance',
        'qualifications': '• 3+ years of JavaScript development\n• Proficiency in React and Node.js\n• Experience with MongoDB\n• Knowledge of RESTful APIs\n• Good communication skills',
        'min_salary': 600000, 'max_salary': 1200000, 'experience': '3-5 Years'
    },
    {
        'title': 'Data Scientist',
        'category': 'Data Science',
        'type': 'Full Time',
        'level': 'Senior Level',
        'skills': 'Python, Machine Learning, TensorFlow, Pandas, NumPy, SQL',
        'summary': 'Seeking a talented Data Scientist to analyze complex data sets and develop predictive models that drive business decisions.',
        'responsibilities': '• Analyze large datasets to extract insights\n• Build machine learning models\n• Create data visualizations and reports\n• Collaborate with stakeholders\n• Present findings to management',
        'qualifications': '• Master\'s degree in Data Science or related field\n• 4+ years of experience in data analysis\n• Strong Python and SQL skills\n• Experience with ML frameworks\n• Excellent analytical abilities',
        'min_salary': 1000000, 'max_salary': 1800000, 'experience': '5-7 Years'
    },
    {
        'title': 'DevOps Engineer',
        'category': 'IT & Software',
        'type': 'Full Time',
        'level': 'Mid Level',
        'skills': 'AWS, Docker, Kubernetes, Jenkins, Terraform, Linux',
        'summary': 'Looking for a DevOps Engineer to manage our cloud infrastructure and implement CI/CD pipelines.',
        'responsibilities': '• Manage AWS cloud infrastructure\n• Implement CI/CD pipelines\n• Containerize applications using Docker\n• Orchestrate containers with Kubernetes\n• Monitor system performance',
        'qualifications': '• 3+ years in DevOps role\n• Strong AWS knowledge\n• Experience with Docker and Kubernetes\n• Proficiency in scripting (Bash/Python)\n• Understanding of infrastructure as code',
        'min_salary': 700000, 'max_salary': 1400000, 'experience': '3-5 Years'
    },
    {
        'title': 'UI/UX Designer',
        'category': 'Design',
        'type': 'Full Time',
        'level': 'Mid Level',
        'skills': 'Figma, Adobe XD, Sketch, HTML, CSS, User Research',
        'summary': 'Creative UI/UX Designer needed to craft beautiful and intuitive user experiences for our digital products.',
        'responsibilities': '• Design user interfaces for web and mobile\n• Conduct user research and testing\n• Create wireframes and prototypes\n• Collaborate with developers\n• Maintain design systems',
        'qualifications': '• 3+ years of UI/UX design experience\n• Proficiency in Figma and Adobe XD\n• Strong portfolio demonstrating design skills\n• Understanding of HTML/CSS\n• Excellent visual design skills',
        'min_salary': 500000, 'max_salary': 1000000, 'experience': '3-5 Years'
    },
    {
        'title': 'Frontend Developer - React',
        'category': 'IT & Software',
        'type': 'Full Time',
        'level': 'Junior Level',
        'skills': 'React, JavaScript, HTML, CSS, Redux, Git',
        'summary': 'Entry-level frontend developer position for building modern web applications with React.',
        'responsibilities': '• Develop user interfaces with React\n• Implement responsive designs\n• Work with REST APIs\n• Write unit tests\n• Participate in agile ceremonies',
        'qualifications': '• 1-2 years of React experience\n• Strong JavaScript fundamentals\n• Knowledge of HTML5 and CSS3\n• Familiarity with Git\n• Bachelor\'s degree preferred',
        'min_salary': 300000, 'max_salary': 600000, 'experience': '1-2 Years'
    },
    {
        'title': 'Backend Developer - Java',
        'category': 'IT & Software',
        'type': 'Full Time',
        'level': 'Mid Level',
        'skills': 'Java, Spring Boot, Hibernate, MySQL, REST API, Microservices',
        'summary': 'Join our backend team to build scalable microservices using Java and Spring Boot.',
        'responsibilities': '• Develop REST APIs using Spring Boot\n• Design microservices architecture\n• Optimize database queries\n• Write comprehensive tests\n• Document APIs',
        'qualifications': '• 3+ years of Java development\n• Strong Spring Boot experience\n• Knowledge of Hibernate ORM\n• Experience with MySQL/PostgreSQL\n• Understanding of microservices',
        'min_salary': 650000, 'max_salary': 1300000, 'experience': '3-5 Years'
    },
    {
        'title': 'Mobile App Developer - Flutter',
        'category': 'Mobile Development',
        'type': 'Full Time',
        'level': 'Mid Level',
        'skills': 'Flutter, Dart, Firebase, REST API, Git',
        'summary': 'Develop cross-platform mobile applications using Flutter for iOS and Android.',
        'responsibilities': '• Build mobile apps with Flutter\n• Integrate with backend APIs\n• Implement Firebase features\n• Optimize app performance\n• Publish apps to stores',
        'qualifications': '• 2+ years of Flutter development\n• Strong Dart programming skills\n• Experience with Firebase\n• Knowledge of iOS/Android platforms\n• Published apps portfolio',
        'min_salary': 550000, 'max_salary': 1100000, 'experience': '2-4 Years'
    },
    {
        'title': 'QA Automation Engineer',
        'category': 'Testing',
        'type': 'Full Time',
        'level': 'Mid Level',
        'skills': 'Selenium, Python, Pytest, Jenkins, API Testing',
        'summary': 'Quality Assurance Engineer to design and implement automated testing frameworks.',
        'responsibilities': '• Develop automated test scripts\n• Perform API testing\n• Execute test plans\n• Report and track bugs\n• Maintain test frameworks',
        'qualifications': '• 3+ years of QA automation experience\n• Proficiency in Selenium and Python\n• Knowledge of CI/CD pipelines\n• Experience with API testing tools\n• Detail-oriented mindset',
        'min_salary': 450000, 'max_salary': 900000, 'experience': '3-5 Years'
    },
    {
        'title': 'Product Manager',
        'category': 'Management',
        'type': 'Full Time',
        'level': 'Senior Level',
        'skills': 'Product Strategy, Agile, JIRA, User Stories, Stakeholder Management',
        'summary': 'Strategic Product Manager to lead product development and drive product vision.',
        'responsibilities': '• Define product roadmap and strategy\n• Gather and prioritize requirements\n• Work with engineering teams\n• Analyze market trends\n• Present to stakeholders',
        'qualifications': '• 5+ years in product management\n• Strong analytical skills\n• Experience with agile methodologies\n• Excellent communication abilities\n• MBA preferred',
        'min_salary': 1200000, 'max_salary': 2500000, 'experience': '5-7 Years'
    }
]

COMPANIES = [
    'Infosys', 'TCS', 'Wipro', 'HCL Technologies', 'Tech Mahindra', 'Cognizant',
    'Accenture', 'IBM India', 'Microsoft India', 'Google India', 'Amazon India',
    'Oracle India', 'Adobe India', 'Cisco India', 'Intel India', 'SAP Labs',
    'Capgemini', 'Deloitte', 'EY', 'PwC India', 'KPMG India', 'Flipkart',
    'Paytm', 'Zomato', 'Swiggy', 'Ola', 'PhonePe', 'Myntra', 'Snapdeal',
    'MakeMyTrip', 'Freshworks', 'Zoho Corporation', 'Fractal Analytics',
    'Mu Sigma', 'Genpact', 'WNS Global', 'Concentrix', 'Mindtree', 'Mphasis'
]

CITIES = [
    'Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Delhi', 'Noida',
    'Gurugram', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Chandigarh', 'Kochi',
    'Coimbatore', 'Indore', 'Bhopal', 'Nagpur', 'Visakhapatnam'
]

def get_or_create_dropdown(group_value, text_value):
    """Get or create a dropdown master entry"""
    try:
        return DropdownMaster.objects.filter(
            group__value=group_value,
            text__icontains=text_value
        ).first()
    except:
        return None

def generate_job_from_template(template, index, user):
    """Generate a job posting from template"""
    company = random.choice(COMPANIES)
    city = random.choice(CITIES)
    
    # Calculate dates
    days_ago = random.randint(1, 90)
    start_date = datetime.now().date() - timedelta(days=days_ago)
    deadline_days = random.randint(15, 60)
    deadline = start_date + timedelta(days=deadline_days)
    
    # Create unique title
    unique_title = f"{template['title']} - {company}"
    if index > len(JOB_TEMPLATES):
        unique_title = f"{template['title']} #{index}"
    
    # Get dropdown values
    job_category = get_or_create_dropdown('job_category', template['category'])
    job_type = get_or_create_dropdown('job_type', template['type'])
    job_level = get_or_create_dropdown('job_level', template['level'])
    experience = get_or_create_dropdown('experience', template['experience'])
    city_dropdown = get_or_create_dropdown('state_city', city)
    country = get_or_create_dropdown('country', 'India')
    
    # Create job
    job = Job(
        title=unique_title,
        job_summary=template['summary'],
        responsibilities=template['responsibilities'],
        qualifications=template['qualifications'],
        job_category=job_category,
        job_type=job_type,
        job_level=job_level,
        experience_required=experience,
        skills=template['skills'],
        min_salary=Decimal(str(template['min_salary'])),
        max_salary=Decimal(str(template['max_salary'])),
        start_date=start_date,
        deadline=deadline,
        permanent_address=f"{company} Office, {city}",
        state_city=city_dropdown,
        country=country,
        posted_by=user,
        is_active=random.choice([True, True, True, False]),  # 75% active
        slug=slugify(unique_title)
    )
    
    return job

def main():
    print("="*80)
    print("GENERATING 100 JOB POSTS")
    print("="*80)
    
    # Get a user for posting (use first superuser or create one)
    try:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return
        
        print(f"\n✓ Using user: {user.username} (ID: {user.id})")
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return
    
    # Check existing jobs
    existing_count = Job.objects.count()
    print(f"✓ Existing jobs in database: {existing_count}")
    
    # Generate jobs
    jobs_created = 0
    jobs_to_create = []
    
    print(f"\nGenerating 100 job posts...")
    
    for i in range(1, 101):
        # Select template (cycle through templates)
        template_index = (i - 1) % len(JOB_TEMPLATES)
        template = JOB_TEMPLATES[template_index]
        
        try:
            job = generate_job_from_template(template, i, user)
            jobs_to_create.append(job)
            
            if i % 20 == 0:
                print(f"  ✓ Prepared {i} jobs...")
        except Exception as e:
            print(f"  ✗ Error preparing job {i}: {str(e)}")
    
    # Bulk create jobs
    print(f"\nInserting jobs into database...")
    try:
        Job.objects.bulk_create(jobs_to_create, ignore_conflicts=True)
        jobs_created = len(jobs_to_create)
        print(f"✓ Successfully inserted {jobs_created} jobs")
    except Exception as e:
        print(f"❌ Bulk insert failed: {e}")
        print("\nTrying individual inserts...")
        for i, job in enumerate(jobs_to_create, 1):
            try:
                job.save()
                jobs_created += 1
                if i % 20 == 0:
                    print(f"  ✓ Inserted {i} jobs...")
            except Exception as e:
                print(f"  ✗ Error inserting job {i}: {str(e)}")
    
    # Final stats
    final_count = Job.objects.count()
    new_jobs = final_count - existing_count
    
    print(f"\n{'='*80}")
    print("JOB INSERTION COMPLETE")
    print(f"{'='*80}")
    print(f"\nJobs before: {existing_count}")
    print(f"Jobs created: {new_jobs}")
    print(f"Jobs after: {final_count}")
    
    # Show breakdown
    print(f"\nBreakdown by status:")
    active = Job.objects.filter(is_active=True).count()
    inactive = Job.objects.filter(is_active=False).count()
    print(f"  • Active: {active}")
    print(f"  • Inactive: {inactive}")
    
    # Show sample jobs
    print(f"\nSample created jobs:")
    for job in Job.objects.order_by('-created_at')[:5]:
        status = "✓ Active" if job.is_active else "✗ Inactive"
        print(f"  {status} - {job.title}")
        print(f"    Category: {job.job_category}, Type: {job.job_type}")
        print(f"    Salary: ₹{job.min_salary:,.0f} - ₹{job.max_salary:,.0f}")
        print(f"    Deadline: {job.deadline}")
        print()
    
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
