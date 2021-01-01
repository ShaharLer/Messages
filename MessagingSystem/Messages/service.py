from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import SystemUser
from threading import Lock

lock = Lock()
NAME_KEY = 'name'
USER_ID_NOT_FOUND = 'There is no user with id={0}'


def get_all_users():
    try:
        lock.acquire()
        return get_response_with_object(SystemUserSerializer(SystemUser.objects.all(), many=True).data)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def add_user(data):
    if not is_user_params_valid(data):
        return get_invalid_user_name_response()

    try:
        lock.acquire()
        user = SystemUser.objects.create(name=data[NAME_KEY])
        user.save()
        return get_response_with_object(SystemUserSerializer(user).data)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def get_user(user_id):
    try:
        lock.acquire()
        user = SystemUser.objects.get(id=user_id)
        return get_response_with_object(SystemUserSerializer(user).data)
    except SystemUser.DoesNotExist as e:
        return get_response_with_message(USER_ID_NOT_FOUND.format(user_id), status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def update_user(data, user_id):
    if not is_user_params_valid(data):
        return get_invalid_user_name_response()

    try:
        lock.acquire()
        user = SystemUser.objects.get(id=user_id)
        user.name = data[NAME_KEY]
        user.save()
        return get_response_with_object(SystemUserSerializer(user).data)
    except SystemUser.DoesNotExist as e:
        return get_response_with_message(USER_ID_NOT_FOUND.format(user_id), status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


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


def is_user_params_valid(data):
    return NAME_KEY in data and len(data[NAME_KEY]) > 0


def get_invalid_user_name_response():
    return get_response_with_message(f'User must have a non-empty name', status.HTTP_400_BAD_REQUEST)


def get_empty_user_name_response():
    class_name = SystemUser.__name__.title()
    return get_response_with_message(f'{class_name} must have a non-empty name', status.HTTP_400_BAD_REQUEST)


def get_response_with_object(body):
    return Response(body, status.HTTP_200_OK)


def get_response_with_message(message, status_code):
    return Response({"detail": message}, status_code)
