"""
    Views module for things that aren't classifiable to specific entities.
"""
from flask import Blueprint, render_template


general = Blueprint('general', __name__)

@general.route('/')
def home():
    """
        Route for the index/home page.
    """
    return render_template('home.html')

@general.route('/about')
def about():
    """
        Route for the About page.
    """
    return render_template('about.html')
