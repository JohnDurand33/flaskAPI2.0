from flask import request
from . import api
from ..models import Post, db

@api.get('/posts') #route shortcut for get request = -> 'get' instead of 'route' in decorator
def get_all_posts():
    posts = Post.query.all()
    return {
        'status': 'ok',
        'results': len(posts),
        'posts': [post.to_dict() for post in posts]
    }, 200 

@api.get('/posts/<post_id>') 
def get_a_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'results': 1,
            'post': post.to_dict()
        }, 200
    else:
        return {
            'status': 'not ok',
            'message': 'post not found'
        }, 404
    
@api.post('/posts/create') 
def create_post_api():
    try:
        if request.method == 'POST':
            data = request.json

            title = data['title']
            img_url = data['img_url']
            caption = data.get('caption', '')
            user_id = data['user_id']

            post = Post(title, caption, img_url, user_id)
            db.session.add(post)
            db.session.commit()
            return {
                'status': 'ok',
                'message': 'Post created successfully',
            }, 201
    except:
        return{
            "ststus": "not ok",
            'message':'Not enough information to complete a post'
        }, 400
    
