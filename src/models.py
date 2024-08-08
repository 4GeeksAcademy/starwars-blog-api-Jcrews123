from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship("Favorites", backref="user_favorites")

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, email, ):
        self.username = username
        self.email = email
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": [favorite.serialize() for favorite in self.favorites]
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="people")

    def __init__(self, name, description):
        self.name = name
        self.description = description

        db.session.add(self)
        try: 
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)
        
    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "description": self.description,
        }
    
class Planets(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer)
    description = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="planets")

    def __init__(self, name, population, description):
        self.name = name
        self.population = population
        self.description = description
        db.session.add(self)
        try: 
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "population": self.population,
            "description": self.description,
            # "favorites": self.favorites,
        }    
    
class Species(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    language = db.Column(db.String(50))
    description = db.Column(db.String(100), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="species")
    
    def __init__(self, name):
        self.name = name
        db.session.add(self)
        try: 
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "language": self.language,
            "description": self.description,
            # "favorites": self.favorites,
        }        
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.uid"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.uid"))
    species_id = db.Column(db.Integer, db.ForeignKey("species.uid"))

    def __init__(self, user_id, people_uid = None, planets_uid = None, species_uid = None):
        if people_uid is not None and planets_uid is not None and species_uid is not None:
            raise ValueError("A favorite can only have either a character or a planet, not both.")
        if people_uid is None and planets_uid is None and species_uid is None:
            raise ValueError("A favorite must have either a character or a planet.")
        self.user_id = user_id
        self.people_uid = people_uid
        self.planets_uid = planets_uid
        self.species_uid = species_uid
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def serialize(self):
        item_id = self.people_id if self.people_id else self.planets_id
        item_name = self.people_id.name if self.people else self.planets.name
        item_type = "person" if self.people_id else "planet"
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': item_id,
            'item_name': item_name,
            'item_type': item_type
        }