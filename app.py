from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


# Load blog posts from a JSON file
def load_blog_posts():
    with open('blog_posts.json', 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


# Route for adding a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = {
            'id': len(load_blog_posts()) + 1,  # Auto generate ID
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        blog_posts = load_blog_posts()
        blog_posts.append(new_post)

        # Save blog posts back to the file
        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))
    return render_template('add.html')


# Route to delete a blog post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list
    with open('blog_posts.json', 'w') as f:
        json.dump(blog_posts, f)

    return redirect(url_for('index'))


# Route for updating a blog post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Save updated blog post
        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
