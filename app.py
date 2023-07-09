from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("blog_posts.json", "r") as read_file:
        blog_posts = json.load(read_file)
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run()