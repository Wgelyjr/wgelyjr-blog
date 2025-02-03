from flask import Flask

# blueprint import
from database import database
from apps.blog.views import blog

def create_app():
    app = Flask(__name__)
    
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # Enter the application context here
    with app.app_context():
        # setup all our dependencies
        database.init_app(app)
    
    # register blueprint
    app.register_blueprint(blog)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
