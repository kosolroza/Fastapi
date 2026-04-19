from .. import models, schema, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags= ['Posts']
)

# get method to test the connection to the database
@router.get("/", response_model = List[schema.Post])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all() 
    return posts

# Create a post
@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schema.Post) 
def create_posts(post : schema.PostCreate, db : Session = Depends(get_db)):

    new_post = models.Post(**post.dict()) 
    
    db.add(new_post) 
    db.commit() 
    db.refresh(new_post)    
    return new_post

        
# more cleaner than the above code
@router.get("/{id}", response_model = schema.Post) 
def get_post(id : int, response : Response, db : Session = Depends(get_db)):     
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} not found")
    return post

# delete a post 
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first() 

    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post {id} does not exist")
    
    db.delete(deleted_post) 
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


# update a post
@router.put("/{id}", response_model = schema.Post)
def update_post(id: int, updated_post : schema.PostCreate, db : Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first() 
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"post with {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session = False) 
    db.commit()
    return post
