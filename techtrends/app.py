import sqlite3
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    app.config['connection_counter']+=1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

def get_total_posts():
    connection = get_db_connection()
    total_no_of_posts = connection.execute('SELECT count(*) as count FROM posts').fetchone()
    connection.close()
    return total_no_of_posts

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info("A non-existing article is accessed post_id: %s",post_id); 
      return render_template('404.html'), 404
    else:
      app.logger.info("Article %s retrieved", post['title']);  
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("The About Us page is retrieved."); 
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.debug("A new article is created with title %s", title );  
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route("/healthz")
def status():
    response = app.response_class(
        response = json.dumps({"result":"Ok -healthy"}),
        status = 200,
        mimetype='application/json'
    )
    app.logger.debug("Status request successfull")
    return response

@app.route("/metrics")
def metrics():
    total_no_of_posts = get_total_posts()
    connection_counter = app.config['connection_counter']
    response = app.response_class(
        response = json.dumps({"db_connection_count": connection_counter, "post_count": total_no_of_posts['count']}),
        status = 200,
        mimetype='application/json'
    )
    app.logger.debug("Metrics request successfull")
   
    return response 
# start the application on port 3111
if __name__ == "__main__":
    # set logger to handle STDOUT and STDERR
   stdout_handler =  logging.StreamHandler(sys.stdout)# stdout handler 
   stderr_handler =  logging.StreamHandler(sys.stderr)# stderr handler 
   handlers = [stderr_handler, stdout_handler]
   # format output
   app.config['connection_counter']=0
   format_output = '%(asctime)s %(message)s'# formating output here
   logging.basicConfig(level= logging.DEBUG, format=format_output, datefmt='%m/%d/%Y %I:%M:%S %p',handlers=handlers)
   app.run(host='0.0.0.0', port='3111')
