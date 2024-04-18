from flask import request, jsonify
from . import api
from ..models import User, Post, db
from flask import Flask


@api.get('/posts') #route shortcut for get request = -> 'get' instead of 'route' in decorator
# @token_required
def get_all_posts():
    posts = Post.query.order_by(Post.date_created.desc()).all() #.desc() orders the posts by date created in descending order
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
            "status": "not ok",
            'message':'Not enough information to complete a post'
        }, 400
    

@api.post('/posts/like/<post_id>')
# @login_required
def like_post_API(post_id):
    post = Post.query.get(post_id)
    data = request.json
    user_id = data['user_id']
    current_user = User.query.get(user_id)
    if post:
        if post not in current_user.liked_post2:
            current_user.liked_post2.append(post)
            db.session.commit()

            return jsonify({
                "status": "ok",
                "message": "Post liked successfully"
            })
        
        else:
            return {
                "status": "not ok",
                "message": "Post not found"
            }, 404


@api.post('/posts/unlike/<post_id>')
# @login_required
def unlike_post_API(post_id):
    data = request.json
    user_id = data['user_id']
    current_user = User.query.get(user_id)
    post = current_user.liked_post2.filter_by(id=post_id).first()

    if post:
        current_user.liked_post2.remove(post)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "message":"Post unliked successfully!"
        })
    
    else:
        return {
            "status": "not ok",
            "message": "Post not found"
        }, 404

api.route('/signup', methods=['POST', 'OPTIONS'])
def sign_up_API():
    try:
        if request.method == 'POST' or request.method == 'OPTIONS':
            data = request.json

            username = data['username']
            email = data['email']
            password = data['password']

            user = User.query.filter_by(username=username).first()
            if user:
                return {
                    'status': 'not ok',
                    'message': 'User already exists'
                }, 400

            user = User.query.filter_by(email=email).first()
            if user:
                return {
                    'status': 'not ok',
                    'message': 'User already exists'
                }, 400

            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            return {
                'status': 'ok',
                'message': 'Post created successfully',
            }, 201
    except:
        return {
            "status": "not ok",
            'message': 'User already Exists'
        }, 400
