from tokenize import Comment
import socketio
# from utils import config
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from books.models import Book
from books.serializers import CommentSerializer
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
    book_id = "7ce6aa6a-208a-4c1e-8f96-ebeb8eb16996"
    print("SocketIO connect")
    await sio.enter_room(sid, book_id)
    await sio.emit("connect", f"Connected as {sid}")


# communication with orm
def store_comment(data):
    print(data)
    comment = json.loads(data)
    sender_id = comment["sender_id"]
    book_id = comment["book_id"]
    text = comment["text"]
    sender = get_object_or_404(CustomUser, pk=sender_id)
    book = get_object_or_404(Book, short_id=book_id)

    instance = Comment.objects.create(sender=sender, book=book, text=text)
    instance.save()
    comment = CommentSerializer(instance).data
    comment["book"] = book_id
    comment["sender"] = str(comment["sender"])
    return comment


@sio.on("message")
async def receive_message(sid, data):
    print("Socket ID", sid)
    comment = await sync_to_async(store_comment, thread_sensitive=True)(
        data
    )
    await sio.emit("newComment", comment, room=comment["book_id"])


@sio.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")
