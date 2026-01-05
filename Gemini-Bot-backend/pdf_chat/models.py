from django.db import models
from django.utils import timezone


class PDFDocument(models.Model):
    """
    Model to store PDF document metadata
    """
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    file_name = models.CharField(max_length=500)
    file_size = models.IntegerField()  # in bytes
    file_hash = models.CharField(max_length=64, unique=True)  # SHA256 hash
    page_count = models.IntegerField(default=0)
    text_content_length = models.IntegerField(default=0)
    embedding_index_path = models.CharField(max_length=500)  # Path to FAISS index
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadata
    original_filename = models.CharField(max_length=500, null=True, blank=True)
    mime_type = models.CharField(max_length=50, default="application/pdf")
    upload_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"{self.file_name} ({self.session_id})"


class PDFChunk(models.Model):
    """
    Model to store PDF text chunks for vector embeddings
    """
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()  # Order of chunk in document
    text_content = models.TextField()
    chunk_size = models.IntegerField()  # Character count
    page_numbers = models.CharField(max_length=255, help_text="Comma-separated page numbers")
    embedding_vector_id = models.CharField(max_length=255, null=True, blank=True)  # FAISS vector ID
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['pdf_document', 'chunk_index']
        indexes = [
            models.Index(fields=['pdf_document', 'chunk_index']),
        ]
    
    def __str__(self):
        return f"Chunk {self.chunk_index} - {self.pdf_document.file_name}"


class PDFQuery(models.Model):
    """
    Model to store queries made against PDF documents for analytics
    """
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    response_text = models.TextField()
    response_time_ms = models.IntegerField(null=True, blank=True)
    relevant_chunks_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query on {self.pdf_document.file_name}"
