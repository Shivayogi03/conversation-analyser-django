# analysis/serializers.py
from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','sender','text','timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id','title','raw_json','created_at','messages']

class ConversationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True)
    messages = serializers.ListField(child=serializers.DictField(), allow_empty=False)
    # Example message dict: {"sender":"user","message":"Hi"}
    
    def create(self, validated_data):
        from .models import Conversation, Message
        title = validated_data.get('title','')
        conv = Conversation.objects.create(title=title, raw_json=validated_data)
        for m in validated_data['messages']:
            text = m.get('message') or m.get('text') or ''
            sender = m.get('sender','user')
            Message.objects.create(conversation=conv, sender=sender, text=text)
        return conv

class ConversationAnalysisSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer()
    class Meta:
        model = ConversationAnalysis
        fields = '__all__'
