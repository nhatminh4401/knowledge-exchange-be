from functools import wraps
from rest_framework.response import Response
import jwt
from config.settings import SECRET_KEY

def jwt_auth_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Lấy token từ header Authorization
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        if authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            try:
                # Giải mã token bằng khóa bí mật
                secret_key = SECRET_KEY
                decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
                request.user_info = decoded_token.get('user_info')
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return Response({'detail': 'Token has expired.'}, status=401)
            except jwt.DecodeError:
                return Response({'detail': 'Invalid token.'}, status=401)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
    return wrapped_view