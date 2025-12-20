import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

# Create output directory if it doesn't exist
output_dir = r"c:\RandR\Jobstock_Django_v1.0.0\Jobstock_Django"

# Initialize workbook
wb = Workbook()
wb.remove(wb.active)  # Remove default sheet

# Define styles
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF", size=11)
subheader_fill = PatternFill(start_color="B4C7E7", end_color="B4C7E7", fill_type="solid")
subheader_font = Font(bold=True, size=10)
ui_fill = PatternFill(start_color="E7E6F7", end_color="E7E6F7", fill_type="solid")
frontend_fill = PatternFill(start_color="D5F5E3", end_color="D5F5E3", fill_type="solid")
backend_fill = PatternFill(start_color="FCE5CD", end_color="FCE5CD", fill_type="solid")
ai_fill = PatternFill(start_color="F5B7B1", end_color="F5B7B1", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

def apply_header_style(ws, row):
    for cell in ws[row]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border

def apply_task_type_style(cell, task_type):
    if task_type == "UI":
        cell.fill = ui_fill
    elif task_type == "Frontend":
        cell.fill = frontend_fill
    elif task_type == "Backend":
        cell.fill = backend_fill
    elif task_type == "AI/ML":
        cell.fill = ai_fill
    cell.border = thin_border
    cell.alignment = Alignment(vertical='top', wrap_text=True)

def auto_adjust_columns(ws):
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = min(max_length + 2, 80)
        ws.column_dimensions[column_letter].width = adjusted_width

# ============================================================================
# SHEET 1: PROJECT OVERVIEW
# ============================================================================
ws_overview = wb.create_sheet("Project Overview")
overview_data = [
    ["RPO SaaS Tool - Rudra Recruiter AI"],
    ["Product Requirements & Technical Specification"],
    ["Version: v1.0 | Owner: Rudra Enterprise LLC | Date: November 2025"],
    [""],
    ["Category", "Details"],
    ["Project Name", "Rudra Recruiter AI - AI-Powered Applicant Tracking System"],
    ["Target Users", "Internal: RPO Admin, Hiring Manager, Candidates"],
    ["MVP Scope", "Internal recruiters (Rudra Enterprise) - Resume parsing, AI matching, Dashboard & Reports"],
    ["Technology Stack", "Frontend: React/Next.js, Backend: Python FastAPI/Node.js, Database: PostgreSQL, AI: Sentence-BERT"],
    ["Deployment", "AWS (ECS/EC2 + RDS), S3 for storage, CloudFront CDN"],
    ["Security", "JWT + RBAC, AES-256 encryption, TLS 1.3"],
    ["Target Metrics", "99.5% uptime, <2s match scoring, Handle 100K+ candidates"],
    [""],
    ["Project Phases"],
    ["MVP (Current)", "Internal use - Core features: Resume parsing, AI matching, Dashboard"],
    ["Phase II", "External client portal, Multi-tenant, AI sourcing, Predictive analytics"],
    [""],
    ["Key Goals"],
    ["G1", "Recruiter Productivity - Automate repetitive tasks"],
    ["G2", "Match Accuracy - AI-based candidate-job scoring"],
    ["G3", "Central Repository - Unified candidate and job database"],
    ["G4", "Insights & Reporting - Analytics and KPIs"],
    ["G5", "Scalable Foundation - Ready for external rollout"],
]

for row_idx, row_data in enumerate(overview_data, start=1):
    for col_idx, value in enumerate(row_data, start=1):
        cell = ws_overview.cell(row=row_idx, column=col_idx, value=value)
        if row_idx == 1:
            cell.font = Font(bold=True, size=16, color="FFFFFF")
            cell.fill = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
        elif row_idx in [2, 3]:
            cell.font = Font(italic=True, size=10)
        elif row_idx in [5, 9, 14, 17]:
            cell.font = subheader_font
            cell.fill = subheader_fill

auto_adjust_columns(ws_overview)

# ============================================================================
# SHEET 2: MASTER TASK LIST
# ============================================================================
ws_tasks = wb.create_sheet("Master Task List")
ws_tasks.append(["#", "Epic/Category", "Feature/Task", "Task Type", "Priority", "Status", "Complexity", "Dependencies", "Details/Notes"])
apply_header_style(ws_tasks, 1)

tasks_data = [
    # Existing Features
    [1, "Core Pages", "Home Page - Design & Development", "UI, Frontend", "MVP", "In Progress", "Medium", "", "Landing page with branding, navigation, and CTAs"],
    [2, "Core Pages", "Login Page - Authentication UI", "UI, Frontend", "MVP", "Done", "Low", "", "JWT-based authentication with validation"],
    [3, "Core Pages", "Registration Page - User Signup", "UI, Frontend, Backend", "MVP", "Done", "Medium", "Login", "User registration with email verification"],
    [4, "Core Pages", "Candidate Dashboard", "UI, Frontend", "MVP", "In Progress", "High", "Login", "Dashboard showing application status, jobs, analytics"],
    [5, "Core Pages", "Logout Functionality", "Frontend, Backend", "MVP", "Done", "Low", "Login", "Session management and secure logout"],
    
    # Epic 1: Job Requisition Intake
    [6, "Epic 1: Job Requisition", "Job Description Upload & Parsing", "Backend, AI/ML", "MVP", "Not Started", "High", "", "Parse job description text to extract skills, experience, education"],
    [7, "Epic 1: Job Requisition", "Auto-generate Ideal Candidate Profile", "AI/ML", "MVP", "Not Started", "High", "Task 6", "AI analyzes JD and creates benchmark candidate profile"],
    [8, "Epic 1: Job Requisition", "Job Profile Review & Tuning UI", "UI, Frontend", "MVP", "Not Started", "Medium", "Task 7", "Interface for RPO admin to review and adjust AI-generated profile"],
    [9, "Epic 1: Job Requisition", "Market Data Analysis (Time-to-Fill, Salary)", "AI/ML, Backend", "Phase II", "Not Started", "High", "Task 7", "Estimate hiring metrics based on market data"],
    
    # Epic 2: Candidate Sourcing
    [10, "Epic 2: Sourcing", "Auto-post to Job Boards (LinkedIn, Indeed, etc.)", "Backend", "Phase II", "Not Started", "High", "Task 6", "API integrations with job boards for auto-posting"],
    [11, "Epic 2: Sourcing", "Resume Database Search", "Backend, AI/ML", "MVP", "Not Started", "High", "", "Search internal talent pool for matching candidates"],
    [12, "Epic 2: Sourcing", "Passive Candidate Discovery (LinkedIn)", "AI/ML, Backend", "Phase II", "Not Started", "Very High", "", "AI-powered LinkedIn scraping and matching"],
    [13, "Epic 2: Sourcing", "Branded Career Page Generator", "UI, Frontend, Backend", "Phase II", "Not Started", "Medium", "Task 6", "Create unique job-specific landing pages"],
    
    # Epic 3: Screening & Matching
    [14, "Epic 3: Screening", "Resume Parsing (PDF, DOCX)", "Backend, AI/ML", "MVP", "Done", "High", "", "Extract structured data from resumes - COMPLETED"],
    [15, "Epic 3: Screening", "Candidate-Job Match Score Calculation", "AI/ML", "MVP", "In Progress", "Very High", "Task 14", "Semantic similarity scoring (0-100) using Sentence-BERT"],
    [16, "Epic 3: Screening", "Top 10 Candidate Ranking UI", "UI, Frontend", "MVP", "Not Started", "Medium", "Task 15", "Display ranked candidates per job"],
    [17, "Epic 3: Screening", "Match Explanation Summary", "AI/ML, Frontend", "MVP", "Not Started", "Medium", "Task 15", "Show why AI recommended candidate (skills match, experience)"],
    [18, "Epic 3: Screening", "Knockout Questions Setup", "UI, Frontend, Backend", "Phase II", "Not Started", "Medium", "", "Configure auto-filter questions (work auth, etc.)"],
    [19, "Epic 3: Screening", "Sentiment Analysis on Applications", "AI/ML", "MVP", "In Progress", "Medium", "Task 14", "Analyze candidate communication sentiment - WORKING"],
    
    # Epic 4: Candidate Engagement
    [20, "Epic 4: Engagement", "Auto-confirmation Email (Application Received)", "Backend", "MVP", "Not Started", "Low", "Task 14", "Send immediate confirmation to applicants"],
    [21, "Epic 4: Engagement", "Auto-rejection Email (Low Match)", "Backend, AI/ML", "Phase II", "Not Started", "Medium", "Task 15", "Polite rejection for <20% match score candidates"],
    [22, "Epic 4: Engagement", "AI Chatbot for Candidate Q&A", "AI/ML, Frontend", "Phase II", "Not Started", "Very High", "", "24/7 chatbot for application status and FAQs"],
    [23, "Epic 4: Engagement", "Personalized Outreach Message Generator", "AI/ML, Backend", "Phase II", "Not Started", "High", "Task 15", "AI-drafted messages for passive candidates"],
    
    # Epic 5: Interview Scheduling
    [24, "Epic 5: Scheduling", "Self-scheduling Portal for Candidates", "UI, Frontend, Backend", "Phase II", "Not Started", "High", "", "Calendar integration for candidate self-booking"],
    [25, "Epic 5: Scheduling", "Calendar Integration (Google, Outlook)", "Backend", "Phase II", "Not Started", "High", "Task 24", "Sync with interviewer availability"],
    [26, "Epic 5: Scheduling", "Auto Calendar Invites with Video Links", "Backend", "Phase II", "Not Started", "Medium", "Task 25", "Generate and send meeting invites"],
    [27, "Epic 5: Scheduling", "Interview Reminder Emails (24h, 1h)", "Backend", "Phase II", "Not Started", "Low", "Task 24", "Reduce no-shows with automated reminders"],
    
    # Epic 6: Analytics & Hub
    [28, "Epic 6: Analytics", "Recruiter Dashboard - Job Status Overview", "UI, Frontend", "MVP", "Not Started", "High", "", "Central view of all open jobs and pipeline stages"],
    [29, "Epic 6: Analytics", "Candidate Profile View (Full History)", "UI, Frontend", "MVP", "Not Started", "Medium", "", "All communication, statuses, feedback in one view"],
    [30, "Epic 6: Analytics", "Hiring Manager Portal (Pipeline View)", "UI, Frontend", "Phase II", "Not Started", "Medium", "", "Client-facing view of candidate pipeline"],
    [31, "Epic 6: Analytics", "KPI Reports (Time-to-Fill, Source-of-Hire)", "Backend, Frontend", "MVP", "Not Started", "High", "", "Generate and export recruitment metrics"],
    [32, "Epic 6: Analytics", "Visual Charts (Bar, Pie, Heatmap)", "UI, Frontend", "MVP", "Not Started", "Medium", "Task 31", "Graphical widgets for dashboard"],
    [33, "Epic 6: Analytics", "Weekly Email Summary Reports", "Backend", "Phase II", "Not Started", "Low", "Task 31", "Automated report delivery to stakeholders"],
    
    # Technical Infrastructure
    [34, "Infrastructure", "Database Schema Design (PostgreSQL)", "Backend", "MVP", "Not Started", "High", "", "Design Candidate, Job, MatchScore tables"],
    [35, "Infrastructure", "Elasticsearch Integration for Search", "Backend", "MVP", "Not Started", "High", "Task 34", "Semantic search indexing"],
    [36, "Infrastructure", "AWS S3 / Azure Blob Storage Setup", "Backend", "MVP", "Not Started", "Medium", "", "Resume file storage"],
    [37, "Infrastructure", "API Development (FastAPI/Express)", "Backend", "MVP", "Not Started", "Very High", "Task 34", "RESTful API endpoints for all features"],
    [38, "Infrastructure", "CI/CD Pipeline (GitHub Actions, Docker)", "Backend", "MVP", "Not Started", "High", "", "Automated testing and deployment"],
    [39, "Infrastructure", "Monitoring & Logging (Grafana, Prometheus)", "Backend", "MVP", "Not Started", "Medium", "", "System health and performance tracking"],
    [40, "Infrastructure", "Security Implementation (JWT, RBAC, Encryption)", "Backend", "MVP", "Not Started", "Very High", "Task 37", "Authentication, authorization, data encryption"],
    
    # AI/ML Development
    [41, "AI/ML", "Sentence-BERT Model Integration", "AI/ML", "MVP", "Not Started", "Very High", "", "Core semantic similarity engine"],
    [42, "AI/ML", "Fine-tuning Pipeline with Recruiter Feedback", "AI/ML", "Phase II", "Not Started", "Very High", "Task 41", "Improve model based on user validation"],
    [43, "AI/ML", "Resume Entity Extraction (Skills, Education, etc.)", "AI/ML", "MVP", "Not Started", "High", "", "NLP-based structured data extraction"],
    [44, "AI/ML", "Job Description Parsing & Skill Extraction", "AI/ML", "MVP", "Not Started", "High", "", "Extract requirements from JD text"],
    [45, "AI/ML", "Embedding Generation & Vector Storage", "AI/ML, Backend", "MVP", "Not Started", "High", "Task 41", "Store and query semantic embeddings"],
    
    # Additional Features
    [46, "Advanced Features", "Boolean Search with Filters (AND/OR/NOT)", "Frontend, Backend", "MVP", "Not Started", "Medium", "Task 35", "Advanced candidate search"],
    [47, "Advanced Features", "Smart Candidate Suggestions", "AI/ML, Frontend", "Phase II", "Not Started", "Medium", "Task 15", "Find similar candidates feature"],
    [48, "Advanced Features", "Multi-tenant Architecture", "Backend", "Phase II", "Not Started", "Very High", "", "Support for multiple client accounts"],
    [49, "Advanced Features", "GDPR/EEOC Compliance Features", "Backend, Frontend", "Phase II", "Not Started", "High", "", "Data privacy and compliance tools"],
    [50, "Advanced Features", "Audit Trail & Activity Logging", "Backend", "MVP", "Not Started", "Medium", "Task 40", "Track all system changes and actions"],
    
    # Testing & Documentation
    [51, "QA & Testing", "Unit Testing (Backend APIs)", "Backend", "MVP", "Not Started", "Medium", "", "Automated test coverage for APIs"],
    [52, "QA & Testing", "Integration Testing", "Backend, Frontend", "MVP", "Not Started", "Medium", "", "End-to-end workflow testing"],
    [53, "QA & Testing", "UI/UX Testing & Validation", "UI", "MVP", "Not Started", "Medium", "", "User acceptance testing"],
    [54, "Documentation", "API Documentation (Swagger/OpenAPI)", "Backend", "MVP", "Not Started", "Low", "", "Developer documentation"],
    [55, "Documentation", "User Manual & Training Materials", "UI", "Phase II", "Not Started", "Low", "", "End-user guides"],
    
    # Project Management
    [56, "Planning", "WBS (Work Breakdown Structure)", "Management", "MVP", "Not Started", "Low", "", "Detailed task decomposition"],
    [57, "Planning", "Resource Management Plan", "Management", "MVP", "Not Started", "Low", "", "Team allocation and capacity planning"],
    [58, "Planning", "Timeline & Milestone Creation", "Management", "MVP", "Not Started", "Low", "", "Project schedule with deliverable dates"],
    [59, "Planning", "In-scope / Out-of-scope Definition", "Management", "MVP", "Not Started", "Low", "", "Clear boundary documentation"],
]

for task in tasks_data:
    row_idx = ws_tasks.max_row + 1
    for col_idx, value in enumerate(task, start=1):
        cell = ws_tasks.cell(row=row_idx, column=col_idx, value=value)
        if col_idx == 4:  # Task Type column
            apply_task_type_style(cell, value.split(",")[0].strip() if value else "")
        else:
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

# Set column widths
ws_tasks.column_dimensions['A'].width = 5
ws_tasks.column_dimensions['B'].width = 25
ws_tasks.column_dimensions['C'].width = 45
ws_tasks.column_dimensions['D'].width = 20
ws_tasks.column_dimensions['E'].width = 12
ws_tasks.column_dimensions['F'].width = 12
ws_tasks.column_dimensions['G'].width = 12
ws_tasks.column_dimensions['H'].width = 20
ws_tasks.column_dimensions['I'].width = 50

# ============================================================================
# SHEET 3: USER STORIES
# ============================================================================
ws_stories = wb.create_sheet("User Stories")
ws_stories.append(["#", "Epic", "Persona", "User Story", "Acceptance Criteria", "Task Type", "Priority"])
apply_header_style(ws_stories, 1)

user_stories = [
    [1, "Epic 1: Job Requisition", "Hiring Manager", "As a Hiring Manager, I want to upload a simple job description, so that the AI can analyze it and generate a detailed job requisition", "- Support upload of text/PDF job descriptions\n- AI extracts skills, experience, education\n- Auto-generated candidate profile displayed", "AI/ML, Backend", "MVP"],
    [2, "Epic 1: Job Requisition", "System", "As a System, I want to parse the job description to extract key requirements, so that these become the core matching criteria", "- Extract 90%+ accuracy for standard fields\n- Structured data stored in database", "AI/ML", "MVP"],
    [3, "Epic 1: Job Requisition", "RPO Admin", "As an RPO Admin, I want to review and tune the AI-generated profile, so that I can ensure search alignment", "- UI shows all extracted fields\n- Can add/edit/remove skills and requirements\n- Changes saved immediately", "UI, Frontend, Backend", "MVP"],
    [4, "Epic 1: Job Requisition", "System", "As a System, I want to analyze job requirements against market data, so that I can provide time-to-fill estimates", "- Integration with market data APIs\n- Display estimated time and salary range", "AI/ML, Backend", "Phase II"],
    
    [5, "Epic 2: Sourcing", "System", "As a System, I want to auto-post approved jobs to job boards, so that I can maximize candidate reach", "- API integration with LinkedIn, Indeed, Monster\n- Successful posting confirmation\n- Error handling for failed posts", "Backend", "Phase II"],
    [6, "Epic 2: Sourcing", "System", "As a System, I want to search resume databases for matching candidates, so that I can find qualified talent proactively", "- Search internal database\n- Return relevance-ranked results\n- <3 second response time", "Backend, AI/ML", "MVP"],
    [7, "Epic 2: Sourcing", "RPO Admin", "As an RPO Admin, I want the AI to discover passive candidates on LinkedIn, so that I can expand my talent pool", "- LinkedIn integration for profile search\n- Match score calculation\n- Suggest outreach candidates", "AI/ML, Backend", "Phase II"],
    [8, "Epic 2: Sourcing", "System", "As a System, I want to create a branded career page for each job, so that candidates have a central place to apply", "- Auto-generate unique URL per job\n- Customizable branding\n- Mobile-responsive", "UI, Frontend, Backend", "Phase II"],
    
    [9, "Epic 3: Screening", "System", "As a System, I want to automatically parse all incoming resumes, so that I can extract structured data", "- Support PDF, DOCX formats\n- Extract name, skills, experience, education\n- 95%+ parsing accuracy", "Backend, AI/ML", "MVP - DONE"],
    [10, "Epic 3: Screening", "System", "As a System, I want to give every candidate a Match Score, so that I can rank candidates by relevance", "- Calculate 0-100 score using semantic similarity\n- Store scores in database\n- Update scores when job changes", "AI/ML", "MVP"],
    [11, "Epic 3: Screening", "RPO Admin", "As an RPO Admin, I want to see a Top 10 list for each job, so that I can focus on best candidates", "- Display ranked list with scores\n- Show key match factors\n- Quick profile access", "UI, Frontend", "MVP"],
    [12, "Epic 3: Screening", "Hiring Manager", "As a Hiring Manager, I want to see why AI recommended a candidate, so that I can trust the system", "- Display match breakdown (skills, experience)\n- Show matched vs missing requirements\n- Clear, concise summary", "AI/ML, Frontend", "MVP"],
    [13, "Epic 3: Screening", "RPO Admin", "As an RPO Admin, I want to set up knockout questions, so that the system auto-filters non-qualified candidates", "- Configurable question builder\n- Auto-rejection based on answers\n- Notification to candidates", "UI, Frontend, Backend", "Phase II"],
    
    [14, "Epic 4: Engagement", "Candidate", "As a Candidate, I want to receive immediate confirmation after applying, so that I know my application was received", "- Auto-email sent within 1 minute\n- Personalized with candidate name and job title\n- Branded template", "Backend", "MVP"],
    [15, "Epic 4: Engagement", "System", "As a System, I want to send automated rejection emails to low-match candidates, so that we maintain good employer brand", "- Trigger for <20% match score\n- Polite, professional messaging\n- Configurable threshold", "Backend, AI/ML", "Phase II"],
    [16, "Epic 4: Engagement", "Candidate", "As a Candidate, I want to interact with an AI chatbot 24/7, so that I can get immediate answers", "- Natural language Q&A\n- Answer common questions (status, requirements)\n- Escalate complex queries", "AI/ML, Frontend", "Phase II"],
    [17, "Epic 4: Engagement", "RPO Admin", "As an RPO Admin, I want the AI to draft outreach messages, so that I can contact passive candidates efficiently", "- Generate personalized messages\n- Include relevant job highlights\n- Editable before sending", "AI/ML, Backend", "Phase II"],
    
    [18, "Epic 5: Scheduling", "Candidate", "As a Candidate, I want to receive a self-scheduling portal link, so that I can pick an interview time", "- Email with unique scheduling link\n- Show available time slots\n- Timezone-aware", "UI, Frontend, Backend", "Phase II"],
    [19, "Epic 5: Scheduling", "System", "As a System, I want to integrate with interviewer calendars, so that I show only actual availability", "- Google Calendar & Outlook sync\n- Real-time availability check\n- Handle conflicts", "Backend", "Phase II"],
    [20, "Epic 5: Scheduling", "System", "As a System, I want to auto-send calendar invites with video links, so that all parties are notified", "- Generate meeting invites\n- Include Zoom/Teams link\n- Send to candidate and interviewer", "Backend", "Phase II"],
    [21, "Epic 5: Scheduling", "System", "As a System, I want to send reminder emails before interviews, so that we reduce no-shows", "- 24-hour and 1-hour reminders\n- Include meeting details and link\n- Configurable timing", "Backend", "Phase II"],
    
    [22, "Epic 6: Analytics", "RPO Admin", "As an RPO Admin, I want a central dashboard showing all job statuses, so that I can manage my workload", "- Display all open jobs\n- Show candidates at each stage\n- Filterable by date, status, client", "UI, Frontend", "MVP"],
    [23, "Epic 6: Analytics", "RPO Admin", "As an RPO Admin, I want a full Candidate Profile view, so that I see all history in one place", "- Show all communication logs\n- Display application statuses\n- Include interview feedback\n- Timeline view", "UI, Frontend", "MVP"],
    [24, "Epic 6: Analytics", "Hiring Manager", "As a Hiring Manager, I want to see my job pipeline, so that I know status without emailing", "- Simple pipeline view (Applied → Screened → Interview → Offer)\n- Candidate count per stage\n- Quick candidate preview", "UI, Frontend", "Phase II"],
    [25, "Epic 6: Analytics", "RPO Admin", "As an RPO Admin, I want to run reports on key metrics, so that I can show value to clients", "- Generate Time-to-Fill, Source-of-Hire reports\n- Candidate funnel analysis\n- Exportable to Excel/PDF", "Backend, Frontend", "MVP"],
]

for story in user_stories:
    row_idx = ws_stories.max_row + 1
    for col_idx, value in enumerate(story, start=1):
        cell = ws_stories.cell(row=row_idx, column=col_idx, value=value)
        if col_idx == 6:  # Task Type
            apply_task_type_style(cell, value.split(",")[0].strip() if value else "")
        else:
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

ws_stories.column_dimensions['A'].width = 5
ws_stories.column_dimensions['B'].width = 25
ws_stories.column_dimensions['C'].width = 18
ws_stories.column_dimensions['D'].width = 50
ws_stories.column_dimensions['E'].width = 50
ws_stories.column_dimensions['F'].width = 20
ws_stories.column_dimensions['G'].width = 12

# ============================================================================
# SHEET 4: TECHNICAL STACK
# ============================================================================
ws_tech = wb.create_sheet("Technical Stack")
ws_tech.append(["Layer", "Component", "Technology/Tool", "Purpose", "Task Type", "Priority"])
apply_header_style(ws_tech, 1)

tech_stack = [
    ["Frontend", "Framework", "React / Next.js", "Modern UI framework with SSR support", "Frontend", "MVP"],
    ["Frontend", "UI Library", "Tailwind CSS / Material UI", "Responsive design and components", "UI", "MVP"],
    ["Frontend", "State Management", "Redux / Context API", "Application state management", "Frontend", "MVP"],
    ["Frontend", "Authentication", "JWT + HTTP-only cookies", "Secure client-side auth", "Frontend", "MVP"],
    
    ["Backend", "API Framework", "Python FastAPI / Node.js Express", "RESTful API development", "Backend", "MVP"],
    ["Backend", "Language", "Python 3.11+ / Node.js 18+", "Core programming language", "Backend", "MVP"],
    ["Backend", "API Documentation", "Swagger / OpenAPI", "Auto-generated API docs", "Backend", "MVP"],
    ["Backend", "Validation", "Pydantic (FastAPI) / Joi (Express)", "Request/response validation", "Backend", "MVP"],
    
    ["Database", "Primary DB", "PostgreSQL 15+", "Structured data storage", "Backend", "MVP"],
    ["Database", "Search Engine", "Elasticsearch 8.x", "Full-text and semantic search", "Backend", "MVP"],
    ["Database", "Caching", "Redis", "Session and query caching", "Backend", "Phase II"],
    ["Database", "ORM", "SQLAlchemy / Prisma", "Database abstraction layer", "Backend", "MVP"],
    
    ["AI/ML", "Embedding Model", "Sentence-BERT (all-MiniLM-L6-v2)", "Semantic similarity calculations", "AI/ML", "MVP"],
    ["AI/ML", "NLP Library", "spaCy / Hugging Face Transformers", "Text processing and entity extraction", "AI/ML", "MVP"],
    ["AI/ML", "ML Framework", "PyTorch / scikit-learn", "Model training and fine-tuning", "AI/ML", "Phase II"],
    ["AI/ML", "Resume Parsing", "pyresparser / Custom NLP pipeline", "Extract structured data from resumes", "AI/ML", "MVP"],
    ["AI/ML", "Sentiment Analysis", "VADER / DistilBERT", "Analyze candidate communication tone", "AI/ML", "MVP"],
    
    ["Storage", "File Storage", "AWS S3 / Azure Blob Storage", "Resume and document storage", "Backend", "MVP"],
    ["Storage", "CDN", "CloudFront / Azure CDN", "Fast static asset delivery", "Backend", "MVP"],
    
    ["Infrastructure", "Cloud Platform", "AWS / Azure", "Hosting and infrastructure", "Backend", "MVP"],
    ["Infrastructure", "Container", "Docker", "Application containerization", "Backend", "MVP"],
    ["Infrastructure", "Orchestration", "ECS Fargate / Kubernetes", "Container orchestration", "Backend", "MVP"],
    ["Infrastructure", "CI/CD", "GitHub Actions / GitLab CI", "Automated deployment pipeline", "Backend", "MVP"],
    ["Infrastructure", "Monitoring", "Grafana + Prometheus", "System metrics and alerting", "Backend", "MVP"],
    ["Infrastructure", "Logging", "CloudWatch / ELK Stack", "Application and error logging", "Backend", "MVP"],
    
    ["Security", "Authentication", "JWT + RBAC", "Token-based auth with role permissions", "Backend", "MVP"],
    ["Security", "Encryption", "AES-256 (at rest) + TLS 1.3 (in transit)", "Data encryption", "Backend", "MVP"],
    ["Security", "Secret Management", "AWS Secrets Manager / Azure Key Vault", "Secure credential storage", "Backend", "MVP"],
    ["Security", "API Security", "Rate limiting + CORS + Input validation", "Prevent attacks and abuse", "Backend", "MVP"],
    
    ["Integration", "Job Boards", "LinkedIn API, Indeed API", "Job posting automation", "Backend", "Phase II"],
    ["Integration", "Calendar", "Google Calendar API, Microsoft Graph API", "Interview scheduling sync", "Backend", "Phase II"],
    ["Integration", "Email", "SendGrid / AWS SES", "Transactional email delivery", "Backend", "MVP"],
    ["Integration", "Video Conferencing", "Zoom API / Microsoft Teams API", "Auto-generate meeting links", "Backend", "Phase II"],
]

for item in tech_stack:
    row_idx = ws_tech.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_tech.cell(row=row_idx, column=col_idx, value=value)
        if col_idx == 5:  # Task Type
            apply_task_type_style(cell, value)
        else:
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

ws_tech.column_dimensions['A'].width = 15
ws_tech.column_dimensions['B'].width = 20
ws_tech.column_dimensions['C'].width = 35
ws_tech.column_dimensions['D'].width = 45
ws_tech.column_dimensions['E'].width = 15
ws_tech.column_dimensions['F'].width = 12

# ============================================================================
# SHEET 5: RESOURCE PLAN WITH COSTING
# ============================================================================
ws_resource = wb.create_sheet("Resource Plan")
ws_resource.append(["Role", "Required Skills", "Estimated Effort", "Min Cost (INR/Month)", "Max Cost (INR/Month)", "Total Min Cost (INR)", "Total Max Cost (INR)", "Priority", "Status", "Notes"])
apply_header_style(ws_resource, 1)

resource_data = [
    ["Full Stack Developer", "React, Node.js/Python, PostgreSQL, REST APIs", "6-9 months (Full-time)", "80,000", "1,50,000", "4,80,000", "13,50,000", "Critical - NOW", "Hiring", "Primary developer for MVP. Senior level: ₹1.2-1.5L, Mid: ₹80K-1L"],
    ["Backend Developer", "Python/Node.js, FastAPI/Express, Database design", "6-9 months (Full-time)", "70,000", "1,30,000", "4,20,000", "11,70,000", "Critical - NOW", "Hiring", "Focus on API and integrations. Senior: ₹1-1.3L, Mid: ₹70K-90K"],
    ["ML/AI Engineer", "Python, PyTorch, NLP, Sentence-BERT, spaCy", "4-6 months (Part-time initially)", "1,00,000", "2,00,000", "4,00,000", "12,00,000", "High", "Needed Soon", "Resume parsing and matching algorithms. Specialized role with premium rates"],
    ["UI/UX Designer", "Figma, Wireframing, User research, Prototyping", "2-3 months", "50,000", "1,00,000", "1,00,000", "3,00,000", "High", "Needed Soon", "Design all interfaces before development. Senior: ₹80K-1L, Mid: ₹50K-70K"],
    ["DevOps Engineer", "AWS/Azure, Docker, CI/CD, Monitoring", "1-2 months (Part-time)", "80,000", "1,50,000", "80,000", "3,00,000", "Medium", "Phase II", "Infrastructure setup and deployment. Part-time or consultant basis"],
    ["QA Engineer", "Test automation, Selenium, API testing", "2-3 months", "45,000", "80,000", "90,000", "2,40,000", "Medium", "Phase II", "Quality assurance and testing. Can be junior-mid level"],
    ["Product Manager", "Agile, Roadmap planning, Stakeholder management", "Ongoing (Part-time)", "60,000", "1,20,000", "3,60,000", "7,20,000", "Medium", "Current", "RRG + hired PM. Part-time 6 months estimated"],
    ["Solution Architect (Consultant)", "System design, Architecture patterns, Scalability", "2-4 weeks", "2,00,000", "3,50,000", "1,00,000", "3,50,000", "Critical - NOW", "Needed", "Expert advice on architecture. Consultant hourly/project basis"],
    ["Technical Writer", "Documentation, User guides, API docs", "1 month", "40,000", "70,000", "40,000", "70,000", "Low", "Phase II", "Documentation and training materials. Contract basis"],
]

# Add summary row
ws_resource.append(["", "", "", "", "", "", "", "", "", ""])
summary_row = ws_resource.max_row + 1
ws_resource.cell(row=summary_row, column=1, value="TOTAL ESTIMATED COST")
ws_resource.cell(row=summary_row, column=6, value="₹ 20,70,000")
ws_resource.cell(row=summary_row, column=7, value="₹ 57,00,000")

# Style summary row
for col in range(1, 11):
    cell = ws_resource.cell(row=summary_row, column=col)
    cell.font = Font(bold=True, size=12, color="FFFFFF")
    cell.fill = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center', vertical='center')

for item in resource_data:
    row_idx = ws_resource.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_resource.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        if col_idx == 8 and "Critical" in value:
            cell.font = Font(bold=True, color="C00000")
            cell.fill = PatternFill(start_color="FFE6E6", end_color="FFE6E6", fill_type="solid")
        # Highlight cost columns
        if col_idx in [4, 5, 6, 7]:
            cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
            cell.font = Font(bold=True)

# Set column widths
ws_resource.column_dimensions['A'].width = 25
ws_resource.column_dimensions['B'].width = 40
ws_resource.column_dimensions['C'].width = 25
ws_resource.column_dimensions['D'].width = 18
ws_resource.column_dimensions['E'].width = 18
ws_resource.column_dimensions['F'].width = 18
ws_resource.column_dimensions['G'].width = 18
ws_resource.column_dimensions['H'].width = 15
ws_resource.column_dimensions['I'].width = 12
ws_resource.column_dimensions['J'].width = 50

# ============================================================================
# SHEET 6: DETAILED COST BREAKDOWN
# ============================================================================
ws_cost = wb.create_sheet("Detailed Cost Breakdown")
ws_cost.append(["Cost Category", "Item", "Quantity/Duration", "Unit Cost (INR)", "Min Total (INR)", "Max Total (INR)", "Notes"])
apply_header_style(ws_cost, 1)

cost_breakdown = [
    ["Human Resources", "Full Stack Developer (Senior)", "9 months", "1,50,000/month", "10,80,000", "13,50,000", "Including benefits and overhead"],
    ["Human Resources", "Full Stack Developer (Mid-level)", "9 months", "80,000/month", "4,80,000", "7,20,000", "Alternative to senior developer"],
    ["Human Resources", "Backend Developer (Senior)", "9 months", "1,30,000/month", "9,36,000", "11,70,000", "API and database specialist"],
    ["Human Resources", "Backend Developer (Mid-level)", "9 months", "70,000/month", "4,20,000", "6,30,000", "Alternative to senior"],
    ["Human Resources", "ML/AI Engineer", "6 months", "1,50,000/month", "4,00,000", "12,00,000", "Part-time to full-time progression"],
    ["Human Resources", "UI/UX Designer", "3 months", "70,000/month", "1,00,000", "3,00,000", "Full project design phase"],
    ["Human Resources", "DevOps Engineer (Part-time)", "2 months", "1,00,000/month", "80,000", "3,00,000", "Infrastructure setup"],
    ["Human Resources", "QA Engineer", "3 months", "60,000/month", "90,000", "2,40,000", "Testing and quality assurance"],
    ["Human Resources", "Product Manager (Part-time)", "6 months", "80,000/month", "3,60,000", "7,20,000", "Project coordination"],
    ["Human Resources", "Solution Architect (Consultant)", "1 month", "2,50,000/month", "1,00,000", "3,50,000", "2-4 weeks consultation"],
    ["Human Resources", "Technical Writer", "1 month", "55,000/month", "40,000", "70,000", "Documentation"],
    ["", "", "", "SUBTOTAL - HR", "₹ 20,70,000", "₹ 57,00,000", ""],
    
    ["Infrastructure", "AWS/Azure Hosting (Monthly)", "12 months", "30,000/month", "3,60,000", "7,20,000", "EC2, RDS, S3, CloudFront"],
    ["Infrastructure", "Domain & SSL Certificates", "1 year", "5,000", "5,000", "10,000", "Custom domain and security"],
    ["Infrastructure", "Email Service (SendGrid/SES)", "12 months", "5,000/month", "60,000", "1,20,000", "Transactional emails"],
    ["Infrastructure", "Monitoring Tools (Grafana Cloud)", "12 months", "10,000/month", "1,20,000", "1,80,000", "Performance monitoring"],
    ["Infrastructure", "CI/CD Pipeline (GitHub Actions)", "12 months", "3,000/month", "36,000", "60,000", "Automated deployment"],
    ["", "", "", "SUBTOTAL - Infrastructure", "₹ 5,81,000", "₹ 10,90,000", ""],
    
    ["Software & Tools", "Figma Professional (UI/UX)", "12 months", "1,200/month", "14,400", "21,600", "Design collaboration"],
    ["Software & Tools", "JetBrains/IDE Licenses", "3 licenses x 12 months", "700/month/user", "25,200", "42,000", "Development tools"],
    ["Software & Tools", "Jira/Project Management", "12 months", "10,000/month", "1,20,000", "1,80,000", "Agile project tracking"],
    ["Software & Tools", "Postman Team", "12 months", "5,000/month", "60,000", "1,00,000", "API testing"],
    ["Software & Tools", "Git Repository (GitHub Teams)", "12 months", "2,000/month", "24,000", "36,000", "Code repository"],
    ["", "", "", "SUBTOTAL - Software", "₹ 2,43,600", "₹ 3,79,600", ""],
    
    ["API & Integrations", "LinkedIn API (Recruitment)", "12 months", "40,000/month", "4,80,000", "7,20,000", "Phase II - Job posting & sourcing"],
    ["API & Integrations", "Indeed API Access", "12 months", "20,000/month", "2,40,000", "3,60,000", "Phase II - Job posting"],
    ["API & Integrations", "Zoom API (Video Interviews)", "12 months", "15,000/month", "1,80,000", "2,40,000", "Phase II - Interview scheduling"],
    ["API & Integrations", "Google Calendar/Outlook API", "One-time setup", "50,000", "50,000", "1,00,000", "Calendar integration"],
    ["", "", "", "SUBTOTAL - APIs (Phase II)", "₹ 9,50,000", "₹ 14,20,000", "Phase II features"],
    
    ["Training & Misc", "Team Training & Workshops", "5 sessions", "20,000/session", "1,00,000", "2,00,000", "Skill development"],
    ["Training & Misc", "Documentation & Knowledge Base", "One-time", "50,000", "50,000", "1,00,000", "Internal wikis and guides"],
    ["Training & Misc", "Legal & Compliance (GDPR/EEOC)", "Consultation", "1,00,000", "1,00,000", "2,00,000", "Legal review and compliance"],
    ["Training & Misc", "Testing Environments & Data", "One-time setup", "50,000", "50,000", "1,00,000", "Test data and environments"],
    ["Training & Misc", "Buffer/Contingency (10%)", "10% of HR costs", "-", "2,07,000", "5,70,000", "Unexpected expenses"],
    ["", "", "", "SUBTOTAL - Misc", "₹ 5,07,000", "₹ 12,70,000", ""],
    
    ["", "", "", "", "", "", ""],
    ["TOTAL MVP COST", "", "", "", "₹ 34,01,600", "₹ 81,89,600", "Minimum viable product"],
    ["TOTAL WITH PHASE II", "", "", "", "₹ 43,51,600", "₹ 96,09,600", "Including Phase II features"],
]

for idx, item in enumerate(cost_breakdown):
    row_idx = ws_cost.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_cost.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        
        # Style category headers
        if col_idx == 1 and value and value not in ["", "TOTAL MVP COST", "TOTAL WITH PHASE II"] and item[1] == "":
            cell.font = Font(bold=True, size=11)
            cell.fill = subheader_fill
        
        # Style subtotals
        if "SUBTOTAL" in str(value):
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="7030A0", end_color="7030A0", fill_type="solid")
        
        # Style totals
        if value in ["TOTAL MVP COST", "TOTAL WITH PHASE II"]:
            for c in range(1, 8):
                cell_total = ws_cost.cell(row=row_idx, column=c)
                cell_total.font = Font(bold=True, size=12, color="FFFFFF")
                cell_total.fill = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
                cell_total.border = thin_border
                cell_total.alignment = Alignment(horizontal='center', vertical='center')
        
        # Highlight cost columns
        if col_idx in [5, 6] and value and value != "":
            if "₹" in str(value):
                cell.font = Font(bold=True, size=11)
                cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

