# draft

https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

> virtualenv .pyenv
$ source .pyenv/bin/activate
$ pip install Flask
$ pip freeze > requirements.txt
$ cat requirements.txt
$ python run.py



> .pyenv/bin/pip install flask
> .pyenv/bin/pip install mtgsdk

> sqlite3 app/db/draft.db < app/db/schema.sql


frontend:

/pods/new create
/pods view (by email address?)
/pods/:id

/user/:hash current pack


frontend: npm install and npm start


download prod db
download latest mtgjson
add set to models/set
run app
localhost:5000/api/v1/sets/seed
delete the non-rated cards that might reappear
get draftsim ratings
find/replace _
export to csv
delete/import card_ratings
localhost:5000/api/v1/sets/transfer_ratings
delete non-rated non-basics