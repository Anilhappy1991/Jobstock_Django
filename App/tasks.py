"""
Background Tasks for Document Processing
Location: App/tasks.py

This module contains Celery tasks for processing documents using:
- LayoutParser: For document layout analysis
- SpaCy: For NLP and entity extraction
- Transformers: For advanced document understanding
"""
import os
import logging
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
import spacy
from transformers import AutoTokenizer, AutoModel
import layoutparser as lp
import cv2
import numpy as np
from pdf2image import convert_from_path
import torch

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Document processor using LayoutParser, SpaCy, and Transformers
    """
    
    def __init__(self):
        """Initialize models"""
        self.nlp = None
        self.tokenizer = None
        self.model = None
        self.layout_model = None
        
    def load_models(self):
        """Lazy load models to save memory"""
        if self.nlp is None:
            logger.info("Loading SpaCy model...")
            self.nlp = spacy.load(settings.SPACY_MODEL)
            
        if self.tokenizer is None or self.model is None:
            logger.info("Loading Transformers model...")
            self.tokenizer = AutoTokenizer.from_pretrained(settings.TRANSFORMERS_MODEL)
            self.model = AutoModel.from_pretrained(settings.TRANSFORMERS_MODEL)
            
        if self.layout_model is None:
            logger.info("Loading LayoutParser model...")
            self.layout_model = lp.Detectron2LayoutModel(
                settings.LAYOUTPARSER_MODEL,
                extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
            )
    
    def analyze_layout(self, image_path):
        """
        Analyze document layout using LayoutParser
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Layout analysis results
        """
        self.load_models()
        
        # Load image
        image = cv2.imread(image_path)
        image = image[..., ::-1]  # Convert BGR to RGB
        
        # Detect layout
        layout = self.layout_model.detect(image)
        
        # Extract layout elements
        elements = []
        for block in layout:
            elements.append({
                'type': block.type,
                'coordinates': {
                    'x1': int(block.block.x_1),
                    'y1': int(block.block.y_1),
                    'x2': int(block.block.x_2),
                    'y2': int(block.block.y_2)
                },
                'score': float(block.score)
            })
        
        return {
            'total_elements': len(elements),
            'elements': elements,
            'element_types': [e['type'] for e in elements]
        }
    
    def extract_entities(self, text):
        """
        Extract named entities using SpaCy
        
        Args:
            text: Input text
            
        Returns:
            dict: Extracted entities
        """
        self.load_models()
        
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        # Extract key information
        persons = [e['text'] for e in entities if e['label'] == 'PERSON']
        organizations = [e['text'] for e in entities if e['label'] == 'ORG']
        dates = [e['text'] for e in entities if e['label'] == 'DATE']
        locations = [e['text'] for e in entities if e['label'] in ['GPE', 'LOC']]
        
        return {
            'total_entities': len(entities),
            'entities': entities,
            'persons': persons,
            'organizations': organizations,
            'dates': dates,
            'locations': locations
        }
    
    def analyze_with_transformers(self, text):
        """
        Analyze document using Transformers
        
        Args:
            text: Input text
            
        Returns:
            dict: Analysis results
        """
        self.load_models()
        
        # Tokenize and get embeddings
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Get the embedding of the [CLS] token
        embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        
        return {
            'embedding_shape': embeddings.shape,
            'embedding_mean': float(embeddings.mean()),
            'embedding_std': float(embeddings.std()),
            'token_count': len(inputs['input_ids'][0])
        }


@shared_task(bind=True, name='process_resume_document')
def process_resume_document(self, resume_path, profile_id):
    """
    Background task to process resume document
    
    Args:
        resume_path: Path to the resume file
        profile_id: Profile ID associated with the resume
        
    Returns:
        dict: Processing results
    """
    try:
        logger.info(f"Starting resume processing for profile {profile_id}")
        self.update_state(state='PROCESSING', meta={'status': 'Initializing...'})
        
        processor = DocumentProcessor()
        results = {
            'profile_id': profile_id,
            'processed_at': timezone.now().isoformat(),
            'status': 'processing'
        }
        
        # Step 1: Convert PDF to images if needed
        if resume_path.lower().endswith('.pdf'):
            self.update_state(state='PROCESSING', meta={'status': 'Converting PDF to images...'})
            images = convert_from_path(resume_path, dpi=300)
            image_path = os.path.join(
                settings.DOCUMENT_PROCESSING_DIR,
                f'resume_{profile_id}_page1.jpg'
            )
            images[0].save(image_path, 'JPEG')
        else:
            image_path = resume_path
        
        # Step 2: Layout Analysis
        self.update_state(state='PROCESSING', meta={'status': 'Analyzing document layout...'})
        layout_results = processor.analyze_layout(image_path)
        results['layout_analysis'] = layout_results
        logger.info(f"Layout analysis complete: {layout_results['total_elements']} elements found")
        
        # Step 3: Extract text (simplified - you'd use OCR in production)
        # For now, assuming text extraction is done elsewhere
        # In production, use pytesseract or other OCR tools
        sample_text = "Sample resume text for processing"  # Replace with actual OCR
        
        # Step 4: Named Entity Recognition
        self.update_state(state='PROCESSING', meta={'status': 'Extracting entities...'})
        entity_results = processor.extract_entities(sample_text)
        results['entity_extraction'] = entity_results
        logger.info(f"Entity extraction complete: {entity_results['total_entities']} entities found")
        
        # Step 5: Transformer Analysis
        self.update_state(state='PROCESSING', meta={'status': 'Performing deep analysis...'})
        transformer_results = processor.analyze_with_transformers(sample_text)
        results['transformer_analysis'] = transformer_results
        logger.info("Transformer analysis complete")
        
        # Cleanup temporary files
        if os.path.exists(image_path) and image_path != resume_path:
            os.remove(image_path)
        
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


@shared_task(bind=True, name='process_job_description')
def process_job_description(self, job_description_text, job_id):
    """
    Background task to process job description
    
    Args:
        job_description_text: Job description text
        job_id: Job ID
        
    Returns:
        dict: Processing results
    """
    try:
        logger.info(f"Starting job description processing for job {job_id}")
        
        processor = DocumentProcessor()
        
        # Extract entities from job description
        entity_results = processor.extract_entities(job_description_text)
        
        # Analyze with transformers
        transformer_results = processor.analyze_with_transformers(job_description_text)
        
        results = {
            'job_id': job_id,
            'processed_at': timezone.now().isoformat(),
            'entity_extraction': entity_results,
            'transformer_analysis': transformer_results,
            'status': 'completed'
        }
        
        logger.info(f"Job description processing completed for job {job_id}")
        return results
        
    except Exception as e:
        logger.error(f"Error processing job description: {str(e)}", exc_info=True)
        raise


@shared_task(bind=True, name='match_resume_to_jobs')
def match_resume_to_jobs(self, profile_id, job_ids):
    """
    Background task to match resume to multiple jobs
    
    Args:
        profile_id: Profile ID
        job_ids: List of job IDs to match against
        
    Returns:
        dict: Matching results
    """
    try:
        logger.info(f"Starting resume matching for profile {profile_id} against {len(job_ids)} jobs")
        
        # This would implement actual matching logic
        # For now, returning a placeholder
        
        results = {
            'profile_id': profile_id,
            'matched_jobs': len(job_ids),
            'matches': [
                {
                    'job_id': job_id,
                    'match_score': 0.75,  # Placeholder
                    'matched_skills': [],
                    'matched_entities': []
                }
                for job_id in job_ids
            ],
            'processed_at': timezone.now().isoformat(),
            'status': 'completed'
        }
        
        logger.info(f"Resume matching completed for profile {profile_id}")
        return results
        
    except Exception as e:
        logger.error(f"Error matching resume: {str(e)}", exc_info=True)
        raise


@shared_task(name='cleanup_temp_files')
def cleanup_temp_files():
    """
    Periodic task to cleanup temporary processing files
    """
    try:
        logger.info("Starting cleanup of temporary files")
        
        temp_dir = settings.DOCUMENT_PROCESSING_DIR
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                # Delete files older than 24 hours
                if os.path.isfile(file_path):
                    file_age = timezone.now().timestamp() - os.path.getmtime(file_path)
                    if file_age > 86400:  # 24 hours in seconds
                        os.remove(file_path)
                        logger.info(f"Deleted old temp file: {file}")
        
        logger.info("Cleanup completed")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
