from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .models import Question, Category, Tag
from .serializers import QuestionSerializer, CategorySerializer, TagSerializer
from django.utils.decorators import method_decorator
from .decorators import jwt_auth_required
from rest_framework.views import APIView
import json


# Create your views here.
class CategoryAPI(APIView):
    def get(self, request):
        categories_lst = Category.objects.all()
        srlz = CategorySerializer(categories_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def post(self, request):
        new_cat = Category.objects.create(name=request.data["category_name"])
        categories_lst = Category.objects.all()
        srlz = CategorySerializer(categories_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        del_cat = Category.objects.get(category_ID = request.data["id"])
        del_cat.delete()
        categories_lst = Category.objects.all()
        srlz = CategorySerializer(categories_lst, many=True)
        return Response(srlz.data)

class TagAPI(APIView):
    def get(self, request):
        tags_lst = Tag.objects.all()
        srlz = TagSerializer(tags_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def post(self, request):
        new_tag = Tag.objects.create(name=request.data["tag_name"])
        tags_lst = Tag.objects.all()
        srlz = TagSerializer(tags_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        del_tag = Tag.objects.get(tag_ID = request.data["id"])
        del_tag.delete()
        tags_lst = Tag.objects.all()
        srlz = TagSerializer(tags_lst, many=True)
        return Response(srlz.data)

class QuestionAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        question =  Question()
        question.title = request.data["title"]
        question.content = request.data["content"]
        question.status = "Pending"
        request_user = requests.get("http://127.0.0.1:8000/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        xml_data = request_user.content
        user_data = json.loads(xml_data.decode("utf-8"))
        question.user = user_data["id"]
        category = Category.objects.get(category_ID = request.data["category_id"])
        question.category = category
        question.save()
        request_tags = request.data["tags_id"].split(",")
        for tag in request_tags:
            question.tags.add(tag)
        
        return Response({"message": "Question added successfully"}, status=300)

    def get(self, request):
        if request.query_params.get("id"):
            question_lst = Question.objects.filter(question_ID = request.query_params.get("id"))
        else:
            question_lst = Question.objects.all()
        if question_lst:
            srlz = QuestionSerializer(question_lst, many=True)
            return Response(srlz.data, status=200)
        else:
            return Response({"message": "Sorry not found!"}, status=404)