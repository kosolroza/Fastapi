"""
This is the Basic code of use of fastapi with postgreSQL database, and the code of CRUD operations on the database.
It is need to connect with database file and models file to work
"""


# from random import randrange
# from typing import Optional
# from fastapi import Body, FastAPI, Response, status, HTTPException
# from pydantic import BaseModel      # pydantic is a library that is used to validate the data that is sent to the server. It is used to create a model that can be used to validate the data that is sent to the server.
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


# app = FastAPI()

# class Post(BaseModel):      # This class is needed to has in the first one 
#     title : str
#     content : str
#     published : bool = True
#     # rating : Optional[int] = None

# # Connect the database into fastapi
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
#                                 password = 'Roza231105', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print(f"Database connection was successfully")
#         break
#     except Exception as error:
#         print("Connecting to database is fail")
#         print("Error: ", error)
#         time.sleep(2)

# # Create a post for testing the database connection
# my_post = [{"title" : "Test title", "content" : "Test content", "published" : True},
#            {"title" : "Test title 2", "content" : "Test content 2", "published" : False},
#            {"title" : "Test title 3", "content" : "Test content 3", "published" : True}]

# # get method to test the connection to the database
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     post = cursor.fetchall()        # to get all the data from the database and store it in the post variable
#     # print(post)
#     return {"data" : post}

# # Create a post
# @app.post("/posts")
# def create_posts(post : Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                     (post.title, post.content, post.published))
#     post = cursor.fetchone()
#     conn.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
#     return {"data": post}

# # more cleaner than the above code
# @app.get("/posts/{id}")
# def get_post(id : str, response : Response):     # validated the id to be an integer
#     cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # to get the post with the specific id from the database and store it in the test_post variable
#     post = cursor.fetchone()
#     # print(test_post)
#     # post = find_post(id)
#     if not post: 
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id {id} not found")
#     # print(post)
#     return {"post_detail" : post}

# # 




from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel      # pydantic is a library that is used to validate the data that is sent to the server. It is used to create a model that can be used to validate the data that is sent to the server.
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

# @app.get("/")       # get is to request to information
# async def root():       # async is the synatic that can be match the database and the other 
#     return {"message": "Hello Backend Devloper ><"}

# @app.get("/posts")
# def get_posts():
#     return {"data": "This is your posts"}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):        #extract the information from the body of the request and store it in the payload variable
#     print(payload)
#     return {"new post": f"title: {payload['title']}, content: {payload['content']}"}


# ===== using pydantic to validate the data that is sent to the server =====
# class Post(BaseModel):
#     title: str
#     content : str
#     published : bool = True      # default value is true
#     rating : Optional[int] = None # optional means that the rating can be null or not provided, and the default value is None

# @app.post("/createposts")
# def create_posts(post : Post):
#     # print(new_post.rating)
#     print(post.dict())
#     return {"data" : "new post created"}


# ===== CRUD operations =====
# Create - POST
class Post(BaseModel):      # This class is needed to has in the first one 
    title : str
    content : str
    published : bool = True
    # rating : Optional[int] = None

# Connect the database into fastapi
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
                                password = 'Roza231105', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print(f"Database connection was successfully")
        break
    except Exception as error:
        print("Connecting to database is fail")
        print("Error: ", error)
        time.sleep(2)



# Create some post to test
my_post = [{"title": "title of post 1", "content": "Content of post 1", "id" : 1}, 
           {"title" : "favorite food", "content" : "I love pizza", "id" : 2}]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
    return None

# get all post : to 
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    post = cursor.fetchall()        # to get all the data from the database and store it in the post variable
    # print(post)
    return {"data" : post}

# Create a post
# @app.post("/posts")
# def create_posts(post : Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 100000000)
#     my_post.append(post_dict)
#     return {"data": post_dict}


