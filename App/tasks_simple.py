"""
Simplified Background Tasks for Document Processing (Windows-Compatible)
Location: App/tasks_simple.py

This module uses Windows-compatible libraries:
- NLTK: For NLP and entity extraction
- PDFPlumber: For PDF text extraction
- TextBlob: For sentiment analysis
- PyPDF2: For PDF manipulation
"""
import os
import re
import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
import pdfplumber
import PyPDF2
from docx import Document
import nltk
from textblob import TextBlob
from collections import Counter

logger = logging.getLogger(__name__)


class SimpleDocumentProcessor:
    """
    Simplified document processor using Windows-compatible libraries
    """
    
    def __init__(self):
        """Initialize NLTK data"""
        try:
            # Download required NLTK data
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF using pdfplumber
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            str: Extracted text
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            logger.info(f"Extracted {len(text)} characters from PDF")
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                logger.error(f"PyPDF2 fallback also failed: {str(e2)}")
        
        return text.strip()
    
    def extract_text_from_docx(self, docx_path):
        """
        Extract text from DOCX file
        
        Args:
            docx_path: Path to DOCX file
            
        Returns:
            str: Extracted text
        """
        try:
            doc = Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info(f"Extracted {len(text)} characters from DOCX")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            return ""
    
    def extract_text_from_txt(self, txt_path):
        """
        Extract text from TXT file
        
        Args:
            txt_path: Path to TXT file
            
        Returns:
            str: Extracted text
        """
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()
            logger.info(f"Extracted {len(text)} characters from TXT")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {str(e)}")
            return ""
    
    def extract_text(self, file_path):
        """
        Extract text from various file formats
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Extracted text
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            logger.warning(f"Unsupported file format: {ext}")
            return ""
    
    def extract_entities(self, text):
        """
        Extract named entities using NLTK
        
        Args:
            text: Input text
            
        Returns:
            dict: Extracted entities
        """
        from nltk import word_tokenize, pos_tag, ne_chunk
        from nltk.chunk import tree2conlltags
        
        # Tokenize and tag
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        
        # Named entity recognition
        named_entities = ne_chunk(pos_tags, binary=False)
        
        # Extract entities
        entities = []
        for chunk in named_entities:
            if hasattr(chunk, 'label'):
                entity_text = ' '.join(c[0] for c in chunk)
                entities.append({
                    'text': entity_text,
                    'label': chunk.label(),
                })
        
        # Categorize entities
        persons = [e['text'] for e in entities if e['label'] == 'PERSON']
        organizations = [e['text'] for e in entities if e['label'] == 'ORGANIZATION']
        locations = [e['text'] for e in entities if e['label'] in ['GPE', 'LOCATION']]
        
        return {
            'total_entities': len(entities),
            'entities': entities,
            'persons': list(set(persons)),
            'organizations': list(set(organizations)),
            'locations': list(set(locations))
        }
    
    def extract_contact_info(self, text):
        """
        Extract contact information using regex
        
        Args:
            text: Input text
            
        Returns:
            dict: Contact information
        """
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Phone pattern (various formats)
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text.lower())
        
        # GitHub pattern
        github_pattern = r'github\.com/[\w-]+'
        github = re.findall(github_pattern, text.lower())
        
        return {
            'emails': list(set(emails)),
            'phones': list(set([''.join(p) for p in phones if p])),
            'linkedin': list(set(linkedin)),
            'github': list(set(github))
        }
    
    def extract_skills(self, text):
        """
        Extract skills/keywords from text
        
        Args:
            text: Input text
            
        Returns:
            dict: Extracted skills
        """
        # Common tech skills
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Laravel',
            'HTML', 'CSS', 'Bootstrap', 'Tailwind', 'jQuery',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
            'Git', 'GitHub', 'GitLab', 'Bitbucket',
            'Machine Learning', 'Deep Learning', 'AI', 'NLP', 'Computer Vision',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
        ]
        
        # Find skills in text (case-insensitive)
        text_lower = text.lower()
        found_skills = []
        
        for skill in tech_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Extract years of experience
        exp_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        experience_matches = re.findall(exp_pattern, text_lower)
        
        return {
            'skills': found_skills,
            'total_skills': len(found_skills),
            'experience_years': [int(exp) for exp in experience_matches]
        }
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text using TextBlob
        
        Args:
            text: Input text
            
        Returns:
            dict: Sentiment analysis
        """
        blob = TextBlob(text)
        sentiment = blob.sentiment
        
        return {
            'polarity': sentiment.polarity,  # -1 to 1
            'subjectivity': sentiment.subjectivity,  # 0 to 1
            'sentiment_label': 'positive' if sentiment.polarity > 0 else 'negative' if sentiment.polarity < 0 else 'neutral'
        }
    
    def get_text_statistics(self, text):
        """
        Get basic text statistics
        
        Args:
            text: Input text
            
        Returns:
            dict: Text statistics
        """
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize, sent_tokenize
        
        # Basic counts
        char_count = len(text)
        word_tokens = word_tokenize(text.lower())
        word_count = len(word_tokens)
        sentence_count = len(sent_tokenize(text))
        
        # Remove stopwords and get most common words
        stop_words = set(stopwords.words('english'))
        filtered_words = [w for w in word_tokens if w.isalnum() and w not in stop_words]
        most_common = Counter(filtered_words).most_common(10)
        
        return {
            'character_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(word_count / sentence_count, 2) if sentence_count > 0 else 0,
            'unique_words': len(set(filtered_words)),
            'most_common_words': [{'word': word, 'count': count} for word, count in most_common]
        }


