from flask import Flask
from views.votes import bp_votes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_votes);
    return app

if __name__ == '__main__':
    app = create_app().run()