# ================================================================
# How to create a code with the right status code
@app.post("/posts", status_code= status.HTTP_201_CREATED)
# create a post with the database
def create_posts(post : Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                    (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
    return {"data": post}

# create a post without the database
# def create_posts(post : Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 100000000)
#     my_post.append(post_dict)
#     return {"data": post_dict}

# get one post
# @app.get("/posts/{id}")
# def get_post(id : int):     # validated the id to be an integer
#     post = find_post(id)
#     print(post)
#     return {"post_detail" : post}

# get post with response
# @app.get("/posts/{id}")
# def get_post(id : int, response : Response):     # validated the id to be an integer
#     post = find_post(id)
#     if not post: 
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message" : f"post with id {id} not found"}
#     print(post)
#     return {"post_detail" : post}

# more cleaner than the above code
@app.get("/posts/{id}")
def get_post(id : str, response : Response):     # validated the id to be an integer
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # to get the post with the specific id from the database and store it in the test_post variable
    post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} not found")
    # print(post)
    return {"post_detail" : post}

# ================================================================
# define the post in the list
def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
        return None
        
# define the index in the array that has the ID -> This in needed in define the delete
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
        
# delete a post 
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    # define the index in the array that has the ID
    # my_post.pop(index)
    index = find_index_post(id)

    # When the ID is not found and we use 404 as the atatus code, if not then it see the 500 the server is error
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post {id} does not exist")
    my_post.pop(index)
    # return {"message": "Post has been deleted"}
    return Response(status_code= status.HTTP_204_NO_CONTENT)

# ================================================================
# update post 
@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"post with {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data" : post_dict}






"""
This is the code of connetion of postgreSQL database with fastapi, and the code of CRUD operations on the database.
It is need to connect with database file and models file to work
"""

# from random import randrange
# from typing import Optional
# from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
# from pydantic import BaseModel      # pydantic is a library that is used to validate the data that is sent to the server. It is used to create a model that can be used to validate the data that is sent to the server.
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
# from . import models
# from .database import engine, get_db


# models.Base.metadata.create_all(bind = engine) # to create the tables in the database based on the models that we have defined in the models.py file. It will create the tables if they do not exist, if they exist then it will not do anything.

"""
    - This is the main file that contains the code for the backend of the application. 
    - It is used to create the API endpoints and connect to the database. 
    - It also contains the code for the CRUD operations.
"""

# app = FastAPI()

# # define the post in the list
# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p
#         return None
        
# # define the index in the array that has the ID -> This in needed in define the delete
# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i
        


# class Post(BaseModel):      # This class is needed to has in the first one 
#     title : str
#     content : str
#     published : bool = True
#     # rating : Optional[int] = None

# # Connect the database into fastapi
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
#                                 password = 'Roza231105', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print(f"Database connection was successfully")
#         break
#     except Exception as error:
#         print("Connecting to database is fail")
#         print("Error: ", error)
#         time.sleep(2)

# # Create a post for testing the database connection
# my_post = [{"title" : "Test title", "content" : "Test content", "published" : True},
#            {"title" : "Test title 2", "content" : "Test content 2", "published" : False},
#            {"title" : "Test title 3", "content" : "Test content 3", "published" : True}]

# # get method to test the connection to the database
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     post = cursor.fetchall()        # to get all the data from the database and store it in the post variable
#     # print(post)
#     return {"data" : post}

# # Create a post
# @app.post("/posts")
# def create_posts(post : Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                     (post.title, post.content, post.published))
#     post = cursor.fetchone()
#     conn.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
#     return {"data": post}

        
# # more cleaner than the above code
# @app.get("/posts/{id}")
# def get_post(id : str, response : Response):     # validated the id to be an integer
#     cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # to get the post with the specific id from the database and store it in the test_post variable
#     post = cursor.fetchone()
#     # print(test_post)
#     # post = find_post(id)
#     if not post: 
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id {id} not found")
#     # print(post)
#     return {"post_detail" : post}

# # delete a post 
# @app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id : int):
#     # define the index in the array that has the ID
#     # my_post.pop(index)
#     cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
#     # When the ID is not found and we use 404 as the atatus code, if not then it see the 500 the server is error
#     if deleted_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail = f"Post {id} does not exist")
#     # return {"message": "Post has been deleted"}
#     return Response(status_code= status.HTTP_204_NO_CONTENT)


# # update a post
# @app.put("/posts/{id}")
# def update_post(id: int, post : Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                     (post.title, post.content, post.published, str(id)))
#     conn.commit()
#     updated_post = cursor.fetchone()

#     if updated_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail = f"post with {id} does not exist")

#     return {"data" : updated_post}



# ========================================== ORM ==========================================
""" 
    - ORM is Object Relational Mapping.
    - It is a technique that is used to convert the data from the database into an object that can be used in the code.
    - It is used to create a model that can be used to validate the data that is sent to the server.
    - It is used to create a model that can be used to interact with the database.
    - It is used to create a model that can be used to perform CRUD operations on the database.
"""

"""
This is the code of connection of PostgreSQL database with fastapi using ORM, and the code of CRUD operations on the database.
"""

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True


app.get("/posts")
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data" : posts}

app.post("/posts")
def create_posts(post : Post, db : Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post_by_id(id : str, response : Response, 
                   db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} not found")
    return {"data" : post}

