from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Review
import requests
from .serializers import ReviewSerializer
from django.utils.decorators import method_decorator
from .decorators import jwt_auth_required
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from config.settings import USER_API_URL

class ReviewQuestionAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        review = Review()
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]
        request_user = requests.get(USER_API_URL + "user/", headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        xml_data = request_user.content
        user_data = json.loads(xml_data.decode("utf-8"))
        review.user = user_data["id"]

        review.question_ID = request.data["question_id"]
        review.save()

        return Response({"message": "Review added successfully."})

    def get(self, request):
        if request.query_params.get("id"):
            review_lst = Review.objects.filter(
                question_ID=request.query_params.get("id"))
        else:
            review_lst = Review.objects.all()

        if review_lst:
            srlz = ReviewSerializer(review_lst, many=True)
            return Response(srlz.data)
        else:
            return Response({"message": "Review not exist."}, status=404)

    @method_decorator(jwt_auth_required)
    def put(self, request):
        try:
            review = Review.objects.get(
                review_ID=request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Review not exist."}, status=404)
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]

        review.save()
        serializer = ReviewSerializer(review)
        return Response({"message": "Review updated successfully.", "data": serializer.data})


class ReviewAnswerAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        review = Review()
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]
        request_user = requests.get(USER_API_URL + "user/", headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        xml_data = request_user.content
        user_data = json.loads(xml_data.decode("utf-8"))
        review.user = user_data["id"]

        review.answer_ID = request.data["answer_id"]
        point = review.like + review.rating
        requests.put(USER_API_URL + "user/", headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')}, data={"point": point})
        review.save()

        return Response({"message": "Review added successfully."})

    def get(self, request):
        if request.query_params.get("id"):
            review_lst = Review.objects.filter(
                answer_ID=request.query_params.get("id"))
        else:
            review_lst = Review.objects.all()

        if review_lst:
            srlz = ReviewSerializer(review_lst, many=True)
            return Response(srlz.data)
        else:
            return Response({"message": "Review not exist."}, status=404)

    @method_decorator(jwt_auth_required)
    def put(self, request):
        try:
            review = Review.objects.get(
                answer_ID=request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Review not exist."}, status=404)
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]
        point = review.like + review.rating
        requests.put(USER_API_URL + "user/", headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')}, data={"point": point})
        review.save()
        return self.get(request)


class ReviewAPI(APIView):
    @method_decorator(jwt_auth_required)
    def delete(self, request):
        try:
            review = Review.objects.get(
                review_ID=request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Review not exist."}, status=404)
        review.delete()

        return Response({"message": "Question deleted successfully."})
