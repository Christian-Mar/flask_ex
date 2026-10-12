from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/post/<int:post_id>")
    def post(post_id):
        return render_template("post.html")

    return app
