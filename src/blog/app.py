import json
from pathlib import Path

from flask import Flask, abort, render_template

POSTS_FILE = Path(__file__).parent / "posts.json"


def load_posts():
    with POSTS_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def create_app():
    app = Flask(__name__)

    @app.context_processor
    def inject_categories():
        categories = sorted({c for p in load_posts() for c in p["categories"]})
        return {"categories": categories}

    @app.route("/")
    def index():
        return render_template("index.html", posts=load_posts())

    @app.route("/post/<int:post_id>")
    def post(post_id):
        post = next((p for p in load_posts() if p["id"] == post_id), None)
        if post is None:
            abort(404)
        return render_template("post.html", post=post)

    return app
