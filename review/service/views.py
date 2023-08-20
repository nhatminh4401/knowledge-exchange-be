from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Review
from .serializers import ReviewSerializer
from django.utils.decorators import method_decorator
from .decorators import jwt_auth_required
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class ReviewQuestionAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        review = Review()
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]
        request_user = request.get("http://127.0.0.1:8001/user/", headers={
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
                question_ID=request.query_params.get("id"))
        except ObjectDoesNotExist:
            return Response({"message": "Review not exist."}, status=404)
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]

        review.save()
        return self.get(request)


class ReviewAnswerAPI(APIView):
    @method_decorator(jwt_auth_required)
    def post(self, request):
        review = Review()
        review.like = request.data["like"]
        review.rating = request.data["rating"]
        review.report = request.data["report"]
        request_user = request.get("http://127.0.0.1:8001/user/", headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION', '')})
        xml_data = request_user.content
        user_data = json.loads(xml_data.decode("utf-8"))
        review.user = user_data["id"]

        review.answer_ID = request.data["answer_id"]
        review.save()

        return Response({"message": "Review added successfully."})

    def get(self, request):
        if request.query_params.get("id"):
            review_lst = Review.objects.filter(
                answer_ID=request.query_params.get("id"))
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

        review.save()
        return self.get(request)
