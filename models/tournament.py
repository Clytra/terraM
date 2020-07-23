from db import db



class TournamentModel(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer(), primary_key=True)
    tournament_name = db.Column(db.String(80))

    scores = db.relationship('ScoreModel', backref='tour', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, tournament_name: str):
        self.tournament_name = tournament_name

    def json(self):
        return {
            'id': self.id, 'tournament_name': self.tournament_name
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, tournament_name):
        return cls.query.filter_by(tournament_name=tournament_name).first()

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
