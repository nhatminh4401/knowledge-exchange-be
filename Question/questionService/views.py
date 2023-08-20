from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .models import Question, Category, Tag, ReferenceLink, Image
from .serializers import QuestionSerializer, CategorySerializer, TagSerializer, ReferenceLinkSerializer, ImageSerializer
from django.utils.decorators import method_decorator
from .decorators import jwt_auth_required
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from cloudinary import uploader
from django.http.response import JsonResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# @csrf_exempt
# def SaveFile(request):
#     file = request.FILES['file']
#     # file_name=default_storage.save(file.name,file)
#     print(file.name, type(file))
#     result = uploader.upload(file, public_id=file.name, folder="UserApp", overwrite=True)
#     return JsonResponse(result["url"], safe=False)

class CategoryAPI(APIView):
    def get(self, request):
        categories_lst = Category.objects.all()
        srlz = CategorySerializer(categories_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def post(self, request):
        new_cat = Category.objects.create(name=request.data["category_name"])
        return self.get()
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        del_cat = Category.objects.get(category_ID = request.data["id"])
        del_cat.delete()
        return self.get()

class TagAPI(APIView):
    def get(self, request):
        tags_lst = Tag.objects.all()
        srlz = TagSerializer(tags_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def post(self, request):
        new_tag = Tag.objects.create(name=request.data["tag_name"])
        return self.get()
    
    @method_decorator(jwt_auth_required)
    def put(self, request):
        try:
            action = request.query_params.get("action")
        except ObjectDoesNotExist:
            return Response({"message": "Tag not exist."}, status=404)
        if action == "tag":
            tag = Tag.objects.get(tag_ID = request.data["id"])
            tag.questions.add(request.data["question_id"])
            return Response({"message": "Tagged."})
        elif action == "untag":
            tag = Tag.objects.get(tag_ID = request.data["id"])
            tag.questions.remove(request.data["question_id"])        
            return Response({"message": "Untagged."})
        else:
            return Response({"message": "Unavailable action."})
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            del_tag = Tag.objects.get(tag_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Tag not exist."}, status=404)
        del_tag.delete()
        return self.get()
        

class QuestionAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        question =  Question()
        question.title = request.data["title"]
        question.content = request.data["content"]
        question.status = "Pending"
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        xml_data = request_user.content
        user_data = json.loads(xml_data.decode("utf-8"))
        question.user = user_data["id"]
        category = Category.objects.get(category_ID = request.data["category_id"])
        question.category = category
        question.save()
        try:
            request_tags = request.data["tags_id"].split(",")
            for tag in request_tags:
                question.tags.add(tag)
        except:
            pass
        try:
            links = request.data["reference_links"].split(",")
            for link in links:
                new_link = ReferenceLink.objects.create(content=link, question_ID = question)
        except:
            pass
        try:
            images = request.FILES.getlist("images")
            for image in images:
                result = uploader.upload(image, public_id=image.name, folder="UserApp", overwrite=True)
                new_image = Image.objects.create(content = result["url"], question_ID = question)
        except:
            pass
        return Response({"message": "Question added successfully."})

    def get(self, request):
        sort = "-created_date"
        search = ""
        if request.query_params.get("sort"):
            sort = request.query_params.get("sort")
        if request.query_params.get("order") and request.query_params.get("order") == "desc":
            sort = "-" + sort
        if request.query_params.get("search"):
            search = request.query_params.get("search")
        if request.query_params.get("id"):
            question_lst = Question.objects.filter(question_ID = request.query_params.get("id"), title__contains = search).order_by(sort)
        elif request.query_params.get("user"):
            question_lst = Question.objects.filter(user = request.query_params.get("user"), title__contains = search).order_by(sort)
        else:
            question_lst = Question.objects.filter(title__contains = search).order_by(sort)
        if question_lst:
            srlz = QuestionSerializer(question_lst, many=True)
            for data in srlz.data:
                links = ReferenceLink.objects.filter(question_ID = int(data["question_ID"]))
                images = Image.objects.filter(question_ID = int(data["question_ID"]))
                links_srlz = ReferenceLinkSerializer(links, many = True)
                images_srlz = ImageSerializer(images, many = True)
                data["reference_links"] = links_srlz.data
                data["images"] = images_srlz.data
            return Response(srlz.data)
        else:
            return Response({"message": "Question not exist."}, status=404)

    @method_decorator(jwt_auth_required)
    def put(self, request):
        try:
            question =  Question.objects.get(question_ID = request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        question.title = request.query_params.get("title")
        question.content = request.query_params.get("content")
        question.status = request.query_params.get("status")
        category = Category.objects.get(category_ID = request.query_params.get("category_id"))
        question.category = category
        question.updated_date = datetime.now()
        question.save()
        return self.get(request)
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            question =  Question.objects.get(question_ID = request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        question.delete()
        
        return Response({"message": "Question deleted successfully."})
    
class ReferenceLinkAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        try:
            question =  Question.objects.get(question_ID = request.data["question_id"])
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        
        link  = ReferenceLink.objects.create(content = request.data["content"], question_ID = question)
        return Response({"message": "Link added successfully."})
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            link =  ReferenceLink.objects.get(ref_ID = request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Link not exist."}, status=404)
        
        link.delete()
        return Response({"message": "Link deleted successfully."})
    
class ImageAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        try:
            question =  Question.objects.get(question_ID = request.data["question_id"])
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        image_file = request.FILES("image")
        result = uploader.upload(image_file, public_id=image_file.name, folder="UserApp", overwrite=True)
        image = Image.objects.create(content = result["url"], question_ID = question)
        return Response({"message": "Image added successfully."})
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            image =  Image.objects.get(img_ID = request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Image not exist."}, status=404)
        
        image.delete()
        return Response({"message": "Image deleted successfully."})