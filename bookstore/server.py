import uvicorn

if __name__ == "__main__":
    uvicorn.run("bookstore.asgi:application", reload=True)