ws_cost.column_dimensions['A'].width = 20
ws_cost.column_dimensions['B'].width = 35
ws_cost.column_dimensions['C'].width = 20
ws_cost.column_dimensions['D'].width = 18
ws_cost.column_dimensions['E'].width = 18
ws_cost.column_dimensions['F'].width = 18
ws_cost.column_dimensions['G'].width = 40

# ============================================================================
# SHEET 7: PROJECT TIMELINE
# ============================================================================
ws_timeline = wb.create_sheet("Timeline & Milestones")
ws_timeline.append(["Phase", "Milestone", "Duration", "Dependencies", "Deliverables", "Status"])
apply_header_style(ws_timeline, 1)

timeline_data = [
    ["Planning", "Project Kickoff & Requirements Finalization", "Week 1-2", "", "Finalized PRD, WBS, Resource Plan", "In Progress"],
    ["Planning", "Technical Architecture Design", "Week 2-3", "Milestone 1", "Architecture diagram, Technology stack finalized", "Not Started"],
    ["Planning", "UI/UX Design & Wireframing", "Week 3-6", "Milestone 2", "Figma designs, User flows, Prototypes", "Not Started"],
    
    ["Development - Phase 1", "Database Schema & Backend Setup", "Week 6-8", "Milestone 3", "PostgreSQL schema, FastAPI skeleton", "Not Started"],
    ["Development - Phase 1", "Authentication & User Management", "Week 8-10", "Milestone 4", "Login, Registration, JWT implementation", "Partially Done"],
    ["Development - Phase 1", "Resume Parsing Implementation", "Week 10-13", "Milestone 4", "PDF/DOCX parsing, Data extraction", "Done"],
    ["Development - Phase 1", "AI Matching Algorithm (Core)", "Week 13-16", "Milestone 6", "Sentence-BERT integration, Match scoring", "In Progress"],
    
    ["Development - Phase 2", "Job Management Module", "Week 16-18", "Milestone 4", "Job CRUD, Job profile management", "Not Started"],
    ["Development - Phase 2", "Candidate Dashboard UI", "Week 18-20", "Milestone 5", "Dashboard with application tracking", "In Progress"],
    ["Development - Phase 2", "Recruiter Dashboard & Analytics", "Week 20-24", "Milestone 9", "Pipeline view, KPI reports, Charts", "Not Started"],
    ["Development - Phase 2", "Search & Filter Functionality", "Week 24-26", "Milestone 7", "Elasticsearch integration, Advanced filters", "Not Started"],
    
    ["Testing & Deployment", "Integration Testing", "Week 26-28", "All Dev Milestones", "End-to-end test cases, Bug fixes", "Not Started"],
    ["Testing & Deployment", "Performance Testing & Optimization", "Week 28-29", "Milestone 12", "Load testing, Query optimization", "Not Started"],
    ["Testing & Deployment", "UAT (User Acceptance Testing)", "Week 29-30", "Milestone 13", "User feedback, Final adjustments", "Not Started"],
    ["Testing & Deployment", "Production Deployment", "Week 30-31", "Milestone 14", "AWS deployment, Monitoring setup", "Not Started"],
    
    ["MVP Launch", "Internal MVP Launch", "Week 32", "Milestone 15", "Live system for Rudra Enterprise recruiters", "Not Started"],
    ["MVP Launch", "Post-launch Support & Bug Fixes", "Week 32-36", "Milestone 16", "Stabilization, User support", "Not Started"],
    
    ["Phase II Planning", "Client Portal Architecture", "Week 36+", "MVP Launch", "Multi-tenant design, Client features", "Future"],
    ["Phase II Planning", "AI Sourcing & Chatbot Development", "Week 36+", "MVP Launch", "LinkedIn integration, Chatbot NLP", "Future"],
]

