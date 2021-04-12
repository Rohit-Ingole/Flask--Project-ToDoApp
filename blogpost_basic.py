from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)

# creating datbase
class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False) # this field cannot be null
	content = db.Column(db.Text, nullable=False)
	author = db.Column(db.String, nullable=False, default="N/A")
	date_post = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return "Blog post" + str(self.id)

@app.route("/")
def index():
	return render_template("index.html")
	# can return any thing including HTML code for good look of website

# sending data to HTML file to display the data on the screen
@app.route("/posts", methods=["GET", "POST"])
def posts():
	if request.method == "POST":
		post_title = request.form["title"]
		post_content = request.form["content"]
		post_author = request.form["author"]

		new_post = BlogPost(title=post_title, author=post_author, content=post_content)

		db.session.add(new_post)
		db.session.commit()

		return redirect("/posts")

	else:
		all_posts = BlogPost.query.order_by(BlogPost.date_post).all()
		return render_template("posts.html", posts = all_posts)

@app.route("/posts/delete/<int:id>")
def delete(id):
	post = BlogPost.query.get_or_404(id)

	db.session.delete(post)
	db.session.commit()

	return redirect("/posts")

@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
	post = BlogPost.query.get_or_404(id)

	if request.method == "POST":
		post.title = request.form["title"]
		post.author = request.form["author"]
		post.content = request.form["content"]

		db.session.commit()

		return redirect("/posts")

	else:
		return render_template("edit.html", post=post)

if __name__ == "__main__":
	app.run(debug=True)
