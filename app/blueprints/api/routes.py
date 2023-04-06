from flask import request
from . import api
from app.models import Post


@api.route('/')
def index():
    return 'Hello this is the API'


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


@api.route('/posts', methods=['POST'])
def create_post():
    #check to see that the request is a json request
    if not request.is_json:
        return {'error': 'Request must be JSON'}, 400
    # get the data from the request
    data = request.json
    required_fields = ['title', 'body', 'user_id']
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
    user_id=data.get('user_id')

    #Create a new Post instance with the data from the request
    new_post = Post(title=title, body=body, image_url=image_url, user_id=user_id)

    #Return the new post as JSON response
    return new_post.to_dict(), 201
        
    return 'This is the create post route'
