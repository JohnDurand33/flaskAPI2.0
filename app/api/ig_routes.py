from flask import request, jsonify, flash, redirect
from . import api
from ..models import User, Post, db
from werkzeug.security import check_password_hash
import base64
from ..apiauthhelper import token_auth, basic_auth, token_auth_required, basic_auth_required
import stripe
import os

# like and unlike post routes: One uses a built in decorator and one of our custom decorators for contrast!


@api.get('/posts')
def get_all_posts_API():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    user = None

    if "Authorization" in request.headers:
        val = request.headers['Authorization']
        type, token = val.split()
        if type == 'Bearer':
            token = token
            user = User.query.filter_by(token=token).first()
    return {
        'status': 'ok',
        'results': len(posts),
        'posts': [post.to_dict(user) for post in posts]
    }, 200

@api.get('/posts/<post_id>')
def get_a_post_api(post_id):
    post = Post.query.get(post_id)
    user=None
    if post:
        if "Authorization" in request.headers:
            val = request.headers['Authorization']
            type, token = val.split()
            if type == 'Bearer':
                token = token
                user = User.query.filter_by(token=token).first()

        return {
            'status': 'ok',
            'post': post.to_dict(user)
            },200
    else:
        return {
            'status': 'not ok',
            'message': 'post not found'
        }, 404

@api.route('/posts/create', methods=['POST'])
@token_auth_required
def create_post_api(user):
    try:
        data = request.json
        
        title = data['title']
        img_url = data['img_url']
        caption = data.get('caption', '')
        user_id = user.id

        post = Post(title, img_url, caption, user_id)
        db.session.add(post)
        db.session.commit()
        return {
            'status': 'ok',
            'message': 'Post created successfully',
        }, 201
    
    except Exception as e:
        return {
            "status": "not ok",
            'message': 'Not enough information to complete a post',
            e: f"{e}"
        }, 400

@api.route('/posts/like/<post_id>', methods=['POST'])
def like_post_API(post_id):
    if "Authorization" in request.headers:
        val = request.headers['Authorization']
        type, token = val.split()
        if type == 'Bearer':
            token = token
            user = User.query.filter_by(token=token).first()
    post = Post.query.get(post_id)

    if post == None:
        return {
            "status": "not ok",
            "message": "Post not found"
        }, 404

    if user in post.likers:
        return {
            "status": "not ok",
            "message": "Post already liked by user"
        }, 404

    post.likers.append(user)
    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'Post liked successfully', 'liked': True}), 200

@api.route('/posts/unlike/<int:post_id>', methods=['POST'])
def unlike_post_API(post_id):
    try:
        if "Authorization" in request.headers:
            val = request.headers['Authorization']
            type, token = val.split()
            if type == 'Bearer':
                token = token
            try:
                user = User.query.filter_by(token=token).first()
            except: 
                flash('User not found')
                return jsonify({'status': 'not ok', 'message': 'User not found'}), 404
        # Use relationship to find if the post is liked by the user
        post = user.liked_posts.filter_by(id = post_id).first()

        if not post:
            print("Post not liked or not found")
            return jsonify({
                "status": "not ok",
                "message": "Post not liked or not found"
            }), 404

        if user not in post.likers:
            return jsonify({
                "status": "not ok",
                "message": "Post not liked by user"
            }), 409

        # Remove the post from the user's list of liked posts
        user.liked_posts.remove(post)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": "Post successfully unliked.",
            'liked': False
        }), 200

    except Exception as e:
        return jsonify({
            "status": "not ok",
            "message": "Error processing request",
            "details": str(e)
        }), 500

@api.route('/signup', methods=['POST'])
def sign_up_API():

    try:
        data = request.json

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not (username and email and password):  # Check if all fields are provided
            return jsonify({
                'status': 'not ok',
                'message': 'Missing username, email, or password'
            }), 400

        if User.query.filter_by(username=username).first():
            return jsonify({
                'status': 'not ok',
                'message': 'Username already exists'
            }), 400

        if User.query.filter_by(email=email).first():
            return jsonify({
                'status': 'not ok',
                'message': 'Email already registered'
            }), 400

        # Password is hashed in the init
        user = User(username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'status': 'ok',
            'message': 'User created successfully'
        }), 201

    except Exception as e:  # Catch exceptions more explicitly if possible
        return jsonify({
            'status': 'not ok',
            'message': 'An error occurred during signup',
            'details': str(e)
        }), 500

@api.route('/login', methods=['POST'])
# @basic_auth_required
@basic_auth.login_required # This is the same as the above but user is not passed in their decorator function, so we need to access it from current_user
def login_API(): #before we had the flask basic_auth.verify_password decorator, the definition of the login_API function was: def login_API(user)
    user = basic_auth.current_user()
    return jsonify({
        'status': 'ok',
        'message': 'User logged in successfully',
        'user': user.to_dict()
    }), 200

@api.route('/logout', methods=['POST'])
@token_auth_required
def logout_API(user):
        return jsonify({
            'status': 'ok',
            'message': f'{user.username} logged out successfully',
            'logged_out_user': user.to_dict()
        }), 200


######################## front end only shop backend routes ############################
# FRONTEND_URL = os.environ.get('FRONTEND_URL')
FRONTEND_URL = os.environ.get('FRONTEND_URL')
stripe.api_key = os.environ.get('STRIPE_API_KEY')

@api.route('/checkout', methods=['POST'])
def stripe_checkout():
    try:
        data = request.form
        print(f' data: {data}')
        line_items = []
        for price in data:

            line_items.append({'price': price, 'quantity': data[price]})
        print(f' line_items: {line_items}')

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=FRONTEND_URL + '?success=true',
            cancel_url=FRONTEND_URL + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
