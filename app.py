from flask import Flask
from flask import request, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_posts.json", "r") as read_file:
        blog_posts = json.load(read_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