@shared_task(bind=True, name='process_resume_simple')
def process_resume_simple(self, resume_path, profile_id):
    """
    Simplified background task to process resume
    
    Args:
        resume_path: Path to the resume file
        profile_id: Profile ID associated with the resume
        
    Returns:
        dict: Processing results
    """
    try:
        logger.info(f"Starting resume processing for profile {profile_id}")
        self.update_state(state='PROCESSING', meta={'status': 'Initializing...'})
        
        processor = SimpleDocumentProcessor()
        results = {
            'profile_id': profile_id,
            'processed_at': timezone.now().isoformat(),
            'status': 'processing'
        }
        
        # Step 1: Extract text
        self.update_state(state='PROCESSING', meta={'status': 'Extracting text from document...'})
        text = processor.extract_text(resume_path)
        
        if not text:
            raise ValueError("No text could be extracted from the document")
        
        results['text_length'] = len(text)
        logger.info(f"Extracted {len(text)} characters")
        
        # Step 2: Extract contact information
        self.update_state(state='PROCESSING', meta={'status': 'Extracting contact information...'})
        contact_info = processor.extract_contact_info(text)
        results['contact_info'] = contact_info
        logger.info(f"Found {len(contact_info['emails'])} emails, {len(contact_info['phones'])} phones")
        
        # Step 3: Extract entities
        self.update_state(state='PROCESSING', meta={'status': 'Extracting named entities...'})
        entity_results = processor.extract_entities(text)
        results['entities'] = entity_results
        logger.info(f"Found {entity_results['total_entities']} entities")
        
        # Step 4: Extract skills
        self.update_state(state='PROCESSING', meta={'status': 'Identifying skills...'})
        skills_results = processor.extract_skills(text)
        results['skills'] = skills_results
        logger.info(f"Found {skills_results['total_skills']} skills")
        
        # Step 5: Text statistics
        self.update_state(state='PROCESSING', meta={'status': 'Analyzing text...'})
        stats = processor.get_text_statistics(text)
        results['statistics'] = stats
        
        # Step 6: Sentiment analysis
        sentiment = processor.analyze_sentiment(text)
        results['sentiment'] = sentiment
        
        results['status'] = 'completed'
        logger.info(f"Resume processing completed for profile {profile_id}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}", exc_info=True)
        self.update_state(
            state='FAILURE',
            meta={'error': str(e), 'status': 'failed'}
        )
        raise


@shared_task(bind=True, name='match_resume_simple')
def match_resume_simple(self, profile_id, job_description):
    """
    Simple resume-job matching
    
    Args:
        profile_id: Profile ID
        job_description: Job description text
        
    Returns:
        dict: Match results
    """
    try:
        logger.info(f"Starting simple matching for profile {profile_id}")
        
        processor = SimpleDocumentProcessor()
        
        # Extract skills from job description
        job_skills = processor.extract_skills(job_description)
        
        # This would compare with stored resume data
        # For now, returning structure
        
        results = {
            'profile_id': profile_id,
            'required_skills': job_skills['skills'],
            'match_score': 0.75,  # Placeholder
            'processed_at': timezone.now().isoformat(),
            'status': 'completed'
        }
        
        logger.info(f"Matching completed for profile {profile_id}")
        return results
        
    except Exception as e:
        logger.error(f"Error in matching: {str(e)}", exc_info=True)
        raise


@shared_task(name='cleanup_temp_files_simple')
def cleanup_temp_files_simple():
    """
    Periodic task to cleanup temporary files
    """
    try:
        logger.info("Starting cleanup of temporary files")
        
        temp_dir = settings.DOCUMENT_PROCESSING_DIR
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if os.path.isfile(file_path):
                    file_age = timezone.now().timestamp() - os.path.getmtime(file_path)
                    if file_age > 86400:  # 24 hours
                        os.remove(file_path)
                        logger.info(f"Deleted old temp file: {file}")
        
        logger.info("Cleanup completed")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
