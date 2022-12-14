'''
In main.py wird die Klasse Teilnehmer für die korrespondierende Ressource angelegt
und die benötigten Methoden implementiert. Zur Nutzung von Daten die in der Query übergeben werden
die requestParser von flask_restful verwendet. Zusätzlich wird die das Flask Projekt initialisiert
'''
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#Initialize the flask App
app=Flask(__name__)
#Wrap the app in api
api=Api(app)
#configure the database used for sql alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#argument parser to collect data from post and put request
teilnehmer_post_arguments = reqparse.RequestParser()
teilnehmer_post_arguments.add_argument("name", type=str, help="Name is required",
 required=True)
teilnehmer_post_arguments.add_argument("vorname", type=str, help="Vorname is required",
 required=True)
teilnehmer_post_arguments.add_argument("thema", type=str, help="Thema is required",
 required=True)
teilnehmer_post_arguments.add_argument("session_chair", type=str, help="Session Chair is required",
 required=True)
teilnehmer_post_arguments.add_argument("note", type=float, help="Note of teilnehmer is required",
 required=True)

#since not all arguments are required for patch, there is a need for a second argument parser
teilnehmer_patch_arguments = reqparse.RequestParser()
teilnehmer_patch_arguments.add_argument("name", type=str, help="Name of teilnehmer is required")
teilnehmer_patch_arguments.add_argument("vorname", type=str,
 help="Vorname of teilnehmer is required")
teilnehmer_patch_arguments.add_argument("thema", type=str, help="Thema of teilnehmer is required")
teilnehmer_patch_arguments.add_argument("session_chair", type=str,
 help="Session Chair of teilnehmer is required")
teilnehmer_patch_arguments.add_argument("note", type=float, help="Note of teilnehmer is required")

#with resource_fields the data that should be rendered in a response is defined 
resource_fields = {
    'id': fields.Integer,
    'vorname': fields.String,
    'name': fields.String,
    'thema': fields.String,
    'session_chair': fields.String,
    'note': fields.Float
}

class TeilnehmerModel(db.Model):
    '''
    In the class Teilnehmermodel the data fields for the Ressource
    Teilnehmer are defined.
    '''
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    thema = db.Column(db.String(200), nullable=False)
    session_chair = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Teilnehmer(vorname= {vorname},name = {name}, thema= {thema}, session_chair={session_chair}, note={note})"




class Teilnehmer(Resource):
    '''
    In der Klasse Teilnehmer, werden die HTTP-Methoden
    get, post, put, patch und delete definiert,
    die für die Interaktion mit der Teilnehmer Ressource benötigt werden.
    '''
    @marshal_with(resource_fields)
    def get(self, teilnehmer_id):
        '''Mit get wird die JSON Repräsentation der spezifizierte Ressource angefragt'''
        result = TeilnehmerModel.query.filter_by(id=teilnehmer_id).first()
        if not result:
            abort(404, message="could not find a teilnehmer with this id")
        return result

    @marshal_with(resource_fields)
    def post(self, teilnehmer_id):
        '''Mit post wird eine neue Ressource angelegt'''
        teilnehmer_check = TeilnehmerModel.query.filter_by(id=teilnehmer_id).first()
        if teilnehmer_check:
            abort(409, message="A Teilnehmer with this id already exists...")
        args = teilnehmer_post_arguments.parse_args()
        teilnehmer = TeilnehmerModel(id=teilnehmer_id,name=args['name'], vorname=args['vorname'],
         thema=args['thema'], session_chair=args['session_chair'], note=args['note'])
        db.session.add(teilnehmer)
        db.session.commit()
        return teilnehmer, 201

    @marshal_with(resource_fields)
    def put(self, teilnehmer_id):
        '''Mit put wird eine spezifizierte Ressource aktualisiert'''
        args = teilnehmer_post_arguments.parse_args()
        teilnehmer = TeilnehmerModel.query.filter_by(id=teilnehmer_id).first()

        if not teilnehmer:
            abort(404, message="Teilnehmer cannot be updated, because it can't be found")

        teilnehmer = TeilnehmerModel(name=args['name'], vorname=args['vorname'],
         thema=args['thema'], session_chair=args['session_chair'], note=args['note'])
        db.session.add(teilnehmer)
        db.session.commit()
        return teilnehmer, 201

    @marshal_with(resource_fields)
    def patch(self, teilnehmer_id):
        '''Die Methode patch wird zum partiellen modifizieren einer Ressource verwendet'''
        args = teilnehmer_patch_arguments.parse_args()
        teilnehmer = TeilnehmerModel.query.filter_by(id=teilnehmer_id).first()
        if not teilnehmer:
            abort(404, message="Teilnehmer cannot be updated, because it can't be found")
        if args['vorname']:
            teilnehmer.vorname = args['vorname']
        if args['name']:
            teilnehmer.name = args['name']
        if args['thema']:
            teilnehmer.thema = args['thema']
        if args['session_chair']:
            teilnehmer.session_chair = args['session_chair']
        if args['note']:
            teilnehmer.note = args['note']
        db.session.add(teilnehmer)
        db.session.commit()

        return teilnehmer, 201

    def delete(self, teilnehmer_id):
        '''delete löscht die spezifizierte Ressource'''
        to_be_deleted = TeilnehmerModel.query.get(teilnehmer_id)
        db.session.delete(to_be_deleted)
        db.session.commit()
        return "", 204

#add url for the Teilnehmer ressource
api.add_resource(Teilnehmer, "/teilnehmer/<int:teilnehmer_id>")

#initialize flask app
if __name__ == "__main__":
    app.run(debug=True)
