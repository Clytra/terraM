from flask_jwt import jwt_required
from flask_jwt_extended import get_jwt_claims, jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse


from models.score import ScoreModel

BLANK_ERROR = "'{}' nie może być puste."
ITEM_NOT_FOUND = "Nie znaleziono rekordu."
ADMIN_PERMISSION = "Wymagane uprawnienia administratora."
NAME_ALREADY_EXISTS = "Użytkownik o takim nicku już istnieje."
ERROR_ADDING = "Wystąpił błąd podczas dodawania danych."
SUCCESS_DELETING = "Dane usunięto pomyślnie."
ERROR_EDITING = "Wystąpił błąd podczas edycji danych."

class Score(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('has_own_game', type=bool)
    parser.add_argument('end_terra_first', type=bool, default=0)
    parser.add_argument('end_terra_second', type=bool, default=0)
    parser.add_argument('status', type=enumerate, default='oczekujący', required=True)
    parser.add_argument('group1', type=int, required=False)
    parser.add_argument('group2', type=int, required=False)
    parser.add_argument('pz1', type=int, required=False)
    parser.add_argument('pz2', type=int, required=False)
    parser.add_argument('pz3', type=int, required=False)
    parser.add_argument('pb1', type=int, required=False)
    parser.add_argument('pb2', type=int, required=False)
    parser.add_argument('pb_sum', type=int, required=False)
    parser.add_argument('tb1', type=int, required=False)
    parser.add_argument('tb2', type=int, required=False)
    parser.add_argument('user_id', type=int, required=False)
    parser.add_argument('tournament_id', type=int, required=False)

    @classmethod
    def delete(cls, user_id: int, tournament_id: int):

        score = ScoreModel.find_by_id(user_id, tournament_id)

        if not score:
            return {"message": ITEM_NOT_FOUND}, 404
        score.delete_from_db()
        return {"message": SUCCESS_DELETING}, 200

    @classmethod
    def put(cls, user_id: int, tournament_id: int):

        data = Score.parser.parse_args()
        score = ScoreModel.find_by_id(user_id, tournament_id)
        if score:
            score.has_own_game = data['has_own_game']
            score.end_terra_first = data['end_terra_first']
            score.end_terra_second = data['end_terra_second']
            score.status = data['status']
            score.group1 = data['group1']
            score.group2 = data['group2']
            score.pz1 = data['pz1']
            score.pz2 = data['pz2']
            score.pz3 = data['pz3']
        try:
            score.save_to_db()
        except:
            return {"message": ERROR_EDITING}, 500

        return score.json(), 200

class DeleteMember(Resource):
    @classmethod
    @jwt_required
    def delete(cls, tournament_id, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': ADMIN_PERMISSION}, 401
        tournament = ScoreModel.find_by_id(tournament_id)
        member = ScoreModel.find_by_id(user_id)

        if tournament:
            if member:
                member.delete_from_db()
                return {"message": SUCCESS_DELETING}, 200
            return {"message": ITEM_NOT_FOUND}, 404
        return {"message": ITEM_NOT_FOUND}, 404



class FirstRound(Resource):
    @classmethod
    def put(cls, tournament_id):

        tournament = ScoreModel.get_all_members(tournament_id)
        number = len(tournament)

        tournament = ScoreModel.get_number_of_tables(number, tournament)

        if tournament:
            for row in tournament:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.find_all(tournament_id)]}

class SecondRound(Resource):
    @classmethod
    def put(cls, tournament_id):

        check_owners = ScoreModel.get_all_members(tournament_id)
        groups2 = []

        if check_owners:
            for row in check_owners:
                if row.has_own_game:
                    row.group2 = row.group1
                    groups2.append(row.group2)
                    row.save_to_db()

        tournament = ScoreModel.get_group2(tournament_id)

        number = len(tournament)

        tournament = ScoreModel.get_number_of_tables2(number, tournament, groups2)

        if tournament:
            for row in tournament:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.find_all(tournament_id)]}

class ThirdRound(Resource):
    @classmethod
    def put(cls, tournament_id):

        sumPoints = ScoreModel.get_all_members(tournament_id)

        sumPoints = ScoreModel.pb_summary(sumPoints)

        if sumPoints:
            for row in sumPoints:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.get_finalists(tournament_id)]}

class TournamentPointsFirst(Resource):
    @classmethod
    def put(cls, tournament_id, group1):

        tournament = ScoreModel.get_group(tournament_id, group1)

        tournament = ScoreModel.add_pb1(tournament)

        if tournament:
            for row in tournament:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.find_all(tournament_id)]}

class TournamentPointsSecond(Resource):
    @classmethod
    def put(cls, tournament_id, group2):

        tournament = ScoreModel.get_points(tournament_id, group2)

        tournament = ScoreModel.add_pb2(tournament)

        if tournament:
            for row in tournament:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.find_all(tournament_id)]}

class TieBreakerFirst(Resource):
    @classmethod
    def put(cls, tournament_id, user_id):

        tournament = ScoreModel.get_all_members(tournament_id)
        user = ScoreModel.get_user(user_id)

        tournament = ScoreModel.add_tie_breaker1(tournament, user, user_id)

        if tournament:
            for row in tournament:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.find_all(tournament_id)]}

class TieBreakerSecond(Resource):
    @classmethod
    def put(cls, tournament_id, user_id):

        tournament = ScoreModel.get_all_members(tournament_id)
        user = ScoreModel.get_user(user_id)

        tournament = ScoreModel.add_second_tie_breaker(tournament, user, user_id)

        if tournament:
            for row in tournament:
                row.save_to_db()

        return {"scores": [row.json() for row in ScoreModel.find_all(tournament_id)]}

class ScoreTournamentList(Resource):
    @classmethod
    def get(cls, tournament_id):
        scores = [score.json() for score in ScoreModel.find_all(tournament_id)]
        if scores:
            return {"scores": scores}, 200
        return {"message": ITEM_NOT_FOUND}, 404


#    def get(self):
#        scores = [score.json() for score in ScoreModel.find_all()]
#        return {'scores': scores}, 200
#    @jwt_optional
#    def get(self):
#        user_id = get_jwt_identity()
#        scores = [score.json() for score in ScoreModel.find_all()]
#        if user_id:
#            return {'scores': scores}, 200
#        return (
#            {
#                'scores': [score[''] for score in scores],
#                'message': 'Więcej informacji po zalogowaniu.'
#            }
#        )