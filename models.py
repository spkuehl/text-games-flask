import random

next_player_id = 0

class Player(object):
    def __init__(self, name):
        global next_player_id
        self.name = name
        self.id = next_player_id
        next_player_id += 1

    def __str__(self):
        return self.name


class Prompt(object):
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

    def __str__(self):
        return self.word


prompt_list = [
    Prompt('dog', 'an animal'),
    Prompt('house', 'a place of living'),
    Prompt('doghouse', 'place of living for an animal')
]


class PlayerEntry(object):
    def __init__(self, player, score=0):
        self.player = player
        self.score = score

    def __repr__(self):
        return '{} {}'.format(self.player, self.score)


class Game(object):
    def __init__(self,round_limit=3):
        self.players = {}
        self.rounds = []
        self.round_limit = round_limit
        global prompt_list
        self.prompt_list = prompt_list
        self.complete = False

    def add_player(self, name):
        player = Player(name)
        self.players[player.id] = PlayerEntry(player, 0)

    def new_round(self):
        self.rounds.append(Round(game=self))


    def end_round(self):
        round = self.rounds[-1]
        print(round.entries)
        for entry in self.players.values():
            entry.score += round.entries[entry.player.id].votes

        if len(self.rounds) < self.round_limit:
            self.new_round()
        else:
            # Game is complete
            self.end_game()

    def end_game(self):
        return self.players.values()

    def __repr__(self):
        return self.players.values()


class Entry(object):
    def __init__(self, definition, votes=0):
        self.definition = definition
        self.votes = votes

    def __repr__(self):
        return '{} {}'.format(self.definition, self.votes)

class Round(object):
    def __init__(self, game, prompt=None):
        self.game = game
        if prompt == None:
            self.prompt = self.game.prompt_list.pop(random.randrange(
                len(self.game.prompt_list)))
        else:
            self.prompt = prompt
        self.entries = {
            None: Entry(self.prompt.definition)
        }
        self.options = []
        self.voting = False
        self.complete = False

    def add_entry(self, player, definition):
        self.entries[player.id] = Entry(definition)
        if len(self.entries) == len(self.game.players)+1:
            self.voting = True
            self.options = random.sample(
                list(self.entries.values()),
                len(self.entries))

    def add_vote(self, entry_index):
        entry = self.options[entry_index]
        for e in self.entries.values():
            if e.definition == entry.definition:
                e.votes +=1
        if sum([x.votes for x in self.entries.values()]) == len(
            self.game.players):
            self.complete = True

    # def __str__(self):
    #    return self.name
