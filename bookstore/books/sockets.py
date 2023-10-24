import socketio
import json
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from books.models import Comment, Book
from books.serializers import CommentCreateSerializer
from users.models import CustomUser

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*"
)

@sio.on("connect")
async def connect(sid, env, auth):
    print('lalalla')
    print(sid)
    print(env)
    print(auth)

    # if auth:
    #     book_id = auth["book_id"]
    #     print("SocketIO connect")
    #     sio.enter_room(sid, book_id)
    #     await sio.emit("connect", f"Connected as {sid}")
    # else:
    #     raise ConnectionRefusedError("No auth")
    book_id = 3
    print("SocketIO connect")
    await sio.enter_room(sid, book_id)
    await sio.emit("connect", f"Connected as {sid}")


def store_comment(data):
    print(data)
    data = json.loads(data)
    user_id = data["user_id"]
    book_id = data["book_id"]
    body = data["body"]
    user = get_object_or_404(CustomUser, pk=user_id)
    book = get_object_or_404(Book, id=book_id)

    instance = Comment.objects.create(user=user, book=book, body=body)
    instance.save()
    comment = CommentCreateSerializer(instance).data
    comment["book"] = book_id
    comment["author"] = str(comment["author"])
    return comment


@sio.on("message")
async def print_message(sid, data):
    print("Socket ID", sid)
    comment = await sync_to_async(store_comment, thread_sensitive=True)(
        data
    )
    await sio.emit("new_message", comment, room=comment["book"])


@sio.on("disconnect")
async def disconnect(sid):
    sio.leave_room(sid)
    print("SocketIO disconnect")

