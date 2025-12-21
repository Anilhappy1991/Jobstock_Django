"""
Generate 100 Sample Resume Files in Multiple Formats
Creates realistic resumes with varied data for testing
"""
import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Sample data pools
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Sai", "Reyansh", "Ayush", "Krishna", "Ishaan", "Shaurya",
    "Aadhya", "Ananya", "Pari", "Anika", "Ira", "Myra", "Sara", "Kavya", "Diya", "Navya",
    "Rahul", "Amit", "Priya", "Sneha", "Rajesh", "Pooja", "Vikram", "Anjali", "Suresh", "Meera",
    "Karan", "Neha", "Rohan", "Simran", "Aryan", "Riya", "Varun", "Shreya", "Nikhil", "Kriti",
    "Akash", "Divya", "Harsh", "Nisha", "Manish", "Ritika", "Sanjay", "Swati", "Gaurav", "Pallavi"
]

LAST_NAMES = [
    "Sharma", "Verma", "Kumar", "Singh", "Gupta", "Patel", "Reddy", "Rao", "Nair", "Iyer",
    "Chopra", "Kapoor", "Malhotra", "Agarwal", "Jain", "Mehta", "Shah", "Desai", "Kulkarni", "Joshi",
    "Bansal", "Mittal", "Saxena", "Tiwari", "Pandey", "Mishra", "Chawla", "Bhatia", "Arora", "Khanna",
    "Sethi", "Sinha", "Roy", "Das", "Ghosh", "Mukherjee", "Sengupta", "Bose", "Dutta", "Chatterjee",
    "Pillai", "Menon", "Krishnan", "Raman", "Sundaram", "Venkatesh", "Murthy", "Naidu", "Varma", "Sastry"
]

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad",
    "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
    "Visakhapatnam", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad",
    "Meerut", "Rajkot", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar",
    "Noida", "Gurugram", "Chandigarh", "Coimbatore", "Kochi", "Madurai", "Guwahati"
]

SKILLS = [
    "Python", "Java", "JavaScript", "React", "Angular", "Node.js", "Django", "Flask",
    "Spring Boot", "Hibernate", "MongoDB", "MySQL", "PostgreSQL", "AWS", "Azure", "Docker",
    "Kubernetes", "Git", "CI/CD", "Agile", "Scrum", "REST API", "GraphQL", "Microservices",
    "Machine Learning", "Data Analysis", "Pandas", "NumPy", "TensorFlow", "PyTorch",
    "HTML", "CSS", "Bootstrap", "Tailwind CSS", "TypeScript", "Vue.js", "Express.js",
    "Redis", "Elasticsearch", "Kafka", "RabbitMQ", "Jenkins", "Terraform", "Ansible",
    "Linux", "Bash", "PowerShell", "C++", "C#", ".NET", "ASP.NET", "PHP", "Laravel"
]

JOB_TITLES = [
    "Software Engineer", "Senior Software Developer", "Full Stack Developer", "Backend Developer",
    "Frontend Developer", "DevOps Engineer", "Data Scientist", "Machine Learning Engineer",
    "QA Engineer", "Test Automation Engineer", "Product Manager", "Project Manager",
    "Business Analyst", "System Administrator", "Cloud Architect", "Solution Architect",
    "UI/UX Designer", "Mobile App Developer", "Database Administrator", "Security Engineer",
    "Technical Lead", "Engineering Manager", "Scrum Master", "IT Consultant", "Network Engineer"
]

COMPANIES = [
    "Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra", "Cognizant", "Accenture", "IBM",
    "Microsoft", "Google", "Amazon", "Oracle", "SAP", "Adobe", "Cisco", "Intel",
    "Capgemini", "Deloitte", "EY", "KPMG", "PwC", "Flipkart", "Paytm", "Zomato",
    "Swiggy", "Ola", "PhonePe", "Myntra", "Snapdeal", "MakeMyTrip", "Freshworks",
    "Zoho", "Fractal Analytics", "Mu Sigma", "Genpact", "WNS", "Concentrix"
]

QUALIFICATIONS = [
    "B.Tech in Computer Science", "B.E. in Information Technology", "B.Sc. in Computer Science",
    "M.Tech in Software Engineering", "M.Sc. in Computer Applications", "MCA",
    "B.Tech in Electronics", "B.E. in Electrical Engineering", "MBA in IT Management",
    "B.Com with Computer Applications", "BCA", "Diploma in Computer Science"
]

UNIVERSITIES = [
    "IIT Delhi", "IIT Bombay", "IIT Bangalore", "IIT Madras", "IIT Kharagpur", "NIT Trichy",
    "NIT Warangal", "BITS Pilani", "VIT Vellore", "SRM University", "Amity University",
    "Anna University", "Delhi University", "Mumbai University", "Pune University",
    "Bangalore University", "Osmania University", "JNTU Hyderabad", "Manipal University"
]

