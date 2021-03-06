import random

from django.db import transaction

from accounts.models import User, create_profile
from api import sms, log
from accounts import models
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    # serializer.save()
    manager = models.UserManager()
    password = random.randint(1000, 9999)
    print(password)
    phone = request.POST['phone']
    user = User.objects.filter(phone=phone).first()
    if user:
        try:
            profile = user.profile
        except Exception:
            profile = create_profile(user=user)
        user.set_password(password)
        user.save()
    else:
        with transaction.atomic():
            try:
                user = manager.create_user(phone, password)
                profile = create_profile(user=user)
            except Exception:
                log.error("could not create user", request.user)

    # sms_send.send_sms(phone, password)
    sms.verify(phone, password)

    return Response({'success': 'success'},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    phone = request.data.get("phone")
    password = request.data.get("password")
    if phone is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=phone, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    user.set_unusable_password()
    user.save()
    return Response({'token': token.key},
                    status=HTTP_200_OK)


# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def sign(request):
#     user_manager = UserManager()
#     user_manager.create_staffuser(request.GET['phone'], request.GET['password'])
#     return Response({'success': 'success'},
#                     status=HTTP_200_OK)
