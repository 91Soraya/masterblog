from flask import Flask
from flask import request, render_template, redirect, url_for
import json

app = Flask(__name__)


def create_new_id():
    with open("blog_posts.json", "r") as read_file:
        blog_posts = json.load(read_file)
        new_id = blog_posts[-1]["id"] + 1
        return new_id


@app.route('/')
def index():
    with open("blog_posts.json", "r") as read_file:
        blog_posts = json.load(read_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
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

        new_post = {}
        new_post["id"] = new_id
        new_post["author"] = author
        new_post["title"] = title
        new_post["content"] = content
        all_posts.append(new_post)

        with open("blog_posts.json", "w") as write_file:
            json.dump(all_posts, write_file)

        return redirect(url_for("index"))
    return render_template("add.html")




if __name__ == '__main__':
    app.run()
