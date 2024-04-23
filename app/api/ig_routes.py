from flask import request, jsonify
from . import api
from ..models import User, Post, db
from werkzeug.security import check_password_hash
import base64
from ..apiauthhelper import token_auth_required


@api.get('/posts')
def get_all_posts_API():
    # .desc() orders the posts by date created in descending order
    posts = Post.query.order_by(Post.date_created.desc()).all()

    if posts:
        return jsonify({
            'status': 'ok',
            'results': len(posts),
            'posts': [post.to_dict() for post in posts]
        }), 200
    else:
        return jsonify({"status": "not ok", "message": "No posts found"}), 404


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


@api.route('/posts/create', methods=['POST'])
@token_auth_required
def create_post_api(user):
    print('create post api beginning')
    try:
        print('try block beginning')
        data = request.json
        print(f'initial fetch executed: data: {data}')
        title = data['title']
        img_url = data['img_url']
        caption = data.get('caption', '')
        user_id = user.id

        post = Post(title, img_url, caption, user_id)
        print(f'post query executed successfully, post: {post}')
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
@token_auth_required
def like_post_API(post_id, user):
    try:
        post_to_like = Post.query.get(post_id)
        # post = Post.query.filter_by(id=post_id).first()   ###### OR ########

        if not post_to_like:
            return jsonify({
                "status": "not ok",
                "message": "Post not found"
            }), 404

        if post_to_like in user.liked_posts:
            return jsonify({
            "status": "not ok",
            "message": "Post already liked"
        }), 404

        user.liked_posts.append(post_to_like)
        print(f'Post | {post_to_like.title} now liked by user | {user.username}')
        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": "Post liked successfully"
        })

    except Exception as e:
        return jsonify({
            "status": "not ok",
            "message": "Post not found",
            "details": f"{e}"
        }), 404


@api.route('/posts/unlike/<post_id>', methods=['POST'])
@token_auth_required
def unlike_post_API(post_id, user):

    try:
        current_user = User.query.filter_by(user.id).first()
        post = current_user.liked_posts.filter_by(post_id).first()

        if post:
            current_user.liked_posts.remove(post)
            print(f'Post | {post.title} now unliked by current user |{
                current_user.username}')
            db.session.commit()

            return jsonify({
                "status": "ok",
                "message": "Post unliked successfully!"
            })

        else:
            return {
                "status": "not ok",
                "message": "Post not found"
            }, 404
    except Exception as e:
        return jsonify({
            "status": "not ok",
            "message": "Post not found",
            "details": f"{e}"
        }), 404


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
def login_API():
    try:
        if "Authorization" in request.headers:
            val = request.headers['Authorization']
            encoded_version = val.split()[1]

            x = base64.b64decode(
                encoded_version.encode('ascii')).decode('ascii')
            username, password = x.split(':')
            print(username)

        else:
            return {
                'status': 'not ok',
                'message': 'No Authorization header provided'
            }, 401

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({
                'status': 'not ok',
                'message': 'No User'
            }), 400

        if check_password_hash(user.password, password):
            return jsonify({
                'status': 'ok',
                'message': 'User logged in successfully',
                # wrapping this in quotes will pass this string as the only user attribute
                'user': user.to_dict(),
            }), 200
        # Return user info as needed, in reality you want to create expiration system(flask token package!)
    except:
        return jsonify({
            'status': 'not ok',
            'message': 'User / password combination not found',
        }), 400
