from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://petproject-34206-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

db_ref = db.reference()

@app.route('/posts')
def get_posts():
    """Retrieves all posts from the database."""
    posts = db_ref.child('posts').get()
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    """Creates a new post in the database."""
    data = request.get_json()

    data['tags'] = data.get('tags', [])
    db_ref.child('posts').push(data)
    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/posts/<post_id>')
def get_post(post_id):
    """Retrieves a specific post from the database."""
    post = db_ref.child('posts').child(post_id).get()
    return jsonify(post)

@app.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Updates an existing post in the database."""
    data = request.get_json()
    
    data['tags'] = data.get('tags', [])
    db_ref.child('posts').child(post_id).update(data)
    return jsonify({'message': 'Post updated successfully'}), 200

@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Deletes a specific post from the database."""
    db_ref.child('posts').child(post_id).delete()
    return jsonify({'message': 'Post deleted successfully'}), 200


@app.route('/posts/tags/<tag>')
def get_posts_by_tag(tag):
    """Retrieves posts associated with a specific tag."""
    posts = db_ref.child('posts').order_by_child('tags').equal_to(tag).get()
    return jsonify(posts)

@app.route('/users/<user_id>/favorite-tags', methods=['GET'])
def get_favorite_tags(user_id):
    """Retrieves favorite tags for a specific user."""
    favorite_tags = db_ref.child('users').child(user_id).child('favoriteTags').get()
    return jsonify(favorite_tags)

@app.route('/users/<user_id>/favorite-tags', methods=['POST'])
def add_favorite_tag(user_id):
    """Adds a favorite tag for a user."""
    tag = request.get_json()['tag']
    db_ref.child('users').child(user_id).child('favoriteTags').push(tag)
    return jsonify({'message': 'Favorite tag added successfully'}), 201

@app.route('/users/<user_id>/favorite-tags/<tag>', methods=['DELETE'])
def remove_favorite_tag(user_id, tag):
    """Removes a favorite tag for a user."""
    db_ref.child('users').child(user_id).child('favoriteTags').child(tag).delete()
    return jsonify({'message': 'Favorite tag removed successfully'}), 200

@app.route('/posts/<post_id>/comments')
def get_comments(post_id):
    """Retrieves comments for a specific post."""
    comments = db_ref.child('posts').child(post_id).child('comments').get()
    return jsonify(comments)

@app.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Creates a new comment for a post."""
    data = request.get_json()
    db_ref.child('posts').child(post_id).child('comments').push(data)
    return jsonify({'message': 'Comment created successfully'}), 201

@app.route('/posts/<post_id>/comments/<comment_id>', methods=['PUT'])
def update_comment(post_id, comment_id):
    """Updates an existing comment for a post."""
    data = request.get_json()
    db_ref.child('posts').child(post_id).child('comments').child(comment_id).update(data)
    return jsonify({'message': 'Comment updated successfully'}), 200

@app.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    """Deletes a specific comment from a post."""
    db_ref.child('posts').child(post_id).child('comments').child(comment_id).delete()
    return jsonify({'message': 'Comment deleted successfully'}), 200

@app.route('/posts/<post_id>/comments/<comment_id>/replies')
def get_replies(post_id, comment_id):
    """Retrieves replies for a specific comment."""
    replies = db_ref.child('posts').child(post_id).child('comments').child(comment_id).child('replies').get()
    return jsonify(replies)

@app.route('/posts/<post_id>/comments/<comment_id>/replies', methods=['POST'])
def create_reply(post_id, comment_id):
    """Creates a new reply for a comment."""
    data = request.get_json()
    db_ref.child('posts').child(post_id).child('comments').child(comment_id).child('replies').push(data)
    return jsonify({'message': 'Reply created successfully'}), 201

@app.route('/posts/<post_id>/comments/<comment_id>/replies/<reply_id>', methods=['PUT'])
def update_reply(post_id, comment_id, reply_id):
    """Updates an existing reply for a comment."""
    data = request.get_json()
    db_ref.child('posts').child(post_id).child('comments').child(comment_id).child('replies').child(reply_id).update(data)
    return jsonify({'message': 'Reply updated successfully'}), 200

@app.route('/posts/<post_id>/comments/<comment_id>/replies/<reply_id>', methods=['DELETE'])
def delete_reply(post_id, comment_id, reply_id):
    """Deletes a specific reply from a comment."""
    db_ref.child('posts').child(post_id).child('comments').child(comment_id).child('replies').child(reply_id).delete()
    return jsonify({'message': 'Reply deleted successfully'}), 200

@app.route('/posts/<post_id>/comments/<comment_id>/accept', methods=['POST'])
def accept_comment(post_id, comment_id):
    """Accepts a specific comment for a post."""
    db_ref.child('posts').child(post_id).child('comments').child(comment_id).update({'accepted': True})
    return jsonify({'message': 'Comment accepted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
