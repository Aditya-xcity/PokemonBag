# Question: This file serves as the main Flask entry point for the Pokémon Bag web application
# Name - ADITYA BHARDWAJ
# Section - D2
# Roll No - 08
# Course – B TECH
# Branch – CSE
#
# Description:
# This file initializes and configures the Flask application.
# It sets up static and template directories, loads configuration,
# registers all application blueprints, and defines the main page route.
#
# The create_app() factory pattern is used to keep the application
# modular, scalable, and easy to test or extend.
#
# This file is responsible for starting the development server
# when the application is run directly.



from flask import Flask, render_template
from routes.bag_routes import bag_bp
import config
import os

def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )

    # Load config if needed later
    app.config.from_object(config)

    # Register blueprints
    app.register_blueprint(bag_bp)

    # ---------------- PAGES ----------------
    @app.route("/")
    def bag_page():
        return render_template("bag.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
