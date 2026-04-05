from flask_frozen import Freezer
from main import app

freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DESTINATION'] = 'build' # This names the output folder

if __name__ == '__main__':
    freezer.freeze()