from datetime import datetime
from bson.objectid import ObjectId

def create_blog(db, title, content, author):
    blog = {
        "title": title,
        "content": content,
        "author": author,
        "created_at": datetime.utcnow()
    }
    result = db.blogs.insert_one(blog)
    blog["_id"] = result.inserted_id
    return blog

def get_all_blogs(db):
    return list(db.blogs.find())

def get_blog_by_id(db, blog_id):
    return db.blogs.find_one({"_id": ObjectId(blog_id)})

def update_blog(db, blog_id, title, content):
    db.blogs.update_one(
        {"_id": ObjectId(blog_id)},
        {"$set": {"title": title, "content": content}}
    )
    return get_blog_by_id(db, blog_id)

def delete_blog(db, blog_id):
    return db.blogs.delete_one({"_id": ObjectId(blog_id)})
