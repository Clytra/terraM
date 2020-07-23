from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS

from db import db
from blacklist import BLACKLIST
from resources.user import (
    User,
    UserList,
    UserRegister,
    UserLogin,
    UserLogout,
    TokenRefresh
)
from resources.tournament import (
    Tournament,
    AddTournament,
    TournamentList
)

from resources.usertournament import JoinTournament

from resources.score import (
    Score,
    FirstRound,
    SecondRound,
    ThirdRound,
    TournamentPointsFirst,
    TournamentPointsSecond,
    TieBreakerFirst,
    TieBreakerSecond,
    ScoreTournamentList
)


app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(
        identity
):
    if (
            identity == 1
    ):
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
            decrypted_token['jti'] in BLACKLIST
    )


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'message': 'Token wygasł', 'error': 'token wygasł'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(
        error
):
    return (
        jsonify(
            {'message': 'Signature verification failed', 'error': 'invalid_token'}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                'description': 'Request does not contain an acces token',
                'error': 'authorization_required',
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {'description': 'The token is not fresh', 'error': 'fresh_token_required'}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {'description': 'The token has been revoked.', 'error': 'token_revoked'}
        ),
        401,
    )


api.add_resource(UserRegister, "/api/register")
api.add_resource(UserLogin, "/api/login")
api.add_resource(UserLogout, "/api/logout")
api.add_resource(TokenRefresh, '/api/refresh')
api.add_resource(User, "/api/user/<int:id>")
api.add_resource(UserList, "/api/users")

api.add_resource(AddTournament, "/api/add_tournament")
api.add_resource(Tournament, "/api/tournament/<int:id>")
api.add_resource(TournamentList, "/api/tournaments")



api.add_resource(JoinTournament, "/api/join/<int:user_id>/<int:tournament_id>")



api.add_resource(Score, "/api/score/<int:tournament_id>")
api.add_resource(DeleteMember, "/api/delete_member/<string:tournament_name>/<int:user_id>")
api.add_resource(TournamentPointsFirst, "/api/score/scores_first_round/<int:tournament_id>/<int:group1>")
api.add_resource(TournamentPointsSecond, "/api/score/scores_second_round/<int:tournament_id>/<int:group2>")
api.add_resource(TieBreakerFirst,
                 "/api/score/tie_breaker_first/<int:tournament_id>/<int:user_id>")
api.add_resource(TieBreakerSecond,
                 "/api/score/tie_breaker_second/<int:tournament_id>/<int:user_id>")
api.add_resource(ScoreTournamentList, "/api/scores/<int:tournament_id>")
api.add_resource(FirstRound, "/api/score/first_round/<int:tournament_id>")
api.add_resource(SecondRound, "/api/score/second_round/<int:tournament_id>")
api.add_resource(ThirdRound, "/api/score/third_round/<int:tournament_id>")

if __name__ == '__main__':
    db.init_app(app)
    app.run()