for item in timeline_data:
    row_idx = ws_timeline.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_timeline.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)

# ============================================================================
# SHEET 7: PROJECT TIMELINE
# ============================================================================
ws_timeline = wb.create_sheet("Timeline & Milestones")
ws_timeline.append(["Phase", "Milestone", "Duration", "Dependencies", "Deliverables", "Status"])
apply_header_style(ws_timeline, 1)

timeline_data = [
    ["Planning", "Project Kickoff & Requirements Finalization", "Week 1-2", "", "Finalized PRD, WBS, Resource Plan", "In Progress"],
    ["Planning", "Technical Architecture Design", "Week 2-3", "Milestone 1", "Architecture diagram, Technology stack finalized", "Not Started"],
    ["Planning", "UI/UX Design & Wireframing", "Week 3-6", "Milestone 2", "Figma designs, User flows, Prototypes", "Not Started"],
    
    ["Development - Phase 1", "Database Schema & Backend Setup", "Week 6-8", "Milestone 3", "PostgreSQL schema, FastAPI skeleton", "Not Started"],
    ["Development - Phase 1", "Authentication & User Management", "Week 8-10", "Milestone 4", "Login, Registration, JWT implementation", "Partially Done"],
    ["Development - Phase 1", "Resume Parsing Implementation", "Week 10-13", "Milestone 4", "PDF/DOCX parsing, Data extraction", "Done"],
    ["Development - Phase 1", "AI Matching Algorithm (Core)", "Week 13-16", "Milestone 6", "Sentence-BERT integration, Match scoring", "In Progress"],
    
    ["Development - Phase 2", "Job Management Module", "Week 16-18", "Milestone 4", "Job CRUD, Job profile management", "Not Started"],
    ["Development - Phase 2", "Candidate Dashboard UI", "Week 18-20", "Milestone 5", "Dashboard with application tracking", "In Progress"],
    ["Development - Phase 2", "Recruiter Dashboard & Analytics", "Week 20-24", "Milestone 9", "Pipeline view, KPI reports, Charts", "Not Started"],
    ["Development - Phase 2", "Search & Filter Functionality", "Week 24-26", "Milestone 7", "Elasticsearch integration, Advanced filters", "Not Started"],
    
    ["Testing & Deployment", "Integration Testing", "Week 26-28", "All Dev Milestones", "End-to-end test cases, Bug fixes", "Not Started"],
    ["Testing & Deployment", "Performance Testing & Optimization", "Week 28-29", "Milestone 12", "Load testing, Query optimization", "Not Started"],
    ["Testing & Deployment", "UAT (User Acceptance Testing)", "Week 29-30", "Milestone 13", "User feedback, Final adjustments", "Not Started"],
    ["Testing & Deployment", "Production Deployment", "Week 30-31", "Milestone 14", "AWS deployment, Monitoring setup", "Not Started"],
    
    ["MVP Launch", "Internal MVP Launch", "Week 32", "Milestone 15", "Live system for Rudra Enterprise recruiters", "Not Started"],
    ["MVP Launch", "Post-launch Support & Bug Fixes", "Week 32-36", "Milestone 16", "Stabilization, User support", "Not Started"],
    
    ["Phase II Planning", "Client Portal Architecture", "Week 36+", "MVP Launch", "Multi-tenant design, Client features", "Future"],
    ["Phase II Planning", "AI Sourcing & Chatbot Development", "Week 36+", "MVP Launch", "LinkedIn integration, Chatbot NLP", "Future"],
]

