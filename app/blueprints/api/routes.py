from flask import request
from app import db
from . import api
from app.models import Post, User
from .auth import basic_auth, token_auth


@api.route('/token')
@basic_auth.login_required
def index():
    user = basic_auth.current_user()
    token = user.get_token()
    return {'token': token, 'token_exp': user.token_expiration}


# END TO TO GET ALL THE POST 
@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return [post.to_dict() for post in posts]


@api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return {'error': 'Post not found'}, 404
    return post.to_dict()

#endpoint to create a new post
@api.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    #check to see that the request is a json request
    if not request.is_json:
        return {'error': 'Request must be JSON'}, 400
    # get the data from the request
    data = request.json
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'erroe': f"{', '.join(missing_fields)} are required"}, 400
    

    #Get the data from request body
    title=data.get('title')
    body=data.get('body')
    image_url=data.get('image_url')
    user = token_auth.current_user()

    #Create a new Post instance with the data from the request
    new_post = Post(title=title, body=body, image_url=image_url, user_id=user.id)

    #Return the new post as JSON response
    return new_post.to_dict(), 201
        
    return 'This is the create post route'


# @api.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     return [user.to_dict() for user in users]


@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {'error': 'User not found'}, 404
    return user.to_dict()


@api.route('/users', methods=['POST'])
def create_user():
    #check to see that the request is a json request
    if not request.is_json:
        return {'error': 'Request must be JSON'}, 400
    # get the data from the request
    data = request.json
    required_fields = ['first_name', 'last_name','email', 'username',  'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'erroe': f"{', '.join(missing_fields)} are required"}, 400
    

    #Get the data from request body
    first = data.get('first_name')
    last = data.get('last_name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')


    check_user = db.session.execute(db.select(User).filter((User.username == username)| (User.email== email))).scalars().all()
    if check_user:
        return {'error': 'User already exists'}, 400
    

    #Create a new User instance with the data from the request
    new_user = User(first_name=first , last_name=last, email=email, username=username, password=password, )

    #Return the new user as JSON response
    return new_user.to_dict(), 201

