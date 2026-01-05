from django.db import models


class ImageDocument(models.Model):
    """
    Model to store image document metadata
    """
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    file_name = models.CharField(max_length=500)
    file_size = models.IntegerField()  # in bytes
    file_hash = models.CharField(max_length=64, unique=True)  # SHA256 hash
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=50, default="image/jpeg")
    format = models.CharField(max_length=20)  # jpeg, png, webp, etc.
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


class ImageAnalysis(models.Model):
    """
    Model to store image analysis results and metadata
    """
    image_document = models.OneToOneField(ImageDocument, on_delete=models.CASCADE, related_name='analysis')
    analysis_text = models.TextField()
    extracted_text = models.TextField(null=True, blank=True)  # OCR results
    objects_detected = models.JSONField(null=True, blank=True)  # Detected objects
    analysis_time_ms = models.IntegerField(null=True, blank=True)
    model_used = models.CharField(max_length=100, default="gemini-vision")
    confidence_scores = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analysis of {self.image_document.file_name}"


class ImageQuery(models.Model):
    """
    Model to store queries made against images
    """
    image_document = models.ForeignKey(ImageDocument, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    response_text = models.TextField()
    response_time_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query on {self.image_document.file_name}"
