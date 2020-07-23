from flask_restful import Resource, reqparse
from db import db

from models.tournament import TournamentModel
from models.user import UserModel
from models.score import ScoreModel

BLANK_ERROR = "'{}' nie może być puste."


class JoinTournament(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True, help=BLANK_ERROR.format('user_id'))
    parser.add_argument('tournament_id', type=int, required=True, help=BLANK_ERROR.format('tournament_id'))

    @classmethod
    def put(cls, user_id, tournament_id):


        tournament = TournamentModel.find_by_id(tournament_id)
        user = UserModel.find_by_id(user_id)

        if user is not None:
            tournament.members.append(user)
            db.session.commit()
            db.session.close()

        score = ScoreModel(has_own_game=0, status='uczestnik', end_terra_first=0, end_terra_second=0,
                           group1=None, group2=None, pz1=None, pz2=None, pz3=None, pb1=None, pb2=None,
                           pb_sum=None, tb1=None, tb2=None, user_id=user_id, tournament_id=tournament_id)
        user.scores.append(score)
        db.session.add(user)
        db.session.commit()
        db.session.close()






