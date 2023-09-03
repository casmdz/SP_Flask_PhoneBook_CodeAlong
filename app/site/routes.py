from flask import Blueprint, render_template

# variable site, instantiate the BP class 
site = Blueprint('site', __name__, template_folder='site_templates')
# all will be related to how the site runs 

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')