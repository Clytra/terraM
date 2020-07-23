USER:

Tabela users:
	id,
	username,
	password,
	first_name,
	last_name,
	phone_number,
	email


TOURNAMENT:
	
Tabela tournaments:
	id,
	tournament_name = nazwa turnieju. Może być ich więcej (pierwsze w tę niedzielę)
    user_id = relacja tabeli users i tournaments na podstawie id użytkownika
    user_fullname - imię i nazwisko  z tabeli users
    has_own_game = czy posiada swoją grę. Ma to znaczenie przy losowaniu stolików. Jeżeli uczestnik przynosi swoją grę, to już docelowo nie zmienia stolika w losowaniach
    end_terra = czy została w rundzie zakończona terraformacja. Jeśli tak, to dodaje się o punkt więcej w tzw. "duzych punktach"
    status = status zapisanego uczestnika. Do wyboru: uczestnik = 0, rezerwa = 1, rezygnacja = 2, dyskwalifikacja = 3
    group1 = numer stolika w pierwszej rundzie
    group2 = numer stolika w drugiej rundzie
    pz1 = liczba uzyskanych punktów
    pb1 = wartość dużych punktów - obliczane automatycznie, po wprowadzeniu pz1
    pz2 = liczba uzyskanych punktów z rundy drugiej
    pb2 = wartość dużych punktów - obliczane automatycznie, po wprowadzeniu pz2
    pz3 = liczba uzyskanych punktów w rundzie trzeciej
    tb1 = tie breaker 1
    tb2 = tie breaker 2
	
	
	
api.add_resource(Tournament, "/api/tournament/<string:tournament_name>")

Metody: GET - wyświetlenie turnieju po nazwie
PUT - edycja pól: tournament_name, has_own_game, end_terra, status, group1, group2, pz1, pz2, pz3


api.add_resource(AddTournament, "/api/add_tournament")

Metoda: POST 


api.add_resource(DeleteMember, "/api/remove_member/<int:id>")

Metoda: DELETE - usunięcie po numerze id użytkownika zapisanego w tabeli tournaments


api.add_resource(TournamentPointsFirst, "/api/tournament/scores_first_round/<string:tournament_name>/<int:group1>")

Metoda: PUT - dodanie "dużych punktów" (pb), w zależności od uzyskanych wyników PZ w rundzie pierwszej


api.add_resource(TournamentPointsSecond, "/api/tournament/scores_second_round/<string:tournament_name>/<int:group2>")

Metoda: PUT - to samo co wyżej, ale oblicza pb2 na podstawie wartości z pz2 (runda 2)


api.add_resource(TieBreakerFirst, "/api/tournament/tie_breaker_first/<string:tournament_name>/<int:group1>/<int:user_id>")

Metoda: PUT - oblizenie tie-breaker pierwszego rzędu

api.add_resource(TieBreakerSecond, "/api/tournament/tie_breaker_second/<string:tournament_name>/<int:group2>/<int:user_id>")

Metoda: PUT - obliczenie tie-breaker drugiego rzędu

api.add_resource(TournamentList, "/api/tournaments")

Metoda: GET = lista turniejów 

api.add_resource(FirstRound, "/api/tournament/first_round/<string:tournament_name>")

Metoda: PUT - obliczenie stolików dla pierwszej rundy na podstawie nazwy turnieju

api.add_resource(SecondRound, "/api/tournament/second_round/<string:tournament_name>")

Metoda: PUT - ta sama sytuacja co powyżej, ale dla drugiej rundy

api.add_resource(ThirdRound, "/api/tournament/third_round/<string:tournament_name>")

Metoda: PUT aktualizacja sumy PB, wyciągnięcie listy 5 najlepszych na podstawie następującej kolejności => najwyższa suma PB z dwóch rund, tie breaker 1 i tie breaker 2



api.add_resource(UserRegister, "/api/register")
api.add_resource(User, "/api/user/<int:id>")
api.add_resource(UserList, "/api/users")
api.add_resource(UserLogin, "/api/login")
api.add_resource(UserLogout, "/api/logout")
api.add_resource(TokenRefresh, '/api/refresh')
api.add_resource(CsvUpload, "/api/uploaddb") - nie zdążyłam tego zrobić. Także jeszcze nie działa, jak należy.