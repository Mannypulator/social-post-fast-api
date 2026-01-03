import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from sqlalchemy import select
from app.schemas import CreatePost, CreateUser, GetUser, UpdateUser
from app.db import Post, User, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.images import imagekit
import shutil
import os
import tempfile
import aiofiles
import aiofiles.tempfile
from app.users import auth_backend, current_active_user,fastapi_users 


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(GetUser, CreateUser), prefix='/auth', tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix='/auth', tags=["auth"])
app.include_router(fastapi_users.get_verify_router(GetUser), prefix='/auth', tags=["auth"])
app.include_router(fastapi_users.get_users_router(GetUser, UpdateUser), prefix='/users', tags=["users"])


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    temp_file_path = None
    
    try:
        # Create a temporary file to store the upload
        async with aiofiles.tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            await temp_file.write(content)
        
        # Upload to ImageKit
        async with aiofiles.open(temp_file_path, 'rb') as f:
            file_content = await f.read()
            upload_result = imagekit.files.upload(
                file=file_content,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["upload"],
                folder="/uploads/"
            )
        
        # Determine file type based on content type
        file_type = "image"
        if file.content_type:
            if file.content_type.startswith("video/"):
                file_type = "video"
            elif file.content_type.startswith("image/"):
                file_type = "image"
        
        # Create post with ImageKit data
        post = Post(
            user_id= user.id,
            caption=caption,
            url=upload_result.url,
            file_type=file_type,
            file_name=upload_result.name
        )
        
        session.add(post)
        await session.commit()
        await session.refresh(post)
        
        return {
            "id": str(post.id),
            "user_id": str(post.user_id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat() if post.created_at else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()  


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    
    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    
    user_dict = {u.id: u.email for u in users}
    
    posts_data = []
    
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at,
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )
    
    return {"posts": posts_data}


@app.delete("/posts/{post_id}")
async def delete_post(post_id:str, session:AsyncSession = Depends(get_async_session),user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id)
        
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if(user.id != post.user_id):
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")
        await session.delete(post)
        await session.commit()
        
        return {"success": True, "message":"Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    