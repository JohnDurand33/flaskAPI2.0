from flask import render_template , request, redirect, url_for, abort
from .forms import PostForm
from ..models import User, Post, db
from flask_login import login_required, current_user
from datetime import datetime, timezone
from . import ig

@ig.route('/')
@ig.route('/posts')
def homepage():

    posts = Post.query.all()
    if posts:
        return render_template('index.html', posts=posts)
    else:
        return render_template('index.html')

@ig.route('/posts/<post_id>')
def single_post_page(post_id):
    # post = Post.query.filter_by(id=post_id).first() 
    post = Post.query.get(post_id)  # this and above line are identicle.  .get should be used for PRIMARY KEYS ONLY

    if post == None:
        abort(404)
    if post:
        return render_template('singlepost.html', post=post, like_count=len(post.likers2))
    else:
        return redirect(url_for('ig.homepage'))

@ig.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post_page():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():

            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            my_post = Post(title, caption, img_url, user_id=current_user.id)

            db.session.add(my_post)
            db.session.commit()

            return redirect(url_for('ig.homepage'))

    return render_template('createpost.html', form=form, user_id=current_user.id)

@ig.route('/posts/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update_post_page(post_id):
    post = Post.query.get(post_id) #OR Post.query.filter_by(post_id=post_id).first()
    if current_user.id != post.user_id:
        return redirect(url_for('ig.homepage'))
    form=PostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            post.title = title
            post.caption = caption
            post.img_url = img_url

            db.session.commit()
            return redirect(url_for('ig.single_post_page', post_id=post.id))

    return render_template('updatepost.html', post=post, form=form)

@ig.route('/posts/delete/<post_id>', methods=['GET', 'POST'])  
@login_required
def delete_post(post_id):

    post = Post.query.get(post_id) #OR Post.query.filter_by(post_id=post_id).first()
    if current_user.id != post.user_id:
        return redirect(url_for('ig.homepage'))
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('ig.homepage'))

#######  Below were ok for Flask only, but were modifed and moved to api folder for React-Friendly versioning ############

# @ig.route('/posts/like/<post_id>')  ******DEPRECATED for React friendly version moved to api routes file*********
# @login_required
# def like_post2(post_id):
#     post = Post.query.get(post_id)
#     if post:
#         current_user.liked_post2.append(post) #CAN I ADD A WHERE STATEMENT TO INCLUDE A POST_ID TO DELETE ALL THE INSTANCES?
#         db.session.commit()

#     return redirect(url_for('ig.homepage'))


# @ig.route('/posts/unlike/<post_id>')  ******DEPRECATED for React friendly version moved to api routes file*********
# @login_required
# def unlike_post2(post_id):
#     post = current_user.liked_post2.filter_by(id=post_id).first()
#     print(current_user.liked_post2)
#     if post in current_user.liked_post2.all():
#         current_user.liked_post2.remove(post)
#         db.session.commit()

#     return redirect(url_for('ig.homepage'))


#############  FOLLOWING ##################

@ig.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@ig.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)

    if user and user not in current_user.followed.all():
        current_user.followed.append(user)

        db.session.commit()

    return redirect(url_for('ig.users_page'))

@ig.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = current_user.followed.filter_by(id=user_id).first()
    if user:
        current_user.followed.remove(user)
        db.session.commit()
    return redirect(url_for('ig.users_page'))