HOBBIES = [
    "Reading", "Traveling", "Photography", "Blogging", "Coding", "Gaming", "Cooking",
    "Music", "Dancing", "Painting", "Fitness", "Yoga", "Swimming", "Cricket", "Football",
    "Chess", "Volunteering", "Gardening", "Writing", "Learning Languages", "Hiking"
]

def generate_person_data():
    """Generate random person data for resume"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    return {
        'name': f"{first_name} {last_name}",
        'email': f"{first_name.lower()}.{last_name.lower()}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'])}",
        'phone': f"+91-{random.randint(7000000000, 9999999999)}",
        'city': random.choice(CITIES),
        'skills': random.sample(SKILLS, random.randint(5, 12)),
        'current_ctc': random.choice([3.5, 4.0, 5.5, 6.0, 7.5, 8.0, 10.0, 12.0, 15.0, 18.0, 20.0, 25.0]),
        'expected_ctc': lambda ctc: ctc + random.uniform(2.0, 5.0),
        'qualification': random.choice(QUALIFICATIONS),
        'university': random.choice(UNIVERSITIES),
        'graduation_year': random.randint(2015, 2023),
        'hobbies': random.sample(HOBBIES, random.randint(3, 6)),
        'experience_years': random.randint(0, 12)
    }

def generate_experience(years):
    """Generate work experience"""
    experiences = []
    current_year = datetime.now().year
    remaining_years = years
    
    while remaining_years > 0:
        duration = random.randint(1, min(3, remaining_years))
        end_year = current_year
        start_year = end_year - duration
        
        company = random.choice(COMPANIES)
        title = random.choice(JOB_TITLES)
        
        experiences.append({
            'company': company,
            'title': title,
            'start_date': f"{random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])} {start_year}",
            'end_date': f"{random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])} {end_year}" if duration < years else "Present",
            'duration': f"{duration} year{'s' if duration > 1 else ''}",
            'responsibilities': [
                f"Developed and maintained {random.choice(['web applications', 'mobile apps', 'backend services', 'APIs'])}",
                f"Worked with {', '.join(random.sample(SKILLS[:20], 3))}",
                f"Collaborated with cross-functional teams of {random.randint(5, 15)} members",
                f"Improved {random.choice(['performance', 'scalability', 'code quality'])} by {random.randint(20, 60)}%"
            ]
        })
        
        remaining_years -= duration
        current_year = start_year
    
    return experiences

def create_txt_resume(data, filepath):
    """Create plain text resume"""
    current_ctc = data['current_ctc']
    expected_ctc = data['expected_ctc'](current_ctc)
    experiences = generate_experience(data['experience_years'])
    
    content = f"""
{'='*80}
                              RESUME
{'='*80}

PERSONAL INFORMATION
{'-'*80}
Name:               {data['name']}
Email:              {data['email']}
Phone:              {data['phone']}
Location:           {data['city']}, India
Current CTC:        ₹{current_ctc:.1f} LPA
Expected CTC:       ₹{expected_ctc:.1f} LPA

PROFESSIONAL SUMMARY
{'-'*80}
{data['experience_years']} years of experience in software development with expertise in 
{', '.join(data['skills'][:5])}. Proven track record of delivering high-quality 
solutions and working in agile environments.

EDUCATION
{'-'*80}
{data['qualification']}
{data['university']}
Graduated: {data['graduation_year']}

