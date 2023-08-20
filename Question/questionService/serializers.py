from rest_framework import serializers

from .models import Question ,Category, Tag, ReferenceLink, Image

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'
        
class ReferenceLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReferenceLink
        fields = '__all__'
        
class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = '__all__'