for item in timeline_data:
    row_idx = ws_timeline.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_timeline.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)

auto_adjust_columns(ws_timeline)

# ============================================================================
# SHEET 8: REFERENCES & COMPETITORS
# ============================================================================
ws_ref = wb.create_sheet("References & Competitors")
ws_ref.append(["Category", "Name", "URL", "Key Features to Learn From", "Notes"])
apply_header_style(ws_ref, 1)

references = [
    ["AI Recruitment", "Talentz.ai", "https://talentz.ai", "AI-powered candidate matching, Resume parsing, Automated screening", "Primary competitor - analyze their UX"],
    ["ATS Platform", "Greenhouse", "https://www.greenhouse.com", "Pipeline management, Interview scheduling, Analytics dashboard", "Industry leader - best practices reference"],
    ["AI Interview", "Xenhire", "https://www.xenhire.com", "AI video interviews, Sentiment analysis, Auto-scoring", "Useful for AI interview features (Phase II)"],
    ["AI Interview", "AI Interview Space", "https://aiinterview.space/", "Automated video screening, Question generation", "Phase II feature inspiration"],
    ["Recruiting Software", "Skilent (Case Study)", "https://brocoders.com/case-studies/skilent-recruiting-software/", "Full recruitment cycle automation, Client portal", "Architecture reference"],
    ["AI Sourcing", "HireEZ", "https://hireez.com/", "AI-powered candidate sourcing, Boolean search, Passive candidate discovery", "Sourcing feature inspiration"],
    ["Talent Intelligence", "Aetius", "https://www.aetius.com/", "Talent analytics, Market insights, Predictive hiring", "Analytics and reporting ideas"],
    ["Recruitment Platform", "Spottal", "https://www.spottal.com/", "End-to-end recruitment, CRM features, Automation", "Overall platform design reference"],
    ["API Integration", "LinkedIn Developer", "https://developer.linkedin.com/product-catalog", "LinkedIn API documentation for job posting and candidate sourcing", "Required for Phase II integrations"],
]