TECHNICAL SKILLS
{'-'*80}
"""
    
    # Add skills in groups
    skills_per_line = 4
    for i in range(0, len(data['skills']), skills_per_line):
        skills_group = data['skills'][i:i+skills_per_line]
        content += f"• {' | '.join(skills_group)}\n"
    
    content += f"\nWORK EXPERIENCE\n{'-'*80}\n"
    
    for exp in experiences:
        content += f"\n{exp['title']} at {exp['company']}\n"
        content += f"{exp['start_date']} - {exp['end_date']} ({exp['duration']})\n"
        content += "Responsibilities:\n"
        for resp in exp['responsibilities']:
            content += f"  • {resp}\n"
    
    content += f"\nHOBBIES & INTERESTS\n{'-'*80}\n"
    content += f"{', '.join(data['hobbies'])}\n"
    
    content += f"\n{'='*80}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def create_pdf_resume(data, filepath):
    """Create PDF resume using ReportLab"""
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    current_ctc = data['current_ctc']
    expected_ctc = data['expected_ctc'](current_ctc)
    experiences = generate_experience(data['experience_years'])
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 50, data['name'])
    
    # Contact Info
    y = height - 80
    c.setFont("Helvetica", 10)
    contact = f"{data['email']} | {data['phone']} | {data['city']}, India"
    c.drawCentredString(width/2, y, contact)
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PROFESSIONAL SUMMARY")
    
    y -= 20
    c.setFont("Helvetica", 10)
    summary = f"{data['experience_years']} years of experience in software development. Current CTC: ₹{current_ctc:.1f} LPA | Expected: ₹{expected_ctc:.1f} LPA"
    c.drawString(50, y, summary)
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EDUCATION")
    
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"{data['qualification']} - {data['university']} ({data['graduation_year']})")
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TECHNICAL SKILLS")
    
    y -= 20
    c.setFont("Helvetica", 10)
    skills_text = ", ".join(data['skills'])
    # Wrap skills if too long
    if len(skills_text) > 80:
        skills_line1 = ", ".join(data['skills'][:6])
        skills_line2 = ", ".join(data['skills'][6:])
        c.drawString(50, y, skills_line1)
        y -= 15
        c.drawString(50, y, skills_line2)
    else:
        c.drawString(50, y, skills_text)
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "WORK EXPERIENCE")
    
    for exp in experiences:
        if y < 100:  # New page if running out of space
            c.showPage()
            y = height - 50
        
        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{exp['title']} - {exp['company']}")
        
        y -= 15
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, y, f"{exp['start_date']} - {exp['end_date']}")
        
        y -= 15
        c.setFont("Helvetica", 9)
        for resp in exp['responsibilities'][:2]:  # Limit to 2 responsibilities for space
            if y < 80:
                c.showPage()
                y = height - 50
            c.drawString(60, y, f"• {resp[:70]}...")
            y -= 12
    
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "HOBBIES")
    
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(50, y, ", ".join(data['hobbies']))
    
    c.save()

def create_docx_resume(data, filepath):
    """Create DOCX resume using python-docx"""
    doc = Document()
    
    current_ctc = data['current_ctc']
    expected_ctc = data['expected_ctc'](current_ctc)
    experiences = generate_experience(data['experience_years'])
    
    # Title
    title = doc.add_heading(data['name'], level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Contact
    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.add_run(f"{data['email']} | {data['phone']} | {data['city']}, India")
    
    # Professional Summary
    doc.add_heading('Professional Summary', level=1)
    doc.add_paragraph(
        f"{data['experience_years']} years of experience in software development with expertise in "
        f"{', '.join(data['skills'][:5])}. Proven track record of delivering high-quality solutions."
    )
    
    # CTC Information
    ctc_para = doc.add_paragraph()
    ctc_para.add_run(f"Current CTC: ").bold = True
    ctc_para.add_run(f"₹{current_ctc:.1f} LPA | ")
    ctc_para.add_run(f"Expected CTC: ").bold = True
    ctc_para.add_run(f"₹{expected_ctc:.1f} LPA")
    
    # Education
    doc.add_heading('Education', level=1)
    edu_para = doc.add_paragraph()
    edu_para.add_run(f"{data['qualification']}\n").bold = True
    edu_para.add_run(f"{data['university']} | Graduated: {data['graduation_year']}")
    
    # Skills
    doc.add_heading('Technical Skills', level=1)
    doc.add_paragraph(", ".join(data['skills']))
    
    # Experience
    doc.add_heading('Work Experience', level=1)
    for exp in experiences:
        exp_title = doc.add_paragraph()
        exp_title.add_run(f"{exp['title']} - {exp['company']}\n").bold = True
        exp_title.add_run(f"{exp['start_date']} - {exp['end_date']}\n").italic = True
        
        for resp in exp['responsibilities']:
            doc.add_paragraph(resp, style='List Bullet')
    
    # Hobbies
    doc.add_heading('Hobbies & Interests', level=1)
    doc.add_paragraph(", ".join(data['hobbies']))
    
    doc.save(filepath)

def main():
    """Main function to generate all resumes"""
    print("="*80)
    print("GENERATING 100 SAMPLE RESUMES")
    print("="*80)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'sample_resumes')
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"\nSaving resumes to: {data_dir}")
    print(f"\nGenerating resumes...")
    
    formats = ['txt', 'pdf', 'docx', 'doc']
    created_files = {'txt': 0, 'pdf': 0, 'docx': 0, 'doc': 0}
    
    for i in range(1, 101):
        # Generate random person data
        person = generate_person_data()
        
        # Choose format (cycle through formats for variety)
        format_type = formats[i % len(formats)]
        
        # Create filename
        name_slug = person['name'].replace(' ', '_').lower()
        filename = f"resume_{i:03d}_{name_slug}.{format_type}"
        filepath = os.path.join(data_dir, filename)
        
        # Create resume based on format
        try:
            if format_type == 'txt':
                create_txt_resume(person, filepath)
            elif format_type == 'pdf':
                create_pdf_resume(person, filepath)
            elif format_type in ['docx', 'doc']:
                create_docx_resume(person, filepath)
            
            created_files[format_type] += 1
            
            if i % 10 == 0:
                print(f"  ✓ Generated {i} resumes...")
        
        except Exception as e:
            print(f"  ✗ Error creating {filename}: {str(e)}")
    
    print(f"\n{'='*80}")
    print("RESUME GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nTotal resumes created: {sum(created_files.values())}")
    print(f"\nBreakdown by format:")
    for fmt, count in created_files.items():
        print(f"  • {fmt.upper()}: {count} files")
    
    print(f"\nLocation: {data_dir}")
    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
