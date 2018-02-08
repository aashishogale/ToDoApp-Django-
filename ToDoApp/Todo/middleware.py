from django.contrib.auth.models import User
from django.urls import resolve
import redis


class JWTAuthenticationMiddleware:
    
   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # print("inside middleware")
        current_url = resolve(request.path_info).url_name
        # print(current_url)
        jwttoken=request.META.get('HTTP_TOKEN')
        # print("hello")
        # print(jwttoken)
        if current_url=='userlogin' or current_url==None or  current_url=='userregister' or current_url=='startlogin' or current_url=='verifytoken' or current_url=='addimage' or current_url=='getimage' or current_url=='generateOTP' or current_url=='checkOTP' or current_url=='changepassword':
            print("allowed")
            return None
        # print(jwttoken)
        cache=redis.StrictRedis(host='localhost',decode_responses=True)
        username=cache.get(jwttoken)
        # print(username)
        users=User.objects.all()
        user=User.objects.get(username=username)
        print("request.user.", request.user)
        if user in users:
            request.auth = user.id
            # request.update({"user_id": user.id })
            print('user id  ' , user.id)
            return None
        