from rest_framework import viewsets
from rest_framework.decorators import api_view
from .service import *
from .serializers import SystemUserSerializer
from .models import SystemUser


class SystemUsersViewSet(viewsets.ModelViewSet):
    serializer_class = SystemUserSerializer
    queryset = SystemUser.objects.all()


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        return get_all_users()
    else:  # 'POST'
        return add_user(request)


@api_view(['GET', 'PUT']) # consider add DELETE
def specific_user(request):
    if request.method == 'GET':
        return get_user(request)
    else:  # 'PUT'
        return update_user(request)


@api_view(['POST'])
def messages(request):
    return add_message(request)


@api_view(['GET', 'DELETE'])
def specific_message(request, message_id):
    if request.method == 'GET':
        return get_message(message_id)
    else:  # 'DELETE'
        return delete_message(request, message_id)


@api_view(['GET'])
def all_user_messages(request, user_id):
    return get_all_user_messages(user_id)


@api_view(['GET'])
def all_user_unread_messages(request, user_id):
    return get_all_user_unread_messages(user_id)


@api_view(['GET'])
def read_messages(request, message_id):
    return read_message(message_id)

