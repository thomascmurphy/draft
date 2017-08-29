from flask import Flask

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file , draft.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/draft.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('DRAFT_SETTINGS', silent=True)

#from app import views, models
