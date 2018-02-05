from django.contrib.auth.models import User
from django.urls import resolve
import redis


class JWTAuthenticationMiddleware:
    
   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self,request, view_func, view_args, view_kwargs):

        print("inside middleware")
        current_url = resolve(request.path_info).url_name
        print(current_url)
        jwttoken=request.META.get('HTTP_TOKEN')
        print(jwttoken)
        if current_url=='userlogin' or  current_url=='userregister' or current_url=='startlogin' or current_url=='verifytoken' or current_url=='addimage' or current_url=='getimage':
            print("allowed")
            return None
        print(jwttoken)
        cache=redis.StrictRedis(host='localhost',decode_responses=True)
        username=cache.get(jwttoken)
        print(username)
        users=User.objects.all()
        user=User.objects.get(username=username)
        if user in users:
             return None
        