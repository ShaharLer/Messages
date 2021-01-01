from rest_framework.response import Response
from rest_framework import status
from .models import SystemUser
from rest_framework.decorators import api_view
from threading import Lock

lock = Lock()


def get_all_users():
    pass


def add_user(request):
    pass


def get_user(request):
    pass


def update_user(request):
    pass


def add_message(request):
    # Response("all good", status=status.HTTP_200_OK)
    pass


def get_message(message_id):
    pass


def delete_message(request, message_id):
    pass


def get_all_user_messages(user_id):
    # user = SystemUser.objects.filter(id=user_id)
    # if user is None:
    #     return Response({"Did not find user"}, status.HTTP_400_BAD_REQUEST)
    # return Response(UserMessagesSerializer(all_messages).data, status.HTTP_200_OK)
    pass


def get_all_user_unread_messages(user_id):
    pass


def read_message(message_id):
    pass
