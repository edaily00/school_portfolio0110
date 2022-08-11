class Player:

    def __init__(self):
        self._start_place = None
        self._end_place = None
        self._p_position = "H"
        self._q_position = "H"
        self._player_state = "Playing"
        self._p_steps = -1
        self._q_steps = -1
        self._is_stacked = False
        self._final_steps = []

    def set_player_state(self, state):
        self._player_state = state

    def get_completed(self):
        if self._player_state != "Playing":
            return True
        else:
            return False

    def set_p_step_count(self, steps):
        self._p_steps = steps

    def add_p_step_count(self, steps):
        self._p_steps += steps

    def get_token_p_step_count(self):
        return self._p_steps

    def set_q_step_count(self, steps):
        self._q_steps = steps

    def add_q_step_count(self, steps):
        self._q_steps += steps

    def get_token_q_step_count(self):
        return self._q_steps

    def get_space_name(self, steps):
        if steps == -1:
            return "H"
        elif steps == 0:
            return "R"
        elif steps > 0 and steps <= 50:
            if self._start_place + steps > 56:
                return str(self._start_place + steps - 56)
            else:
                return str(self._start_place + steps)
        elif steps > 50:
            index = steps - 51
            return self._final_steps[index]

    def get_stacked(self):
        return self._is_stacked

    def set_stacked_true(self):
        self._is_stacked = True

    def set_stacked_false(self):
        self._is_stacked = False

    def get_start_space(self):
        return self._start_place

    def get_end_space(self):
        return self._end_place

    def set_p_position(self, pos):
        self._p_position = pos

    def get_p_position(self):
        return self._p_position

    def set_q_position(self, pos):
        self._q_position = pos

    def get_q_position(self):
        return self._q_position


class PlayerA(Player):

    def __init__(self):
        super().__init__()
        self._start_place = 0
        self._end_place = 50
        self._final_steps = ["A1", "A2", "A3", "A4", "A5", "A6", "E"]


class PlayerB(Player):

    def __init__(self):
        super().__init__()
        self._start_place = 14
        self._end_place = 8
        self._final_steps = ["B1", "B2", "B3", "B4", "B5", "B6", "E"]


class PlayerC(Player):

    def __init__(self):
        super().__init__()
        self._start_place = 28
        self._end_place = 22
        self._final_steps = ["C1", "C2", "C3", "C4", "C5", "C6", "E"]


class PlayerD(Player):

    def __init__(self):
        super().__init__()
        self._start_place = 42
        self._end_place = 36
        self._final_steps = ["D1", "D2", "D3", "D4", "D5", "D6", "E"]