for item in references:
    row_idx = ws_ref.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_ref.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)

auto_adjust_columns(ws_ref)

# ============================================================================
# SHEET 9: RISK & MITIGATION
# ============================================================================
ws_risk = wb.create_sheet("Risks & Mitigation")
ws_risk.append(["Risk ID", "Risk Description", "Probability", "Impact", "Mitigation Strategy", "Owner"])
apply_header_style(ws_risk, 1)

risks = [
    ["R01", "AI matching accuracy below expectations", "Medium", "High", "Implement feedback loop, Use pre-trained models, Extensive testing with real data", "ML Engineer"],
    ["R02", "Resume parsing errors for complex formats", "High", "Medium", "Support multiple parsing libraries, Manual review option, Continuous improvement", "Backend Dev"],
    ["R03", "Delayed hiring of key developers", "Medium", "High", "Start hiring immediately, Consider contractors, Engage consultants", "PM/RRG"],
    ["R04", "Scope creep beyond MVP", "High", "High", "Strict MVP definition, Regular scope reviews, Change control process", "PM"],
    ["R05", "Integration challenges with job boards", "Medium", "Medium", "Start with fewer integrations, Use well-documented APIs, Budget extra time", "Backend Dev"],
    ["R06", "Performance issues with large candidate database", "Low", "High", "Database optimization, Elasticsearch indexing, Load testing early", "Backend Dev"],
    ["R07", "Security vulnerabilities", "Low", "Very High", "Security audits, Penetration testing, Follow OWASP guidelines, Regular updates", "DevOps/Backend"],
    ["R08", "User adoption challenges", "Medium", "High", "User training, Intuitive UI/UX, Feedback sessions, Iterative improvements", "PM/UX Designer"],
    ["R09", "Budget overrun", "Medium", "Medium", "Detailed cost tracking, Prioritize MVP features, Avoid premature optimization", "PM/RRG"],
    ["R10", "Technology stack mismatch", "Low", "High", "Thorough architecture review, PoC for critical components, Expert consultation", "Solution Architect"],
]

