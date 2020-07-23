from db import db


class UserTournamentModel(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users_tournaments'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    tournament_id = db.Column('tournament_id', db.Integer, db.ForeignKey('tournaments.id'))

    def __init__(self, user_id: int, tournament_id: int):
        self.user_id = user_id
        self.tournament_id = tournament_id

    def json(self):
        return {
            'id': self.id, 'user_id': self.user_id, 'tournament_id': self.tournament_id
        }

    @classmethod
    def save_to_db(cls):
        db.session.add(cls)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
