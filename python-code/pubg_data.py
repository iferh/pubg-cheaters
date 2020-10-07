import csv
from datetime import datetime
import numpy as np
import uuid


def main():
    pass


def get_cheaters_data():
    '''
    Opens "cheaters.txt" and returns all the data in an numpy array.
    Does not take any arguments.
    Returns a numpy.ndarray with the id of the cheaters as strings,
    and date of cheat and ban in datetime format.
    '''

    cheaters = []
    with open('../assignment-final-data/cheaters.txt', newline = '') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            row[1] = datetime.strptime(row[1], "%Y-%m-%d")
            row[2] = datetime.strptime(row[2], "%Y-%m-%d")
            cheaters.append(row)
        cheaters_array = np.array(cheaters)
        return cheaters_array


def get_kills_data():
    '''
    Opens "kills.txt" and returns all the data in a list of lists.
    Does not take any arguments.
    Returns a list of lists with match id, killer's and victim's id,
    the date of kill in datetime format and a unique id for the kill.
    '''

    kills = []
    with open('../assignment-final-data/kills.txt', newline = '') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            row.append(uuid.uuid4().hex)  # generate unique id for kill.
            row[3] = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f")
            kills.append(row)
        return kills


if __name__ == '__main__':
    main()