for item in risks:
    row_idx = ws_risk.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_risk.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        if col_idx == 4 and value in ["High", "Very High"]:
            cell.font = Font(bold=True, color="C00000")

auto_adjust_columns(ws_risk)

# ============================================================================
# SHEET 10: API ENDPOINTS
# ============================================================================
ws_api = wb.create_sheet("API Endpoints")
ws_api.append(["Endpoint", "Method", "Description", "Request Body", "Response", "Task Type", "Priority"])
apply_header_style(ws_api, 1)

api_data = [
    ["/api/v1/auth/register", "POST", "User registration", "email, password, name, role", "user_id, token", "Backend", "MVP"],
    ["/api/v1/auth/login", "POST", "User authentication", "email, password", "token, user_info", "Backend", "MVP"],
    ["/api/v1/auth/logout", "POST", "Logout user", "token", "success message", "Backend", "MVP"],
    ["/api/v1/candidates/upload", "POST", "Upload resume and parse", "file (PDF/DOCX)", "candidate_id, parsed_data", "Backend, AI/ML", "MVP"],
    ["/api/v1/candidates", "GET", "List all candidates", "filters, pagination", "candidate_list", "Backend", "MVP"],
    ["/api/v1/candidates/{id}", "GET", "Get candidate details", "-", "candidate_profile", "Backend", "MVP"],
    ["/api/v1/candidates/{id}", "PUT", "Update candidate", "updated_fields", "success message", "Backend", "MVP"],
    ["/api/v1/candidates/{id}", "DELETE", "Delete candidate", "-", "success message", "Backend", "MVP"],
    ["/api/v1/candidates/search", "POST", "Search candidates", "query, filters", "ranked_candidates", "Backend, AI/ML", "MVP"],
    ["/api/v1/jobs", "POST", "Create job", "title, skills, experience, description", "job_id", "Backend", "MVP"],
    ["/api/v1/jobs", "GET", "List all jobs", "filters, pagination", "job_list", "Backend", "MVP"],
    ["/api/v1/jobs/{id}", "GET", "Get job details", "-", "job_info", "Backend", "MVP"],
    ["/api/v1/jobs/{id}", "PUT", "Update job", "updated_fields", "success message", "Backend", "MVP"],
    ["/api/v1/jobs/{id}", "DELETE", "Delete job", "-", "success message", "Backend", "MVP"],
    ["/api/v1/match/{job_id}", "GET", "Get ranked candidates for job", "-", "candidate_list with scores", "Backend, AI/ML", "MVP"],
    ["/api/v1/match/score", "POST", "Calculate match score", "candidate_id, job_id", "relevance_score, breakdown", "AI/ML", "MVP"],
    ["/api/v1/feedback", "POST", "Submit recruiter feedback", "candidate_id, job_id, feedback", "success message", "Backend", "MVP"],
    ["/api/v1/dashboard/recruiter", "GET", "Get recruiter dashboard data", "-", "metrics, charts_data", "Backend", "MVP"],
    ["/api/v1/reports/summary", "GET", "Get KPI summary report", "date_range", "KPI_data", "Backend", "MVP"],
    ["/api/v1/reports/export", "POST", "Export report", "report_type, format", "file_url", "Backend", "MVP"],
    ["/api/v1/email/send", "POST", "Send email to candidate", "candidate_id, template, data", "success message", "Backend", "Phase II"],
    ["/api/v1/schedule/availability", "GET", "Get interviewer availability", "interviewer_id, date_range", "available_slots", "Backend", "Phase II"],
    ["/api/v1/schedule/book", "POST", "Book interview slot", "candidate_id, interviewer_id, slot", "meeting_id, calendar_invite", "Backend", "Phase II"],
]