class LudoGame:

    def __init__(self):
        self._players = {}

    def get_player_by_position(self, position):
        for players in self._players:
            if players.lower() == position.lower():
                return self._players[players]

        return "Player not found!"

    def determine_kick(self, player, steps):
        # if starting back at home and someone is in front of them

        if player.get_token_p_step_count() >= 0:
            p_pos = player.get_start_space() + player.get_token_p_step_count() + steps
        else:
            p_pos = -1
        if player.get_token_q_step_count() >= 0:
            q_pos = player.get_start_space() + player.get_token_q_step_count() + steps
        else:
            q_pos = -1

        for other in self._players:
            other_player = self._players[other]
            if player is not other_player:
                other_p_position = other_player.get_space_name(other_player.get_token_p_step_count())
                other_q_position = other_player.get_space_name(other_player.get_token_q_step_count())
                if p_pos == other_p_position or p_pos == other_q_position:
                    return "p"
                elif q_pos == other_p_position or q_pos == other_q_position:
                    return "q"
        return


    def move_token(self, player, token, steps):

        finish_space = 57

        if player.get_stacked() is True:
            player.add_p_step_count(steps)
            player.add_q_step_count(steps)
            if player.get_token_p_step_count() > finish_space:
                new_steps = player.get_token_p_step_count() - finish_space
                player.set_p_step_count(finish_space - new_steps)
                player.set_q_step_count(finish_space - new_steps)
                return
            elif player.get_token_p_step_count() == finish_space:
                player.set_p_position("E")
                player.set_q_position("E")
            player_position = player.get_space_name(player.get_token_p_step_count())
            for other in self._players:
                other_player = self._players[other]
                if player is not other_player:
                    other_p_position = other_player.get_space_name(other_player.get_token_p_step_count())
                    other_q_position = other_player.get_space_name(other_player.get_token_q_step_count())
                    if player_position == other_p_position:
                        if other_player.get_stacked() is True:
                            other_player.set_stacked_false()
                            other_player.set_q_step_count(-1)
                        other_player.set_p_step_count(-1)
                    elif player_position == other_q_position:
                        other_player.set_q_step_count(-1)


        elif token == "p":
            player.add_p_step_count(steps)
            if player.get_token_p_step_count() > finish_space:
                new_steps = player.get_token_p_step_count() - finish_space
                player.set_p_step_count(finish_space - new_steps)
                return
            elif player.get_token_p_step_count() == finish_space:
                player.set_p_position("E")
                return

            player_position = player.get_space_name(player.get_token_p_step_count())
            player_q_position = player.get_space_name(player.get_token_q_step_count())

            if player_position == player_q_position:
                player.set_stacked_true()

            if 0 < player.get_token_p_step_count() < 51:
                player_position = player.get_space_name(player.get_token_p_step_count())

                for other in self._players:
                    other_player = self._players[other]
                    if player is not other_player:
                        other_p_position = other_player.get_space_name(other_player.get_token_p_step_count())
                        other_q_position = other_player.get_space_name(other_player.get_token_q_step_count())
                        if player_position == other_p_position:
                            if other_player.get_stacked() is True:
                                other_player.set_stacked_false()
                                other_player.set_q_step_count(-1)
                            other_player.set_p_step_count(-1)
                        elif player_position == other_q_position:
                            other_player.set_q_step_count(-1)



        elif token == "q":
            player.add_q_step_count(steps)
            if player.get_token_q_step_count() > finish_space:
                new_steps = player.get_token_q_step_count() - finish_space
                player.set_q_step_count(finish_space - new_steps)
                return
            elif player.get_token_q_step_count == finish_space:
                player.set_q_position("E")
                return

            player_position = player.get_space_name(player.get_token_q_step_count())
            player_p_position = player.get_space_name(player.get_token_p_step_count())

            if player_position == player_p_position:
                player.set_stacked_true()

            if 0 < player.get_token_q_step_count() < 51:
                player_position = player.get_space_name(player.get_token_q_step_count())

                for other in self._players:
                    other_player = self._players[other]
                    if player is not other_player:
                        other_p_position = other_player.get_space_name(other_player.get_token_p_step_count())
                        other_q_position = other_player.get_space_name(other_player.get_token_q_step_count())
                        if player_position == other_p_position:
                            if other_player.get_stacked() is True:
                                other_player.set_stacked_false()
                                other_player.set_q_step_count(-1)
                            other_player.set_p_step_count(-1)
                        elif player_position == other_q_position:
                            other_player.get_token_q_step_count(-1)


    def decision_making(self, player, roll):

        p_pos = player.get_space_name(player.get_token_p_step_count())
        p_steps = player.get_token_p_step_count()
        q_pos = player.get_space_name(player.get_token_q_step_count())
        q_steps = player.get_token_q_step_count()
        finish_space = 57
        p_loc = player.get_p_position()
        q_loc = player.get_q_position()

        if player.get_token_p_step_count() > 0 and p_loc != "E":
            if p_steps + roll == finish_space:
                self.move_token(player, "p", roll)
                return

        elif player.get_token_q_step_count() > 0 and q_loc != "E":
            if q_steps + roll == finish_space:
                self.move_token(player, "q", roll)
                return

        if roll == 6:
            if player.get_token_p_step_count() == -1 and p_loc != "E":
                self.move_token(player, "p", 1)
                return
            elif player.get_token_q_step_count() == -1 and q_loc != "E":
                self.move_token(player, "q", 1)
                return

        if p_pos == "H" and q_pos == "H":
            return

        answer = self.determine_kick(player, roll)
        if answer == "p" and p_loc != "E":
            self.move_token(player, "p", roll)
            return

        if answer == "q" and q_loc != "E":
            self.move_token(player, "q", roll)
            return

        if p_pos != "H" and p_loc != "E":
            if p_steps <= q_steps or q_pos == "H":
                self.move_token(player, "p", roll)
                return
        if q_pos != "H" and q_loc != "E":
            self.move_token(player, "q", roll)

    def play_game(self, player_list, turn_list):
        for player in player_list:
            if player.lower() == "A".lower():
                p = PlayerA()
            elif player.lower() == "B".lower():
                p = PlayerB()
            elif player.lower() == "C".lower():
                p = PlayerC()
            elif player.lower() == "D".lower():
                p = PlayerD()
            self._players[player] = p

        for turn in turn_list:

            player = self.get_player_by_position(turn[0])
            roll = turn[1]
            #print("P: " + str(player.get_token_p_step_count()))
            #print("Q: " + str(player.get_token_q_step_count()))
            if player.get_completed() is True:
                return
            else:
                self.decision_making(player, roll)
                if player.get_p_position() == "E" and player.get_q_position() == "E":
                    player.set_player_state("Done")

        positions = []
        for player in self._players:
            player = self.get_player_by_position(player)
            positions.append(player.get_space_name(player.get_token_p_step_count()))
            positions.append(player.get_space_name(player.get_token_q_step_count()))

        return positions


players = ['A','B']
turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 6),('A', 5),('A', 3),('B', 6),('B', 2),('A', 2),('A', 4)]
new = LudoGame()

current = new.play_game(players, turns)



print(current)

