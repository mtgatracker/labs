""" sim_quick_explore.py: perform quick explore payout simulations to determine if matchmaking affects WotC "profit."
author: Spencatro

Turns out this wasn't all the interesting. There was a minute where I wondered if the 2 wins / 2 losses event
structure incentivized WotC to make unfair matches (pair losers with winners, etc). That doesn't seem to be the case.

I suppose the data around "profit" might be interesting on it's own, but this experiment was otherwise
pretty much a failure.
"""

import random
# optional: line_profiler helps fix slow code! see:
# https://github.com/rkern/line_profiler
# import line_profiler

class EventEntry(object):
    def __init__(self):
        self.record = []
        self.available = True

    @property
    def wins(self):
        return self.record.count("W")

    @property
    def losses(self):
        return self.record.count("L")

    def update_available(self):
        record_length = len(self.record)
        if record_length > 2:
            self.available = False
        elif record_length == 2 and self.record[0] == self.record[1]:
            self.available = False
        else:
            self.available = True

    def win(self):
        self.record.append("W")
        self.update_available()

    def lose(self):
        self.record.append("L")
        self.update_available()

def match_available(population):
    # clever, but slow
    # return sum(1 for event in population if event.available) > 1
    count = 0
    for event in population:
        if event.available:
            count += 1
        if count > 1:
            return True

def sim_match_first_always_wins(p1, p2):
    p1.win()
    p2.lose()

def sim_match_random(p1, p2):
    coin_toss = random.randint(0,1)
    if coin_toss:
        p1.win()
        p2.lose()
    else:
        p1.lose()
        p2.win()


def gen_next_match_pick_randomly(population):
    """ Decides next two player indexes who will play against each other by randomly selecting two players
    from the list of players available"""
    available_players = [player for player in population if player.available]

    p1 = random.choice(available_players)
    available_players.remove(p1)
    p2 = random.choice(available_players)
    return p1, p2


def get_next_match_pick_first_available(population):
    """ Decides next two player indexes who will play against each other next, iterating over the list
    and picking the very first available"""
    p1 = None
    for player in population:
        if player.available:
            if p1 is not None:
                return p1, player
            else:
                p1 = player


def get_next_match_prefer_fair_matches(population):
    """ Decides next two player indexes who will play against each other next by sorting players into
    win/loss buckets, then picking from the most restrictive buckets available first"""
    both_bucket = [player for player in population if player.available and len(player.record) == 2]
    if len(both_bucket) > 1:
        return both_bucket[0], both_bucket[1]
    win_bucket = [player for player in population if len(player.record) == 1 and player.record[0] == "W"]
    if len(win_bucket) > 1:
        return win_bucket[0], win_bucket[1]
    loss_bucket = [player for player in population if len(player.record) == 1 and player.record[0] == "L"]
    if len(loss_bucket) > 1:
        return loss_bucket[0], loss_bucket[1]
    # if we can't find a fair match, just pick the first available
    return get_next_match_pick_first_available(population)


def get_next_match_prefer_unfair_matches(population):
    """ Decides next two player indexes who will play against each other next by trying to match a player who has
    won with a player who has lost"""
    win_player = None
    loss_player = None
    for player in population:
        if len(player.record) == 1:
            if player.record[0] == "W":
                win_player = player
            elif player.record[0] == "L":
                loss_player = player
        if win_player and loss_player:
            return win_player, loss_player
    # if we can't find an unfair match, just pick the first available
    return get_next_match_pick_first_available(population)


def run_sim(population_size, match_sim_func, next_match_func, verbose=False):

    player_population = [EventEntry() for i in range(population_size)]
    while match_available(player_population):
        next_match = next_match_func(player_population)
        if next_match:
            match_sim_func(*next_match)
        else:  # sometimes someone won't get to finish their match. oh well
            break

    total_gold_spent = 0
    total_gold_rewarded = 0
    total_packs_rewarded = 0
    total_icrs_rewarded = 0
    unmatched_players = [player for player in player_population if player.available]

    for player in player_population:
        total_gold_spent += 600
        if player.wins == 2:
            total_packs_rewarded += 1
            total_gold_rewarded += 100
        elif player.wins == 1:
            total_gold_rewarded += 100
            total_icrs_rewarded += 1
        else:
            total_gold_rewarded += 50
            total_icrs_rewarded += 1

    if verbose:
        print("Sim results:")
        print("Total gold spent by players: {}".format(total_gold_spent))
        print("Total gold rewarded:         {}".format(total_gold_rewarded))
        print("Total packs rewarded:        {}".format(total_packs_rewarded))
        print("Total icr's rewarded:        {}".format(total_icrs_rewarded))
    return player_population, total_gold_spent, total_gold_rewarded, total_packs_rewarded, total_icrs_rewarded, unmatched_players


num_iterations = 10000
population_size = 100
matchmaking_algorithm = get_next_match_prefer_unfair_matches
match_sim_algorithm = sim_match_random


print("Simulation: {} iterations with population size {}".format(num_iterations, population_size))
print("Matchmaking algorithm: " + matchmaking_algorithm.__name__)
print("Matchmaking algorithm: " + match_sim_algorithm.__name__)
print("-------------------------------------------------------")

total_gold_spent = 0
total_gold_rewarded = 0
total_packs_rewarded = 0
total_icrs_rewarded = 0
total_unmatched_players = 0

for i in range(num_iterations):
    player_population_i, total_gold_spent_i, total_gold_rewarded_i, total_packs_rewarded_i, total_icrs_rewarded_i, unmatched_players_i = run_sim(population_size, match_sim_algorithm, matchmaking_algorithm)
    total_gold_spent += total_gold_spent_i
    total_gold_rewarded += total_gold_rewarded_i
    total_packs_rewarded += total_packs_rewarded_i
    total_icrs_rewarded += total_icrs_rewarded_i
    total_unmatched_players += len(unmatched_players_i)

print("Average total gold spent:             {}".format(total_gold_spent / float(num_iterations)))
print("Average total gold rewarded:          {}".format(total_gold_rewarded / float(num_iterations)))
print("Average total gold rewarded / entry:  {}".format(total_gold_rewarded / float(num_iterations * population_size)))
print("Average total packs rewarded / entry: {}".format(total_packs_rewarded / float(num_iterations * population_size)))
print("Average total icr's rewarded / entry: {}".format(total_icrs_rewarded / float(num_iterations * population_size)))
print('Average WotC "profit" (gold):         {}'.format((total_gold_spent - total_gold_rewarded - (1000 * total_packs_rewarded)) / float(num_iterations)))
print("-------------------------------------------------------")
print("Average total unmatched players:      {}".format(total_unmatched_players / float(num_iterations)))