for item in api_data:
    row_idx = ws_api.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_api.cell(row=row_idx, column=col_idx, value=value)
        if col_idx == 6:  # Task Type
            apply_task_type_style(cell, value.split(",")[0].strip() if value else "")
        else:
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

ws_api.column_dimensions['A'].width = 35
ws_api.column_dimensions['B'].width = 10
ws_api.column_dimensions['C'].width = 35
ws_api.column_dimensions['D'].width = 35
ws_api.column_dimensions['E'].width = 35
ws_api.column_dimensions['F'].width = 20
ws_api.column_dimensions['G'].width = 12

# ============================================================================
# SHEET 11: PRICING MODELS
# ============================================================================
ws_pricing = wb.create_sheet("Pricing Models")
ws_pricing.append(["Plan", "Duration/Type", "Features", "Price", "Target Customer", "Notes"])
apply_header_style(ws_pricing, 1)

pricing_data = [
    ["Free Trial", "1 Month", "- Up to 50 candidates\n- Basic resume parsing\n- Manual job posting\n- Email support", "$0", "Trial users, Small agencies", "Limited features to test the platform"],
    ["Basic", "Monthly/Annual", "- Up to 500 candidates\n- AI matching (basic)\n- Resume parsing\n- 5 active jobs\n- Dashboard & reports\n- Email support", "$199/month or $1,990/year", "Small RPO firms, Startups", "10% discount on annual"],
    ["Premium", "Monthly/Annual", "- Up to 5,000 candidates\n- Advanced AI matching\n- 50 active jobs\n- Auto job posting (LinkedIn, Indeed)\n- Advanced analytics\n- API access\n- Priority support", "$799/month or $7,990/year", "Mid-size agencies, Growing companies", "Most popular plan"],
    ["Enterprise", "Custom", "- Unlimited candidates\n- Custom AI fine-tuning\n- Unlimited jobs\n- Multi-tenant (client portals)\n- Dedicated account manager\n- SLA guarantee\n- Custom integrations\n- White-label option", "Custom pricing", "Large RPO firms, Enterprises", "Requires consultation and custom contract"],
    ["Add-ons", "Per feature", "- AI Chatbot: $99/month\n- Interview scheduling: $149/month\n- LinkedIn sourcing: $299/month\n- Video interview platform: $199/month", "Varies", "Any plan tier", "Optional features to enhance capabilities"],
]

