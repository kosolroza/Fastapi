from random import randrange
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel      # pydantic is a library that is used to validate the data that is sent to the server. It is used to create a model that can be used to validate the data that is sent to the server.
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema, utils
from .database import engine, get_db
from passlib.context import CryptContext
from pwdlib import PasswordHash
from .routers import post, user, auth

""" The passlib library is not working anymore, so I use the pwdlib instead of passlib """
# pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto") 
# password_hasher = PasswordHash()
# models.Base.metadata.create_all(bind = engine) # to create the tables in the database based on the models that we have defined in the models.py file. It will create the tables if they do not exist, if they exist then it will not do anything.


"""
    - This is the main file that contains the code for the backend of the application. 
    - It is used to create the API endpoints and connect to the database. 
    - It also contains the code for the CRUD operations.
"""

app = FastAPI()

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

# Create a post for testing the database connection
my_post = [{"title" : "Test title", "content" : "Test content", "published" : True},
           {"title" : "Test title 2", "content" : "Test content 2", "published" : False},
           {"title" : "Test title 3", "content" : "Test content 3", "published" : True}]

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
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# class Post(BaseModel):      # This class is needed to has in the first one 
#     title : str
#     content : str
#     published : bool = True
#     # rating : Optional[int] = None



# # @app.get("/sqlalchemy")
# # def test_post(db : Session = Depends(get_db)):
# #     posts = db.query(models.Post).all()     # this is the same as SELECT * FROM posts, it will return all the posts from the database and store it in the posts variable
# #     return {"data" : posts}


# # get method to test the connection to the database
# @app.get("/posts", response_model = List[schema.Post])
# def get_posts(db : Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts """)
#     # post = cursor.fetchall()        # to get all the data from the database and store it in the post variable
#     # print(post)
#     posts = db.query(models.Post).all() 
#     return posts

# # Create a post
# @app.post("/posts", status_code= status.HTTP_201_CREATED, response_model = schema.Post) # to return the post that is created in the database, it is like SELECT * FROM posts WHERE id = new_post.id
# def create_posts(post : schema.PostCreate, db : Session = Depends(get_db)):
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#     #                 (post.title, post.content, post.published))
#     # post = cursor.fetchone()
#     # conn.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
#     # new_post = models.Post(title = post.title, content = post.content, published = post.published)

#     new_post = models.Post(**post.dict()) # this is the same as the above code, it will create a new post based on the data that is sent to the server and store it in the new_post variable    
    
#     db.add(new_post) # to add the new post to the database, it is like INSERT INTO posts (title, content, published) VALUES (post.title, post.content, post.published)
#     db.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
#     db.refresh(new_post)    # to get the new post from the database and store it in the new_post variable, it is like SELECT * FROM posts WHERE id = new_post.id
#     return new_post

        
# # more cleaner than the above code
# @app.get("/posts/{id}", response_model = schema.Post) # to return the post that is created in the database, it is like SELECT * FROM posts WHERE id = id
# def get_post(id : int, response : Response, db : Session = Depends(get_db)):     # validated the id to be an integer
#     # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # to get the post with the specific id from the database and store it in the test_post variable
#     # post = cursor.fetchone()
#     # print(test_post)
#     # post = find_post(id)
#     post = db.query(models.Post).filter(models.Post.id == id).first() # to get the post with the specific id from the database and store it in the post variable, it is like SELECT * FROM posts WHERE id = id

#     if not post: 
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id {id} not found")
#     # print(post)
#     return post

# # delete a post 
# @app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id : int, db : Session = Depends(get_db)):
#     # define the index in the array that has the ID
#     # my_post.pop(index)
#     # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
#     # deleted_post = cursor.fetchone()
#     # conn.commit() # to save the changes to the database, if we don't use this then the changes will not be saved to the database
#     # When the ID is not found and we use 404 as the atatus code, if not then it see the 500 the server is error
#     deleted_post = db.query(models.Post).filter(models.Post.id == id).first() # to get the post with the specific id from the database and store it in the deleted_post variable, it is like SELECT * FROM posts WHERE id = id

#     if deleted_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail = f"Post {id} does not exist")
#     # return {"message": "Post has been deleted"}
#     db.delete(deleted_post) # to delete the post from the database, it is like DELETE FROM posts WHERE id = id
#     db.commit()
#     return Response(status_code= status.HTTP_204_NO_CONTENT)


# # update a post
# @app.put("/posts/{id}", response_model = schema.Post)
# def update_post(id: int, updated_post : schema.PostCreate, db : Session = Depends(get_db)):
#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#     #                 (post.title, post.content, post.published, str(id)))
#     # conn.commit()
#     # updated_post = cursor.fetchone()
#     post_query = db.query(models.Post).filter(models.Post.id == id) 
#     post = post_query.first() # to get the first post from the database and store it in the post variable, it is like SELECT * FROM posts WHERE id = id LIMIT 1
    
#     if post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail = f"post with {id} does not exist")
#     # this just the update that we update in the code not in postman
#     # updated_post.update({'title' : 'hey this is my update title', 'content' : 'This is my update content'}, 
#     #                     synchronize_session = False)
#     post_query.update(updated_post.dict(), synchronize_session = False) # to update the post in the database, it is like UPDATE posts SET title = post.title, content = post.content, published = post.published WHERE id = id
#     db.commit()
#     db.refresh(post)

#     return post

# @app.post("/users", status_code= status.HTTP_201_CREATED, response_model = schema.UserOut)
# def create_user(users : schema.UserCreate, db : Session = Depends(get_db)):

#     # hash the password - user.password
#     # bcrypt has a 72-byte limit, so truncate if necessary
#     hash_password = utils.hash(users.password)
#     users.password = hash_password

#     new_user = models.User(**users.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/users/{id}", response_model = schema.UserOut)
# def get_user(id : int, db : Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail = f"user with id {id} not found")
#     return user