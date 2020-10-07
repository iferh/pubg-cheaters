import numpy as np
import copy
import random
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter


def main():
    pass


def get_cheaters_set(cheaters_data):
    '''
    Returns a set of the cheater's accounts ids in cheaters data.
    Takes an array with the data of the cheaters as arguments.
    Returns a set with the ids of the cheaters as strings.
    '''

    cheaters_set = set([row[0] for row in cheaters_data])
    return cheaters_set


def get_cheat_kills_set(kills_data, cheaters_data):
    '''
    Returns a set of the ids of cheat kills in the kills data.
    Takes a list with the data of the kills and an array with
    the data of cheats as arguments.
    Returns a set with the ids of the kills as strings.
    '''

    cheaters_set = get_cheaters_set(cheaters_data)
    cheat_kills = set()
    for kill in kills_data:
        if kill[1] in cheaters_set:
            index = np.where(cheaters_data.T[:1] == kill[1])
            row = index[1][0]
            start_cheat = cheaters_data.T[1:2][0][row]
            if kill[3] - start_cheat > timedelta(days = 0):
                cheat_kills.add(kill[4])
    return cheat_kills


def get_cheat_matches_set(kills_data, cheat_kills_set):
    '''
    Returns a set of the matches with cheaters from the kills data.
    Takes a list with the data of the kills and a set with the data of
    cheat kills as arguments.
    Returns a set with the ids of the matches with cheaters on them.
    '''

    cheat_matches_set = set()
    for row in kills_data:
        if row[4] in cheat_kills_set:
            cheat_matches_set.add(row[0])
    return cheat_matches_set


def count_vc_motifs(kills_data, cheaters_data, cheat_kills_set):
    '''
    Counts the number of victim–cheater motifs in a kills dataset.
    Iterates over a dataset of kills and returns the victims of cheaters
    who become cheaters within 5 days of being killed by a cheater.
    Takes a list with the data of kills and an array of cheaters as arguments.
    Returns the number of victim–cheater motifs as an integer.
    '''

    cheaters_set = get_cheaters_set(cheaters_data)
    vc_motifs_set = set()
    for kill in kills_data:
        if kill[4] in cheat_kills_set and kill[2] in cheaters_set:
            index = np.where(cheaters_data.T[:1] == kill[2])
            row = index[1][0]
            start_cheat = cheaters_data.T[1:2][0][row]
            if timedelta(seconds = 0) < start_cheat - kill[3] <= timedelta(days = 5):
                vc_motifs_set.add(kill[2])
    return len(vc_motifs_set)


def get_kills_by_match(kills_data, cheat_matches_set):
    '''
    Returns the data of kills grouped by matches, but only of cheat matches.
    Takes a list with the data of kills and a set of cheat matches as arguments.
    Returns a list of matches with cheaters on them, each sub-list contains
    the data of kills for each match.
    '''

    kills_by_match = []
    kills_data_copy = copy.deepcopy(kills_data)
    kills_data = sorted(kills_data_copy, key = itemgetter(0))  # sort by match id.
    for key, group in groupby(kills_data_copy, key = lambda x: x[0]):
        if key in cheat_matches_set:
            kills_by_match.append(list(group))

    return kills_by_match


def get_players_set(kills_data):
    '''
    Returns a set of the players in the data.
    Takes a list with the data of kills as argument.
    Returns a set with the account id of each player.
    '''

    players = set([row[1] for row in kills_data])
    players_die = set([row[2] for row in kills_data])
    players.update(players_die)
    return players


def make_alt_universe(kills_by_match, cheat_kills_set):
    '''
    Makes a randomized alternative dataset of kills.
    Simulates an alternative world for each match, keeping the
    timing and structure of interactions but randomly assigning
    the identities of each non-cheater player within each match.
    Takes a list of the data of kills grouped by matches and
    a set of the cheat kills as arguments.
    Returns a list of lists with the alternative data of kills.
    '''

    kills_alt = []
    for match in kills_by_match:

        # Making a set of players in the match and removing cheaters.
        players = get_players_set(match)
        for row in match:
            if row[4] in cheat_kills_set and row[1] in players:
                players.remove(row[1])

        # Making a replacement dictionary for alternative universe.
        replace = list(players)
        random.shuffle(replace)  # randomizing position in game.
        replace_dic = {player:alt for (player,alt) in zip(players, replace)}

        # Making Alternative Universe for match.
        for row in match:
            if row[1] in players:
                row[1] = replace_dic[row[1]]
            if row[2] in players:
                row[2] = replace_dic[row[2]]

            # Appending the alternative kills to list.
            kills_alt.append(row)

    return kills_alt


def count_motifs_alt(kills_by_match, cheaters_data, cheat_kills_set, n):
    '''
    Counts the number of victim–cheater motifs in n alternative worlds.
    Returns the number of victims of cheaters who become cheaters within 5
    days of being killed by a cheater in n alternative randimized universes.
    Takes a list with the data of kills gropues by match, an array of
    cheaters, and a set of cheat kills as arguments.
    Returns a list with n number of victim–cheater motifs as integers.
    '''

    n_alt_univ = n
    motifs_alt_univ = []
    for i in range(n):
        kills_alt_univ = make_alt_universe(kills_by_match, cheat_kills_set)
        motifs_alt_univ.append(
            count_vc_motifs(kills_alt_univ, cheaters_data, cheat_kills_set))
    return motifs_alt_univ


if __name__ == '__main__':
    main()
