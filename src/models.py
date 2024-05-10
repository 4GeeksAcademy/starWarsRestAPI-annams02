from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    Personaje_Favoritos = db.relationship('Personaje_Favoritos', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active 
        }

class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    usuario = db.relationship('User') 
    planeta_id = db.Column(db.Integer, db.ForeignKey('planets.id_planeta'))  
    planeta = db.relationship("Planets")    
    nombre_id = db.Column(db.Integer, db.ForeignKey('people.id_persona'))  
    nombre = db.relationship("People")  

class Personaje_Favoritos(db.Model):
    __tablename__= 'personaje_favoritos'
    id =db.Column(db.Integer,primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    people_id = db.Column(db.Integer, db.ForeignKey('people.id_persona'))  

    def __repr__(self):
        return f'<Personaje_Favoritos{self.id}>'
    
    def serialize(self):
        return{
            "id":self.id,
            "usuario_id":self.usuario_id,
            "people_id":self.people_id,
        }  
    
class Planeta_favoritos(db.Model):
    __tablename__= 'planeta_favoritos'
    id =db.Column(db.Integer,primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    planeta_id = db.Column(db.Integer, db.ForeignKey('planets.id_planeta'))  

    def __repr__(self):
        return f'<Planeta_favoritos{self.id}>'
    
    def serialize(self):
        return{
            "id":self.id,
            "usuario_id":self.usuario_id,
            "planet_id":self.planet_id
        }  
    

class People(db.Model):
    __tablename__ = 'people'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre_persona = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    color_de_piel = db.Column(db.String(20), nullable=False)
    color_de_pelo = db.Column(db.String(20))
    genero = db.Column(db.String(20))
    birth_year = db.Column(db.Integer, nullable=False)
    Personaje_Favoritos = db.relationship('Personaje_Favoritos', backref='People', lazy=True)

    def __repr__(self):
        return f'<People {self.nombre_persona}>'

    def serialize(self):
        return {
            "id_persona": self.id_persona,
            "nombre_persona": self.nombre_persona,
            "peso": self.peso,
            "color_de_piel": self.color_de_piel,
            "color_de_pelo": self.color_de_pelo,
            "genero": self.genero,
            "birth_year": self.birth_year
          
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id_planeta = db.Column(db.Integer, primary_key=True)
    nombre_planeta = db.Column(db.String(100), nullable=False)
    periodo_rotacion = db.Column(db.Integer, nullable=False)
    diametro = db.Column(db.Float, nullable=False)
    clima = db.Column(db.String(50), nullable=False)
    terreno = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Planets {self.nombre_planeta}>'

    def serialize(self):
        return {
            "id_planeta": self.id_planeta,
            "nombre_planeta": self.nombre_planeta,
            "periodo_rotacion": self.periodo_rotacion,
            "diametro": self.diametro,
            "clima": self.clima,
            "terreno": self.terreno
        }