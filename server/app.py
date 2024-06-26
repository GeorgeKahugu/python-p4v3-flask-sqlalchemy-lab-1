# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False

migrate = Migrate(app, db)
db.init_app(app)

#Add views here

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes=Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()

    count=len(earthquakes)

    quakes=[]
    for earthquake in earthquakes:
        quake_data={
            'id':earthquake.id,
            'location':earthquake.location,
            'magnitude':earthquake.magnitude,
            'year':earthquake.year
        }
        quakes.append(quake_data)
    
    response_body={
        'count':count,
        'quakes':quakes
    }
    return jsonify(response_body),200

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):

    earthquake = Earthquake.query.get(id)

    if earthquake:
       
        response_body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        return jsonify(response_body), 200
    else:
        
        error_message = {'message': f'Earthquake {id} not found.'}
        return jsonify(error_message), 404


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
