from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .models import Answer, ReferenceLink, Image
from .serializers import AnswerSerializer, ReferenceLinkSerializer, ImageSerializer
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
from Answer.settings import USER_API_URL, QUESTION_API_URL
# Create your views here.


@csrf_exempt
def SaveFile(request):
    file = request.FILES['file']
    # file_name=default_storage.save(file.name,file)
    print(file.name, type(file))
    result = uploader.upload(file, public_id=file.name,
                             folder="UserApp", overwrite=True)
    return JsonResponse(result["url"], safe=False)


class AnswerAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        required_fields = ["content",
                           "question_id"]  # Trường bắt buộc

        # Kiểm tra các trường bắt buộc
        for field in required_fields:
            if field not in request.data:
                return Response({"message": f"Missing required field: {field}"}, status=400)

        # Kiểm tra trường bắt buộc question_id
        if "question_id" not in request.data:
            return Response({"message": "Missing required field: question_id"}, status=400)

        answer = Answer()
        answer.content = request.data["content"]

        user_data = None
        user_response = requests.get(USER_API_URL + "user/", headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')
        })

        if user_response.status_code == 200:
            user_data = json.loads(user_response.content)
        else:
            return Response({"message": "User not found."}, status=404)

        answer_user_id = user_data.get("id")
        if not answer_user_id:
            return Response({"message": "User data does not contain ID."}, status=400)

        answer.user = answer_user_id

        preAnswer_ID = request.data.get("preAnswer_ID")
        if preAnswer_ID:
            answer_parent = Answer.objects.filter(
                answer_ID=preAnswer_ID).first()
            if not answer_parent:
                return Response({"message": "Parent answer not found."}, status=404)

        question_id = request.data["question_id"]
        question_response = requests.get(
            QUESTION_API_URL + f"questions?id={question_id}")

        if question_response.status_code != 200:
            return Response({"message": "Question not found."}, status=404)
        answer.question_ID = question_id
        answer.save()

        if "reference_links" in request.data:
            links = request.data["reference_links"].split(",")
            for link in links:
                new_link = ReferenceLink.objects.create(
                    content=link, answer_ID=answer)

        if "images" in request.FILES:
            images = request.FILES.getlist("images")
            for image in images:
                new_image = Image.objects.create(answer_ID=answer)
                result = uploader.upload(
                    image, public_id=new_image.img_ID, folder="UserApp", overwrite=True)
                new_image.content = result["url"]
                new_image.save()

        return Response({"message": "Answer added successfully."})

    def get(self, request):
        # Danh sách các giá trị hợp lệ cho trường "sort"
        valid_sort_values = ["created_date", "content"]

        sort = "-created_date"
        search = ""
        question_id = request.query_params.get("question_id")

        if not question_id:
            return Response({"message": "Question ID is required in query parameters."}, status=400)

        if request.query_params.get("sort"):
            sort_param = request.query_params.get("sort")
            if sort_param in valid_sort_values:
                sort = sort_param
            else:
                return Response({"message": f"Invalid sort value. Valid values are {', '.join(valid_sort_values)}."}, status=400)

        if request.query_params.get("search"):
            search = request.query_params.get("search")

        answer_lst = Answer.objects.filter(
            question_ID=question_id, content__contains=search).order_by(sort)

        if answer_lst:
            srlz = AnswerSerializer(answer_lst, many=True)
            for data in srlz.data:
                links = ReferenceLink.objects.filter(
                    answer_ID=int(data["answer_ID"]))
                images = Image.objects.filter(answer_ID=int(data["answer_ID"]))
                links_srlz = ReferenceLinkSerializer(links, many=True)
                images_srlz = ImageSerializer(images, many=True)
                data["reference_links"] = links_srlz.data
                data["images"] = images_srlz.data
            return Response(srlz.data)
        else:
            return Response({"message": "No answers found for the given question."}, status=404)

    @method_decorator(jwt_auth_required)
    def put(self, request):
        answer_id = request.query_params.get("id")
        try:
            answer = Answer.objects.get(answer_ID=answer_id)
        except ObjectDoesNotExist:
            return Response({"message": "Answer not exist."}, status=404)

        request_user = requests.get(USER_API_URL + "user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)

        if user_data["id"] != answer.user:
            return Response({"message": "User does not have permission."}, status=403)

        if "content" in request.data.keys():
            answer.content = request.data["content"]
        answer.updated_date = datetime.now()
        answer.save()
        return self.get(request)

    @method_decorator(jwt_auth_required)
    def delete(self, request):
        request_user = requests.get(USER_API_URL + "user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != answer.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        answer_id = request.data.get("id")
        try:
            answer = Answer.objects.get(answer_ID=answer_id)
        except ObjectDoesNotExist:
            return Response({"message": "Answer not exist."}, status=404)

        request_user = requests.get("https://user-service-if4z3.ondigitalocean.app/user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)

        if user_data["id"] != answer.user:
            return Response({"message": "User does not have permission."}, status=403)
        answer.delete()
        return Response({"message": "Answer deleted successfully."})


class ReferenceLinkAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        try:
            answer = Answer.objects.get(answer_ID=request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Answer not exist."}, status=404)
        request_user = requests.get(USER_API_URL + "user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != answer.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        link = ReferenceLink.objects.create(
            content=request.data["content"], answer_ID=answer)
        return Response({"message": "Link added successfully."})

    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            link = ReferenceLink.objects.get(ref_ID=request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Link not exist."}, status=404)
        try:
            answer = Answer.objects.get(answer_ID=link.answer_ID)
        except ObjectDoesNotExist:
            return Response({"message": "Answer not exist."}, status=404)
        request_user = requests.get(USER_API_URL + "user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != answer.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)

        link.delete()
        return Response({"message": "Link deleted successfully."})


class ImageAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        try:
            answer = Answer.objects.get(answer_ID=request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Answer not exist."}, status=404)
        request_user = requests.get(USER_API_URL + "user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != answer.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        image_file = request.FILES["image"]
        image = Image.objects.create(answer_ID=answer)
        result = uploader.upload(
            image_file, public_id=image.img_ID, folder="UserApp", overwrite=True)
        image.content = result["url"]
        image.save()
        return Response({"message": "Image added successfully."})

    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            image = Image.objects.get(img_ID=request.data["id"])
        except ObjectDoesNotExist:
            return Response({"message": "Image not exist."}, status=404)
        try:
            answer = Answer.objects.get(answer_ID=image.answer_ID)
        except ObjectDoesNotExist:
            return Response({"message": "Answer not exist."}, status=404)
        request_user = requests.get(USER_API_URL + "user/", headers={
                                    "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        user_data = json.loads(request_user.content)
        if user_data["id"] != answer.user and user_data["isAdmin"] != True:
            return Response({"message": "User does not have permission."}, status=403)
        result = uploader.destroy(public_id="UserApp/" + str(image.img_ID))
        image.delete()
        return Response({"message": "Image deleted successfully."})
