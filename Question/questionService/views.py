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
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
# @csrf_exempt
# def SaveFile(request):
#     file = request.FILES['file']
#     # file_name=default_storage.save(file.name,file)
#     print(file.name, type(file))
#     result = uploader.upload(file, public_id=file.name, folder="UserApp", overwrite=True)
#     return JsonResponse(result["url"], safe=False)

class CategoryAPI(APIView):
    def get(self):
        categories_lst = Category.objects.all()
        srlz = CategorySerializer(categories_lst, many=True)
        return Response(srlz.data)
    
    @method_decorator(jwt_auth_required)
    def post(self, request):
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["isAdmin"] != True:
            return Response({"message": "User is not Administator."}, status=403)
        new_cat = Category.objects.create(name=request.data["category_name"])
        return self.get()
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["isAdmin"] != True:
            return Response({"message": "User is not Administator."}, status=403)
        try:
            del_cat = Category.objects.get(category_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Category not exist."}, status=404)   
        del_cat.delete()
        return self.get()

class TagAPI(APIView):
    def get(self):
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
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["isAdmin"] != True:
            return Response({"message": "User is not Administator."}, status=403)
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
        user_data = json.loads(request_user.content)
        question.user = user_data["id"]
        category = Category.objects.get(category_ID = request.data["category_id"])
        question.category = category
        question.save()
        if "tags_id" in request.data.keys():
            request_tags = request.data["tags_id"].split(",")
            for tag in request_tags:
                question.tags.add(tag)
        if "reference_links" in request.data.keys():
            links = request.data["reference_links"].split(",")
            for link in links:
                new_link = ReferenceLink.objects.create(content=link, question_ID = question)
        if "images" in request.data.keys():
            images = request.FILES.getlist("images")
            for image in images:
                new_image = Image.objects.create(question_ID = question)
                result = uploader.upload(image, public_id=new_image.img_ID, folder="UserApp", overwrite=True)
                new_image.content = result["url"]
                new_image.save()
        return Response({"message": "Question added successfully."})

    def get(self, request):
        sort = "-created_date"
        search = ""
        if request.query_params.get("sort"):
            sort = request.query_params.get("sort")
        if request.query_params.get("order") and request.query_params.get("order") == "desc" and request.query_params.get("sort"):
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
        
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if "status" in request.data.keys():
            if user_data["isAdmin"] == True:
                question.status = request.data["status"]
                question.save()
            else:
                return Response({"message": "You are not Administator."}, status=403)
        if user_data["id"] != question.user:
            return Response({"message": "User does not have permission."}, status=403)
        if "title" in request.data.keys():
            question.title = request.data["title"]
        if "content" in request.data.keys():
            question.content = request.data["content"]
        if "category_id" in request.data.keys():
            category = Category.objects.get(category_ID = request.data["category_id"])
            question.category = category
        question.updated_date = datetime.now()
        question.save()
        return self.get(request)
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != question.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        try:
            question =  Question.objects.get(question_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        question.delete()
        
        return Response({"message": "Question deleted successfully."})
    
class ReferenceLinkAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        try:
            question =  Question.objects.get(question_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != question.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        link  = ReferenceLink.objects.create(content = request.data["content"], question_ID = question)
        return Response({"message": "Link added successfully."})
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            link =  ReferenceLink.objects.get(ref_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Link not exist."}, status=404)
        try:
            question =  Question.objects.get(question_ID = link.question_ID)
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != question.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        
        link.delete()
        return Response({"message": "Link deleted successfully."})
    
class ImageAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        try:
            question =  Question.objects.get(question_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != question.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        image_file = request.FILES["image"]
        image = Image.objects.create(question_ID = question)
        result = uploader.upload(image_file, public_id=image.img_ID, folder="UserApp", overwrite=True)
        image.content = result["url"]
        image.save()
        return Response({"message": "Image added successfully."})
    
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            image = Image.objects.get(img_ID = request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Image not exist."}, status=404)
        try:
            question =  Question.objects.get(question_ID = image.question_ID)
        except ObjectDoesNotExist:
            return Response({"message": "Question not exist."}, status=404)
        request_user = requests.get("http://127.0.0.1:8001/user/", headers={"Authorization":request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != question.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        result = uploader.destroy(public_id = "UserApp/" + str(image.img_ID))
        image.delete()
        return Response({"message": "Image deleted successfully."})