from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# analysis/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Conversation, Message, ConversationAnalysis
from .serializers import ConversationCreateSerializer, ConversationSerializer, ConversationAnalysisSerializer
from .analysis_utils import perform_analysis
from .analysis_utils import perform_analysis
from .models import ConversationAnalysis

# @api_view(['POST'])
# def upload_conversation(request):
#     """
#     POST /api/conversations/
#     Body:
#     {
#       "title":"Order chat 1",
#       "messages":[{"sender":"user","message":"Hi"}, {"sender":"ai","message":"Hello"}]
#     }
#     """
#     serializer = ConversationCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         conv = serializer.save()
#         return Response(ConversationSerializer(conv).data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upload_conversation(request):
    serializer = ConversationCreateSerializer(data=request.data)
    if serializer.is_valid():
        conv = serializer.save()

        # ⚡ Automatically analyse the conversation
        metrics = perform_analysis(conv)
        ConversationAnalysis.objects.update_or_create(
            conversation=conv,
            defaults={
                'clarity_score': metrics['clarity_score'],
                'relevance_score': metrics['relevance_score'],
                'accuracy_score': metrics['accuracy_score'],
                'completeness_score': metrics['completeness_score'],
                'empathy_score': metrics['empathy_score'],
                'sentiment': metrics['sentiment'],
                'fallback_count': metrics['fallback_count'],
                'resolution': metrics['resolution'],
                'avg_response_time': metrics['avg_response_time'],
                'escalation_need': metrics['escalation_need'],
                'resolution_rate': metrics['resolution_rate'],
                'overall_score': metrics['overall_score'],
            }
        )

        # ✅ Return full response including analysis
        return Response({
            "conversation": ConversationSerializer(conv).data,
            "analysis": metrics
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def analyse_conversation(request, conv_id):
    """
    POST /api/analyse/<conv_id>/
    Trigger analysis and store ConversationAnalysis instance.
    """
    try:
        conv = Conversation.objects.get(id=conv_id)
    except Conversation.DoesNotExist:
        return Response({"detail":"Conversation not found"}, status=404)
    metrics = perform_analysis(conv)
    # create or update ConversationAnalysis
    analysis, created = ConversationAnalysis.objects.update_or_create(
        conversation=conv,
        defaults={
            'clarity_score': metrics['clarity_score'],
            'relevance_score': metrics['relevance_score'],
            'accuracy_score': metrics['accuracy_score'],
            'completeness_score': metrics['completeness_score'],
            'empathy_score': metrics['empathy_score'],
            'sentiment': metrics['sentiment'],
            'fallback_count': metrics['fallback_count'],
            'resolution': metrics['resolution'],
            'avg_response_time': metrics['avg_response_time'],
            'escalation_need': metrics['escalation_need'],
            'resolution_rate': metrics['resolution_rate'],
            'overall_score': metrics['overall_score'],
        }
    )
    return Response(ConversationAnalysisSerializer(analysis).data, status=200)

class AnalysisListView(generics.ListAPIView):
    queryset = ConversationAnalysis.objects.select_related('conversation').all().order_by('-created_at')
    serializer_class = ConversationAnalysisSerializer