for item in pricing_data:
    row_idx = ws_pricing.max_row + 1
    for col_idx, value in enumerate(item, start=1):
        cell = ws_pricing.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        if "Enterprise" in str(value) or "Premium" in str(value):
            cell.font = Font(bold=True)

auto_adjust_columns(ws_pricing)

# Save workbook
output_file = os.path.join(output_dir, "RPO_SaaS_Project_Breakdown.xlsx")
wb.save(output_file)
print(f"✅ Excel file created successfully: {output_file}")
print(f"\n📊 Sheets created:")
print("   1. Project Overview - High-level project info")
print("   2. Master Task List - 59 detailed tasks with categorization")
print("   3. User Stories - 25 user stories across 6 epics")
print("   4. Technical Stack - Complete technology breakdown")
print("   5. Resource Plan - Team requirements with INR cost breakdown")
print("   6. Detailed Cost Breakdown - Complete project costing (MVP: ₹34L-82L)")
print("   7. Timeline & Milestones - Project schedule")
print("   8. References & Competitors - Market research links")
print("   9. Risks & Mitigation - Risk management plan")
print("   10. API Endpoints - Backend API specifications")
print("   11. Pricing Models - Product pricing strategy")
print(f"\n🎨 Task Types Color-Coded:")
print("   • UI - Light Purple")
print("   • Frontend - Light Green")
print("   • Backend - Light Orange")
print("   • AI/ML - Light Red")
