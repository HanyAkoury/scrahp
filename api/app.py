from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////db/scrahp.db"
db = SQLAlchemy(app)


class Articles(db.Model):
    """
    Represents an article record in the database.

    Attributes:
        url (str): Unique URL of the article, serving as the primary key.
        title (str): Title of the article.
        author (str): Author of the article.
        content (str): Content of the article.
    """

    url = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(), nullable=False)


@app.route("/", methods=["GET"])
def home():
    """
    Render the landing page of the website.

    Returns:
        Rendered template: The landing page.
    """
    return render_template("landing_page.html")


@app.route("/articles", methods=["GET"])
def get_articles():
    """
    Retrieve articles from the database. Can choose to optionally filter by a specific URL.

    Returns:
        json: A list of articles or a specific article if a URL parameter is provided.
    """
    article_url = request.args.get("url")
    articles = Articles.query.all()

    # Check if a specific article is asked for using an url
    if article_url:
        specific_article = [
            {"url": article.url, "title": article.title, "author": article.author, "content": article.content}
            for article in articles
            if article.url == article_url
        ]
        return jsonify({"articles": specific_article})
    else:
        articles_list = [{"url": article.url, "title": article.title, "author": article.author, "content": article.content} for article in articles]
        return jsonify({"articles": articles_list})


@app.route("/top_authors", methods=["GET"])
def top_authors():
    """
    Retrieve the top authors based on the number of articles written.

    Returns:
        json: A list of top authors and their article count, excluding 'n/a'.
    """
    # Exclude authors with the value "n/a"
    top_authors = (
        db.session.query(Articles.author, func.count(Articles.author).label("article_count"))
        .filter(Articles.author != "n/a")
        .group_by(Articles.author)
        .order_by(func.count(Articles.author).desc())
        .limit(5)
        .all()
    )

    result = [{"author": author, "article_count": article_count} for author, article_count in top_authors]
    return jsonify({"top_authors": result})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
