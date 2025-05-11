from flask import Flask, render_template
import json

app = Flask(__name__)

# Load blog posts from JSON file
def load_posts(filename='posts.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Attaches the flask app to the home route.
@app.route('/')
def home():
    """
    Calls the load_posts function by creating a variable and returns the index file
    and passing the posts parameter into the blog_posts argument.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# Runs the flask app by calling the run method.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
