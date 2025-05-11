from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load blog posts from JSON file
def load_posts(filename='posts.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Save blog posts to JSON file
def save_posts(posts, filename='posts.json'):
    with open(filename, 'w') as f:
        json.dump(posts, f, indent=4)


# Attaches the flask app to the home route.
@app.route('/')
def index():
    """
    Calls the load_posts function by creating a variable and returns the index file
    and passing the posts parameter into the blog_posts argument.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():

    # IF a post request is sent to this route, it will add a new blog post
    # Route to add a new blog post
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Generate the next ID for the new post
        blog_posts = load_posts()
        new_id = max([post['id'] for post in blog_posts], default=0) + 1

        # Create the new blog post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Add the new post to the list and save it
        blog_posts.append(new_post)
        save_posts(blog_posts)

        # Redirect back to the homepage
        return redirect(url_for('index'))

    # If a GET request, render the form for adding a new post
    # display a form for adding a new blog post.
    return render_template('add.html')




# Runs the flask app by calling the run method.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
