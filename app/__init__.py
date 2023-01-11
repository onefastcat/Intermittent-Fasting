from flask import Flask, render_template
from flask import render_template
from config import Config
from app import routes





app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes.bp)


if __name__ == "__main__":
    app.run()
