from flask import Flask, render_template, jsonify, request
from Seminar_3_SQL_Alchemy.Lecture.models import db, User, Post, Comment
from datetime import datetime, timedelta

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../../instance/mydatabase.database'
db.init_app(app)


@app.route('/')
def index():
    return render_template('base_SQL_Alchemy.html')


@app.route('/data/')
def data():
    return 'Your data!'


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'users': users, 'title': 'Все пользователи'}
    return render_template('users.html', **context)


@app.route('/users_search/', methods=['GET', 'POST'])
def users_by_username():
    username = request.form.get('user_search')
    users = User.query.filter(User.username == username).all()
    context = {'users': users, 'title': 'Поиск пользователя'}
    return render_template('users_search.html', **context, username=username)


@app.route('/posts/author/<int:user_id>/')
def get_posts_by_author(user_id):
    posts = Post.query.filter_by(author_id=user_id).all()
    if posts:
        return jsonify([{'id': post.id, 'title': post.title,
                         'content': post.content,
                         'created_at': post.created_at} for post in posts])
    else:
        return jsonify({'error': 'Posts not found'})


@app.route('/posts/last-week/')
def get_posts_last_week():
    date = datetime.utcnow() - timedelta(days=7)
    posts = Post.query.filter(Post.created_at >= date).all()
    if posts:
        return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'created_at': post.created_at} for post in posts])
    else:
        return jsonify({'error': 'Posts not found'})


if __name__ == '__main__':
    app.run(debug=True)
