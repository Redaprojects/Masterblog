from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts(filename='posts.json'):
    """Retrieves all blog posts from JSON file"""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts, filename='posts.json'):
    """Overwrites a blog post from JSON file"""
    with open(filename, 'w') as f:
        json.dump(posts, f, indent=4)


# Attaches the flask app to the index route.
@app.route('/')
def index():
    """
    Calls the load_posts function by creating a variable and returns the index file
    and passing the posts parameter into the blog_posts argument.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


# Attaches the flask app to the add route.
@app.route('/add', methods=['GET', 'POST'])
def add():
    """Adds a new post by previewing the form file to the user."""
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


# Attaches the flask app to the delete route.
@app.route('/delete/<int:post_id>')
def delete(post_id):
    """ Loads then removes an existing post from the storage by selecting its unique ID."""
    blog_posts = load_posts()

    # Creates a new list of posts that do not have the ID we want to delete.
    # This effectively removes the targeted post.
    # Remove the post with matching ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    # Redirect back to the home page
    return redirect(url_for('index'))


# create a helper function to retrieve a post by ID:
def fetch_post_by_id(post_id, filename='posts.json'):
    posts = load_posts(filename)
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


# Attaches the flask app to the update route.
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Modifies an existing post in the storage by specifying a unique ID, overwriting it and
    Save it to the storage.
    """
    # To display the update form, populated with the current details of the blog post.
    posts = load_posts()
    post = next((pos_t for pos_t in posts if pos_t['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    # If the request is a POST it will update the details for the blog post from the list.
    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

# Runs the Flask app by calling the run method.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
