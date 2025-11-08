# analysis/tasks.py

from celery import shared_task  # ✅ new import for Celery
from .models import Conversation, ConversationAnalysis
from .analysis_utils import perform_analysis

@shared_task  # ✅ makes this callable by Celery Beat
def daily_analyse_new_conversations():
    """
    This function will be invoked automatically by Celery Beat.
    It finds conversations without analysis and analyses them.
    """
    new_convs = Conversation.objects.filter(analysis__isnull=True)
    for conv in new_convs:
        metrics = perform_analysis(conv)
        ConversationAnalysis.objects.create(
            conversation=conv,
            clarity_score=metrics['clarity_score'],
            relevance_score=metrics['relevance_score'],
            accuracy_score=metrics['accuracy_score'],
            completeness_score=metrics['completeness_score'],
            empathy_score=metrics['empathy_score'],
            sentiment=metrics['sentiment'],
            fallback_count=metrics['fallback_count'],
            resolution=metrics['resolution'],
            avg_response_time=metrics['avg_response_time'],
            escalation_need=metrics['escalation_need'],
            resolution_rate=metrics['resolution_rate'],
            overall_score=metrics['overall_score'],
        )

    return f"Analysed {new_convs.count()} new conversations ✅"
