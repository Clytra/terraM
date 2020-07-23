from flask_jwt import jwt_required
from flask_jwt_extended import get_jwt_claims
from flask_restful import Resource, reqparse
from models.tournament import TournamentModel



BLANK_ERROR = "'{}' nie może być puste."
ITEM_NOT_FOUND = "Nie znaleziono rekordu."
ADMIN_PERMISSION = "Wymagane uprawnienia administratora."
NAME_ALREADY_EXISTS = "Użytkownik o takim nicku już istnieje."
ERROR_ADDING = "Wystąpił błąd podczas dodawania danych."
SUCCESS_DELETING = "Dane usunięto pomyślnie."
ERROR_EDITING = "Wystąpił błąd podczas edycji danych."
CREATED_SUCCESSFULLY = "Turniej został dodany pomyślnie."


class Tournament(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tournament_name', type=str, required=False)

    @classmethod
    def get(cls, id):

        tournament = TournamentModel.find_by_id(id)

        if tournament:
            return tournament.json(), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def delete(cls, id: int):

        tournament = TournamentModel.find_by_id(id)

        if not tournament:
            return {"message": ITEM_NOT_FOUND}, 404
        tournament.delete_from_db()
        return {"message": SUCCESS_DELETING}, 200

    @classmethod
    def put(cls, id):

        data = Tournament.parser.parse_args()
        tournament = TournamentModel.find_by_id(id)
        if tournament:
            tournament.tournament_name = data['tournament_name']
        try:
            tournament.save_to_db()
        except:
            return {"message": ERROR_EDITING}, 500

        return tournament.json(), 200


class AddTournament(Resource):
    # @jwt_required
    def post(cls):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        # return {'message': ADMIN_PERMISSION}, 401
        data = Tournament.parser.parse_args()

        if TournamentModel.find_by_name(data["tournament_name"]):
            return {"message": NAME_ALREADY_EXISTS}, 400

        tournament = TournamentModel(**data)

        tournament.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201





class TournamentList(Resource):
    def get(self):
        return {"tournaments": [row.json() for row in TournamentModel.find_all()]}
