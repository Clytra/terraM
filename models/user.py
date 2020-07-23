from db import db


class UserModel(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)

    tournaments = db.relationship('TournamentModel', secondary='users_tournaments', backref=db.backref('members',
                                                                                                       lazy='dynamic'))
    scores = db.relationship('ScoreModel', backref='member', lazy='dynamic')


    def __init__(self, username: str, password: str, first_name: str, last_name: str, phone_number: str, email: str):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email

    def json(self):
        return {
            'id': self.id, 'username': self.username, 'password': self.password, 'first_name': self.first_name,
            'last_name': self.last_name, 'phone_number': self.phone_number, 'email': self.email
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_row(self):
        db.session.update(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
