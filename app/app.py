# backend/app.py
from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)
mongoDB_port = 27017
client = MongoClient(f"mongodb://mongodb:{mongoDB_port}/")  # mongodb is the hostname of MongoDB container

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data_recieved = {
        'name': request.form.get('name'),
        'email': request.form.get('email')
    }
    db = client['webapp_db']
    collection = db['user_data_collection']
    result = collection.insert_one(data_recieved)
    status = ''
    if result.acknowledged:
        status = 'Data Submitted Successfully, id: ' + str(result.inserted_id)
    else:
        status = 'Data Submission Failed, error: 500'

    users = list(collection.find())

    return render_template('index.html', status=status, users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
