# analysis/models.py
from django.db import models

class Conversation(models.Model):
    title = models.CharField(max_length=255, blank=True)
    raw_json = models.JSONField(blank=True, null=True)   # store original payload
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.title or 'untitled'}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=20)  # "user" or "ai"
    text = models.TextField()
    timestamp = models.DateTimeField(null=True, blank=True)  # optional
    def __str__(self):
        return f"{self.sender}: {self.text[:50]}"

class ConversationAnalysis(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name="analysis")
    summary = models.TextField(null=True, blank=True)  # ✅ add this
    clarity_score = models.FloatField()
    relevance_score = models.FloatField()
    accuracy_score = models.FloatField()
    completeness_score = models.FloatField()
    empathy_score = models.FloatField()
    sentiment = models.CharField(max_length=20)
    fallback_count = models.IntegerField()
    resolution = models.BooleanField()
    resolution_rate = models.FloatField()
    avg_response_time = models.FloatField(null=True, blank=True)
    escalation_need = models.BooleanField()
    overall_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Analysis for conv {self.conversation_id} - score {self.overall_score:.2f}"
