from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix = "/posts", tags=['Posts'])

# # request Get method url: "/"
# @router.get("/")
# async def root():
#     return {"message": "Welcome to my API"}



# request Get method url: "/posts"
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 2, search: Optional[str] = ""):

    # posts= db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() (if restricted to logged user)

   # posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
     
    # cursor.execute("""select * from posts """)
    # posts = cursor.fetchall()
    # print(current_user.id) 
    # print(posts)
    return posts

#After adding pydantic model- api looks for the basemodel and validate the given data
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#path parameters id is retrieved as string by default - so dont forget to conver manually
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""select * from posts where id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post was not found with id: {id}")

    
    #if restricted to logged in user then verify the below
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the action")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post was not found with id: {id}"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #deleting the post
    #find the index in the array with the id
    #my_posts.pop(index)
    # cursor.execute(""" delete from posts where id = %s returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    #index_of_id = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post wiht id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the action")
    post_query.delete(synchronize_session = False)
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title =  %s, content = %s, published = %s where id = %s returning * """, (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post wiht id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the action")
    
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()
    
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict                                                                                                   
    return post_query.first()
