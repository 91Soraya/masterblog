from flask import Flask
from flask import request, render_template, redirect, url_for
import json

app = Flask(__name__)


def get_all_posts():
    """read json file with blog posts and return the data"""
    with open("blog_posts.json", "r") as read_file:
        return json.load(read_file)


def create_new_id():
    """Create a new id for a new post based on the last id available in the json file"""
    blog_posts = get_all_posts()
    new_id = blog_posts[-1]["id"] + 1
    return new_id


def fetch_post_by_id(post_id):
    """Fetch a blog post with a specific id"""
    blog_posts = get_all_posts()
    fetched_post = {}
    for blog in blog_posts:
        if blog["id"] == post_id:
            fetched_post = blog
    return fetched_post


@app.route('/')
def index():
    """Render index.html and show all blog posts,
    with additional option to delete, update or add a blog post"""
    blog_posts = get_all_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post to the json file and redirects to index.html"""
    if request.method == 'POST':
        # Add the code that handles adding a new blog
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        new_id = create_new_id()

        all_posts = []
        with open("blog_posts.json", "r") as read_file:
            blog_posts = json.load(read_file)
            for post in blog_posts:
                all_posts.append(post)

        new_post = {"id": new_id, "author": author, "title": title, "content": content}
        all_posts.append(new_post)

        with open("blog_posts.json", "w") as write_file:
            json.dump(all_posts, write_file)

        return redirect(url_for("index"))
    return render_template("add.html")


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """Gets a post_id, and deletes the blog post linked to the id from the json file.
    Redirects to index.html after deletion"""
    updated_posts = []
    if request.method == 'POST':
        with open("blog_posts.json", "r") as read_file:
            blog_posts = json.load(read_file)
            for post in blog_posts:
                if post_id == post["id"]:
                    continue
                updated_posts.append(post)

    with open("blog_posts.json", "w") as write_file:
        json.dump(updated_posts, write_file)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Gets a post_id, shows update.html where the title, author and content can be updated.
    Saves the update in the json file and redirects to index.html"""
    post_to_update = fetch_post_by_id(post_id)
    if post_to_update is None:
        return "Post not found", 404

    if request.method == 'POST':
        updated_posts = []
        blog_posts = get_all_posts()
        content = request.form.get('content')
        title = request.form.get('title')
        author = request.form.get('author')
        for blog in blog_posts:
            if blog['id'] == post_id:
                blog['title'] = title
                blog['author'] = author
                blog['content'] = content
            updated_posts.append(blog)

        with open("blog_posts.json", "w") as write_file:
            json.dump(updated_posts, write_file)

        return redirect(url_for('index'))

    return render_template('update.html', post=post_to_update)


if __name__ == '__main__':
    app.run()
