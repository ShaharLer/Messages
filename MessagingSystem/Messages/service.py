from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import SystemUser, Message
from django.db.models import Q
from threading import Lock

lock = Lock()
NAME_KEY = 'name'
SENDER_KEY = 'sender'
RECEIVER_KEY = 'receiver'
SUBJECT_KEY = 'subject'
MESSAGE_KEY = 'message'
USER_KEY = 'user'
USER_NOT_FOUND = 'There is no user with id={0}'
MESSAGE_NOT_FOUND = 'There is no message with id={0}'


class UserNotFoundException(Exception):
    pass


class MessageNotFoundException(Exception):
    pass


def get_objects(func):
    try:
        lock.acquire()
        return func()
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def add_object(add_func, validate_func, data):
    response = validate_func(data)
    if response:
        return response

    try:
        lock.acquire()
        return add_func(data)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def get_specific_objects(func, obj_id):
    try:
        lock.acquire()
        return func(obj_id)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def get_all_users():
    all_users = SystemUser.objects.all()
    return get_response_with_object(SystemUserSerializer(all_users, many=True).data)


def add_user(data):
    user = SystemUser.objects.create(name=data[NAME_KEY])
    user.save()
    return get_response_with_object(SystemUserSerializer(user).data)


def get_user(user_id):
    user = get_user_object(user_id)
    return get_response_with_object(SystemUserSerializer(user).data)


def update_user(data, user_id):
    response = validate_user_params(data)
    if response:
        return response

    try:
        lock.acquire()
        user = get_user_object(user_id)
        user.name = data[NAME_KEY]
        user.save()
        return get_response_with_object(SystemUserSerializer(user).data)
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def add_message(data):
    message = Message.objects.create(sender=get_user_object(data[SENDER_KEY]),
                                     receiver=get_user_object(data[RECEIVER_KEY]),
                                     subject=data[SUBJECT_KEY],
                                     message=data[MESSAGE_KEY])
    message.save()
    return get_response_with_object(MessageSerializer(message).data)


def get_all_messages():
    all_messages = Message.objects.all()
    return get_response_with_object(MessageSerializer(all_messages, many=True).data)


def get_message(message_id):
    message = get_message_object(message_id)
    return get_response_with_object(MessageSerializer(message).data)


def delete_message(data, message_id):
    response = validate_delete_message_params(data)
    if response:
        return response

    try:
        lock.acquire()
        message = get_message_object(message_id)
        user = get_user_object(data[USER_KEY])
        if user != message.sender and user != message.receiver:
            response = get_response_with_message('Only the sender or the receiver of the message can delete it',
                                                 status.HTTP_400_BAD_REQUEST)
        else:
            response = get_response_with_object(MessageSerializer(message).data)
            message.delete()
        return response
    except Exception as e:
        return get_response_with_message(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        lock.release()


def get_all_user_messages(user_id):
    return get_user_messages(user_id, only_unread_messages=False)


def get_all_user_unread_messages(user_id):
    return get_user_messages(user_id, only_unread_messages=True)


def get_user_messages(user_id, only_unread_messages):
    user = get_user_object(user_id)
    if only_unread_messages:
        user_messages = Message.objects.filter(Q(receiver=user) & Q(is_read=False))
    else:
        user_messages = Message.objects.filter(receiver=user)
    return get_response_with_object(MessageSerializer(user_messages, many=True).data)


def read_user_message(message_id):
    message = get_message_object(message_id)
    message.is_read = True
    message.save()
    return get_response_with_object(MessageSerializer(message).data)


def get_user_object(user_id):
    try:
        return SystemUser.objects.get(id=user_id)
    except SystemUser.DoesNotExist:
        raise UserNotFoundException(USER_NOT_FOUND.format(user_id))


def get_message_object(message_id):
    try:
        return Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        raise MessageNotFoundException(MESSAGE_NOT_FOUND.format(message_id))


def validate_user_params(data):
    if NAME_KEY not in data or len(data[NAME_KEY]) == 0:
        return get_response_with_message(f'User must have a non-empty name', status.HTTP_400_BAD_REQUEST)

    if data[NAME_KEY].isnumeric():
        return get_response_with_message(f'The name of the user cannot be a number', status.HTTP_400_BAD_REQUEST)

    return None


def validate_add_message_params(data):
    if SENDER_KEY not in data or len(data[SENDER_KEY]) == 0:
        return get_response_with_message(f'Message request must have a non-empty sender id', status.HTTP_400_BAD_REQUEST)

    if RECEIVER_KEY not in data or len(data[RECEIVER_KEY]) == 0:
        return get_response_with_message(f'Message request must have a non-empty receiver id', status.HTTP_400_BAD_REQUEST)

    if SUBJECT_KEY not in data or len(data[SUBJECT_KEY]) == 0:
        return get_response_with_message(f'Message request must have a non-empty subject', status.HTTP_400_BAD_REQUEST)

    if MESSAGE_KEY not in data or len(data[MESSAGE_KEY]) == 0:
        return get_response_with_message(f'Message request must have a non-empty message', status.HTTP_400_BAD_REQUEST)

    return None


def validate_delete_message_params(data):
    if USER_KEY not in data or len(data[USER_KEY]) == 0:
        return get_response_with_message(f'Delete message request must have a non-empty user parameter', status.HTTP_400_BAD_REQUEST)


def get_response_with_object(body):
    return Response(body, status.HTTP_200_OK)


def get_response_with_message(message, status_code):
    return Response({"detail": message}, status_code)

