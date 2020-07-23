from db import db
from sqlalchemy import desc, asc
import enum

class StatusEnum(enum.Enum):
    oczekujący = 0,
    uczestnik = 1,
    rezerwa = 2,
    rezygnacja = 3,
    dyskwalifikacja = 4

class ScoreModel(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'scores'

    id = db.Column(db.Integer(), primary_key=True)
    has_own_game = db.Column(db.Boolean, default=False, server_default='false')
    end_terra_first = db.Column(db.Boolean, default=False, server_default='false')
    end_terra_second = db.Column(db.Boolean, default=False, server_default='false')
    status = db.Column(db.Enum(StatusEnum), default='oczekujący')
    group1 = db.Column(db.Integer())
    group2 = db.Column(db.Integer())
    pz1 = db.Column(db.Integer())
    pz2 = db.Column(db.Integer())
    pz3 = db.Column(db.Integer())
    pb1 = db.Column(db.Integer())
    pb2 = db.Column(db.Integer())
    pb_sum = db.Column(db.Integer())
    tb1 = db.Column(db.Integer())
    tb2 = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    def __init__(self, has_own_game: bool, end_terra_first: bool, end_terra_second: bool, status: enumerate,
                 group1: int, group2: int, pz1: int, pz2: int, pz3: int, pb1: int, pb2: int, pb_sum: int,
                 tb1: int, tb2: int, user_id: int, tournament_id: int):
        self.has_own_game = has_own_game
        self.end_terra_first = end_terra_first
        self.end_terra_second = end_terra_second
        self.status = status
        self.group1 = group1
        self.group2 = group2
        self.pz1 = pz1
        self.pz2 = pz2
        self.pz3 = pz3
        self.pb1 = pb1
        self.pb2 = pb2
        self.pb_sum = pb_sum
        self.tb1 = tb1
        self.tb2 = tb2
        self.user_id = user_id
        self.tournament_id = tournament_id

    def json(self):
        return {
            'id': self.id, 'has_own_game': self.has_own_game, 'end_terra_first': self.end_terra_first,
            'end_terra_second': self.end_terra_second, 'group1': self.group1,
            'group2': self.group2, 'pz1': self.pz1, 'pz2': self.pz2, 'pz3': self.pz3, 'pb1': self.pb1,
            'pb2': self.pb2, 'tb1': self.tb1, 'tb2': self.tb2, 'user_id': self.user_id,
            'tournament_id': self.tournament_id
        }

    @classmethod
    def find_by_id(cls, user_id, tournament_id):
        return cls.query.filter_by(user_id=user_id, tournament_id=tournament_id).first()

    @classmethod
    def find_all(cls, tournament_id):
        return cls.query.filter_by(tournament_id=tournament_id).order_by(desc(cls.id)).all()

    @classmethod
    def get_all_members(cls, tournament_id):
        return cls.query.filter_by(tournament_id=tournament_id, status='uczestnik').order_by(
            desc(cls.has_own_game)).all()

    @classmethod
    def get_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_finalists(cls, tournament_id):
        return cls.query.filter_by(tournament_id=tournament_id).order_by(desc(cls.pb_sum), desc(cls.tb1), desc(cls.tb2)).all()

    @classmethod
    def second_round(cls, tournament_id):
        return cls.query.filter_by(tournament_id=tournament_id, status='uczestnik').order_by(asc(cls.group1),
                                                                                                 desc(cls.pz1)).all()

    @classmethod
    def get_group2(cls, tournament_id):
        return cls.query.filter_by(tournament_id=tournament_id, status='uczestnik').order_by(desc(cls.pb1)).all()

    @classmethod
    def get_group2_acs(cls, tournament_id):
        return cls.query.filter_by(tournament_id=tournament_id, status='uczestnik').order_by(asc(cls.pz1)).all()

    @classmethod
    def get_number_of_tables(cls, number, tournament):
        if number % 5 == 0:
            groups = number // 5
            for x in range(0, groups):
                for y in range(0, number - 1, groups):
                    tournament[y + x].group1 = x + 1
            return tournament
        if number % 4 == 0:
            groups = number // 4
            for x in range(0, groups):
                for y in range(0, number - 1, groups):
                    tournament[y + x].group1 = x + 1
            return tournament
        # 4 stoliki 4-os., reszta 5-os.
        if number % 5 == 1 and number % 5 != 0 & number != 11:
            temp = (number - 16) // 5
            groups = temp + 4
            for n in range(0, 4):
                for z in range(number - 16, number - 1, 4):
                    tournament[n + z].group1 = (groups - 3) + n
            for x in range(0, groups - 4):
                for y in range(0, number - 17, temp):
                    tournament[y + x].group1 = x + 1
            return tournament
        # 3 stoliki 4-os, reszta 5-os
        if number % 5 == 2 and number % 4 != 0:
            temp = (number - 12) // 5
            groups = temp + 3
            for n in range(0, 3):
                for z in range(number - 12, number - 1, 3):
                    tournament[n + z].group1 = (groups - 2) + n
            for x in range(0, groups - 3):
                for y in range(0, number - 13, temp):
                    tournament[y + x].group1 = x + 1
            return tournament
        # 2 stoliki 4-os, reszta 5-os
        if number % 5 == 3 and number % 4 != 0:
            temp = (number - 8) // 5
            groups = temp + 2
            for n in range(0, 2):
                for z in range(number - 8, number - 1, 2):
                    tournament[n + z].group1 = (groups - 1) + n
            for x in range(0, groups - 2):
                for y in range(0, number - 9, temp):
                    tournament[y + x].group1 = x + 1
            return tournament
        # 1 stolik 4-os. reszta 5-os.
        if number % 5 == 4 and number % 4 != 0:
            temp = (number - 4) // 5
            groups = temp + 1
            for n in range(0, 1):
                for z in range(number - 4, number, 1):
                    tournament[n + z].group1 = groups + n
            for x in range(0, groups - 1):
                for y in range(0, number - 5, temp):
                    tournament[y + x].group1 = x + 1
            return tournament

    @classmethod
    def get_number_of_tables2(cls, number, tournament, groups2):
        k = 0
        if number % 5 == 0:
            for x in range(0, number, 5):
                k += 1
                if k in groups2:
                    for y in range(0, 4):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
                else:
                    for y in range(0, 5):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
            return tournament
        if number % 4 == 0:
            for x in range(0, number, 4):
                k += 1
                if k in groups2:
                    for y in range(0, 3):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
                else:
                    for y in range(0, 4):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
            return tournament
        # 4 stoliki 4-os., reszta 5-os.
        if number % 5 == 1 and number % 5 != 0 & number != 11:
            k += 1
            for x in range(0, 12, 4):
                if k in groups2:
                    for y in range(0, 3):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
                    k += 1
                else:
                    for n in range(0, 4):
                        if tournament[x + n].group2 is not None:
                            tournament[x + n + 1].group2 = k
                        else:
                            tournament[x + n].group2 = k
                    k += 1
            for l in range(13, number - 1, 5):
                if k in groups2:
                    for y in range(0, 4):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
                else:
                    for y in range(0, 5):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
            return tournament
        # 3 stoliki 4-os, reszta 5-os
        if number % 5 == 2 and number % 4 != 0:
            k += 1
            for x in range(0, 9, 4):
                if k in groups2:
                    for y in range(0, 3):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
                    k += 1
                else:
                    for n in range(0, 4):
                        if tournament[x + n].group2 is not None:
                            tournament[x + n + 1].group2 = k
                        else:
                            tournament[x + n].group2 = k
                    k += 1
            for l in range(10, number - 1, 5):
                if k in groups2:
                    for y in range(0, 4):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
                else:
                    for y in range(0, 5):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
            return tournament
        # 2 stoliki 4-os, reszta 5-os
        if number % 5 == 3 and number % 4 != 0:
            k += 1
            for x in range(0, 6, 4):
                if k in groups2:
                    for y in range(0, 3):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
                    k += 1
                else:
                    for n in range(0, 4):
                        if tournament[x + n].group2 is not None:
                            tournament[x + n + 1].group2 = k
                        else:
                            tournament[x + n].group2 = k
                    k += 1
            for l in range(7, number - 1, 5):
                if k in groups2:
                    for y in range(0, 4):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
                else:
                    for y in range(0, 5):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
            return tournament
        # 1 stolik 4-os. reszta 5-os.
        if number % 5 == 4 and number % 4 != 0:
            k += 1
            for x in range(0, 3, 4):
                if k in groups2:
                    for y in range(0, 3):
                        if tournament[x + y].group2 is not None:
                            tournament[x + y + 1].group2 = k
                        else:
                            tournament[x + y].group2 = k
                    k += 1
                else:
                    for n in range(0, 4):
                        if tournament[x + n].group2 is not None:
                            tournament[x + n + 1].group2 = k
                        else:
                            tournament[x + n].group2 = k
                    k += 1
            for l in range(4, number - 1, 5):
                if k in groups2:
                    for y in range(0, 4):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
                else:
                    for y in range(0, 5):
                        if tournament[l + y].group2 is not None:
                            tournament[l + y + 1].group2 = k
                        else:
                            tournament[l + y].group2 = k
                    k += 1
            return tournament

    @classmethod
    def get_group(cls, tournament_id, group1):
        return cls.query.filter_by(tournament_id=tournament_id, group1=group1, status='uczestnik').order_by(
            desc(cls.pz1)).all()

    @classmethod
    def get_points(cls, tournament_id, group2):
        return cls.query.filter_by(tournament_id=tournament_id, group2=group2, status='uczestnik').order_by(
            desc(cls.pz2)).all()

    @classmethod
    def add_pb1(cls, tournament):
        number = len(tournament)
        n = 0
        if tournament[n].end_terra_first and number is 5:
            tournament[n].pb1 = 7
            tournament[n + 1].pb1 = 5
            tournament[n + 2].pb1 = 3
            tournament[n + 3].pb1 = 2
            tournament[n + 4].pb1 = 1
            return tournament
        if tournament[n].end_terra_first and number is 4:
            tournament[n].pb1 = 7
            tournament[n + 1].pb1 = 5
            tournament[n + 2].pb1 = 3
            tournament[n + 3].pb1 = 2
            return tournament
        if tournament[n].end_terra_first is False and number is 5:
            tournament[n].pb1 = 6
            tournament[n + 1].pb1 = 4
            tournament[n + 2].pb1 = 2
            tournament[n + 3].pb1 = 1
            tournament[n + 4].pb1 = 0
            return tournament
        if tournament[n].end_terra_first is False and number is 4:
            tournament[n].pb1 = 6
            tournament[n + 1].pb1 = 4
            tournament[n + 2].pb1 = 2
            tournament[n + 3].pb1 = 1
            return tournament

    @classmethod
    def add_pb2(cls, tournament):
        number = len(tournament)
        n = 0
        if tournament[n].end_terra_second and number is 5:
            tournament[n].pb2 = 7
            tournament[n + 1].pb2 = 5
            tournament[n + 2].pb2 = 3
            tournament[n + 3].pb2 = 2
            tournament[n + 4].pb2 = 1
            return tournament
        if tournament[n].end_terra_second and number is 4:
            tournament[n].pb2 = 7
            tournament[n + 1].pb2 = 5
            tournament[n + 2].pb2 = 3
            tournament[n + 3].pb2 = 2
            return tournament
        if tournament[n].end_terra_second is False and number is 5:
            tournament[n].pb2 = 6
            tournament[n + 1].pb2 = 4
            tournament[n + 2].pb2 = 2
            tournament[n + 3].pb2 = 1
            tournament[n + 4].pb2 = 0
            return tournament
        if tournament[n].end_terra_second is False and number is 4:
            tournament[n].pb2 = 6
            tournament[n + 1].pb2 = 4
            tournament[n + 2].pb2 = 2
            tournament[n + 3].pb2 = 1
            return tournament

    @classmethod
    def pb_summary(cls, sumPoints):
        for row in sumPoints:
            row.pb_sum = row.pb1 + row.pb2
        return sumPoints

    @classmethod
    def add_tie_breaker1(cls, tournament, user, user_id):
        # trzeba jeszcze dodać logikę do dodania 1 pkt, jeżeli ktoś zrezygnuje itp.
        tb = 0
        user_gr1 = user.group1
        user_gr2 = user.group2
        group1 = []
        group2 = []
        for row in tournament:
            if row.group1 == user_gr1 and row.pb1 is not 0:
                if row.user_id != user_id:
                    group1.append(row)
            if row.group2 == user_gr2 and row.pb2 is not 0:
                if row.user_id != user_id:
                    group2.append(row)
        for x in group1:
            tb += x.pb2
        for y in group2:
            tb += y.pb1
        for row in tournament:
            if row.user_id == user_id:
                row.tb1 = tb
        return tournament

    @classmethod
    def add_second_tie_breaker(cls, tournament, user, user_id):
        pz = 0
        user_pb2 = user.pb2
        user_gr2 = user.group2
        pznb = 0
        pzmb = 0
        for row in tournament:
            if user_pb2 == 0 and row.group2 == user_gr2:
                pzmb += row.pz2
            else:
                if row.group2 == user_gr2 and row.pb2 is not 0:
                    pz += row.pz2
                    if row.pb2 < user_pb2:
                        pznb += row.pz2
                    if row.pb2 > user_pb2:
                        pzmb += row.pz2
        pzn = (pznb / pz) * 100
        pzm = (pzmb / pz) * 100
        tb = pzn - pzm
        for row in tournament:
            if row.user_id == user_id:
                row.tb2 = tb
        return tournament

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_row(self):
        db.session.update(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()