from flask import request, jsonify, g
from . import api
from ..models import User, Post, db
from werkzeug.security import check_password_hash
import base64
from ..apiauthhelper import token_auth_required


@api.get('/posts')
def get_all_posts_API():
    
    posts = Post.query.order_by(Post.date_created.desc()).all()

    if posts:
        return {
            'status': 'ok',
            'results': len(posts),
            'posts': [post.to_dict() for post in posts]
        }, 200
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
@token_auth_required
def like_post_API(post_id, user):
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
    return jsonify({'status': 'ok', 'message': 'Post liked successfully'}), 200


@api.route('/posts/unlike/<int:post_id>', methods=['POST'])
@token_auth_required
def unlike_post_API(post_id, user):
    try:
        # Use relationship to find if the post is liked by the user
        post = user.liked_posts.filter(Post.id == post_id).first()

        if not post:
            return jsonify({
                "status": "not ok",
                "message": "Post not found"
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
            "message": f"Post '{post.title}' successfully unliked."
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
def login_API():
    try:
        val = request.headers['Authorization']
        encoded_version = val.split()[1]

        x = base64.b64decode(
        encoded_version.encode('ascii')).decode('ascii')
        username, password = x.split(':')

        if not username:

            return {
                'status': 'not ok',
                'message': 'No Authorization header provided'
            }, 401

        else:

            user = User.query.filter_by(username=username).first()

            if not user:
                return jsonify({
                    'status': 'not ok',
                    'message': 'User / password combination not found - 1'
                }), 400

            if not check_password_hash(user.password, password):
                return jsonify({
                    'status': 'not ok',
                    'message': 'User / password combination not found - 2',
                }), 400

            else:
                return jsonify({
                    'status': 'ok',
                    'message': 'User logged in successfully',
                    # wrapping key in quotes will only pass user.to_dict() AS A string, ONLY = don't wrap in quotes
                    'user': user.to_dict(),
                }), 200

                # Return user info as needed, in reality you want to create expiration system(flask token package!)
    except:
        return jsonify({
            'status': 'not ok',
            'message': 'User / password combination not found',
        }), 400


@api.route('/logout', methods=['POST'])
@token_auth_required
def logout_API(user):
        return jsonify({
            'status': 'ok',
            'message': 'User logged out successfully',
            'logged_out_user': user.to_dict()
        }), 200
