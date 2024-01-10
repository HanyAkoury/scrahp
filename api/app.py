from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////db/scrahp.db"
db = SQLAlchemy(app)


class Articles(db.Model):
    url = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(255), nullable=False)


description = """
                <!DOCTYPE html>
                <head>
                <title>API Landing</title>
                </head>
                <body>  
                    <h3>A simple API using Flask</h3>
                    <a href="http://localhost:5000/api?value=2">sample request</a>
                </body>
                """


@app.route("/", methods=["GET"])
def homepage():
    return description


@app.route("/test")
def test():
    return "This is a test route. Your query worked!"


@app.route("/articles", methods=["GET"])
def get_articles():
    article_url = request.args.get("url")
    articles = Articles.query.all()

    if article_url:
        specific_article = [
            {"url": article.url, "title": article.title}
            for article in articles
            if article.url == article_url
        ]
        return jsonify({"articles": specific_article})
    else:
        articles_list = [
            {"url": article.url, "title": article.title} for article in articles
        ]
        return jsonify({"articles": articles_list})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
