from django.db import models


class TextDocument(models.Model):
    """
    Model to store text document metadata
    """
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    file_name = models.CharField(max_length=500)
    file_size = models.IntegerField()  # in bytes
    file_hash = models.CharField(max_length=64, unique=True)  # SHA256 hash
    content_length = models.IntegerField()  # Character count
    line_count = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    mime_type = models.CharField(max_length=50, default="text/plain")
    encoding = models.CharField(max_length=20, default="utf-8")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadata
    original_filename = models.CharField(max_length=500, null=True, blank=True)
    upload_ip = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"{self.file_name} ({self.session_id})"


class TextChunk(models.Model):
    """
    Model to store text document chunks for vector embeddings
    """
    text_document = models.ForeignKey(TextDocument, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()  # Order of chunk in document
    text_content = models.TextField()
    chunk_size = models.IntegerField()  # Character count
    line_range = models.CharField(max_length=100, help_text="e.g., '1-50'")
    embedding_vector_id = models.CharField(max_length=255, null=True, blank=True)  # FAISS vector ID
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['text_document', 'chunk_index']
        indexes = [
            models.Index(fields=['text_document', 'chunk_index']),
        ]
    
    def __str__(self):
        return f"Chunk {self.chunk_index} - {self.text_document.file_name}"


class TextQuery(models.Model):
    """
    Model to store queries made against text documents for analytics
    """
    text_document = models.ForeignKey(TextDocument, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    response_text = models.TextField()
    response_time_ms = models.IntegerField(null=True, blank=True)
    relevant_chunks_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query on {self.text_document.file_name}"
