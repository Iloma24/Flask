from flask_mega_tutorial.C1_first_app.microblog.app import appObj

@appObj.route('/')
@appObj.route('/index')
def index():
    return 'Hello, world!'
