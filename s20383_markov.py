from random import random, randrange
from unittest import result
import pandas as pd
import os
from IPython.display import display
import re


def getUserMove():
    user_move = ''
    while not (user_move == "N" or user_move == 'P' or user_move == 'K'):
        user_move = input("Please choose your move (P,K,N): ").upper()
    return user_move


def giveWinningMove(comp_move):
    win = {'K': 'P', 'P': 'N', 'N': 'K'}
    return win[comp_move]


def checkWhoWon(source):
    win = {'K': 'P', 'P': 'N', 'N': 'K'}
    if source[0] == source[1]:
        print("It's a draw!")
        return 0
    elif source[1] == win.get(source[0]):
        print('Not a surprise that I won')
        return -1
    else:
        print('I graciously let you win')
        return 1


def printScore(score):
    print('Score: ', score)
    if score > 0:
        print('Don\'t be ridiculous. You will fall soon')
    elif score < 0:
        print('Well I guess we are getting closer to our destiny')
    else:
        print('Back to beginning')


# main
df = pd.read_csv('s20383_markov_startModel.csv', sep=';')
print("How it started: ")
display(df)
win = 0
score = 0
while win < 3:
    win = int(input("Please set up to how many wins you play (not less than 3): "))
print("We play to ", win,
      " wins! Maybe this time I will play with someone who has brain.")
user_move = getUserMove()
wrt = randrange(0, 4)
comp_move = ''
if wrt == 0:
    comp_move = 'N'
elif wrt == 1:
    comp_move = 'P'
else:
    comp_move = 'K'
print("My great move is: ", comp_move)
source = user_move + comp_move
score = checkWhoWon(source)
printScore(score)
df.to_csv('s20383_markov_model.csv', sep=';', index=True)

# how read properly
while score < win and score > -win:
    df = pd.read_csv('s20383_markov_model.csv', sep=';', index_col=0)
    # display(df)
    # print(df.index)
    max_val = 0
    index_list = []
    for i in range(df[source].size):
        val = df[source][i].split("/")
        wrt = int(val[0])/int(val[1])
        if wrt == max_val:
            index_list.append(df.index[i])
        if wrt > max_val:
            max_val = wrt
            index_list.clear()
            index_list.append(df.index[i])
    if len(index_list) > 1:
        comp_move = index_list[randrange(0, len(index_list)-1)]
    else:
        comp_move = index_list[0]

    comp_move = giveWinningMove(comp_move[0])
    user_move = getUserMove()
    print("My great move is: ", comp_move)
    dest = user_move + comp_move
    score = score + checkWhoWon(dest)
    printScore(score)
    for col in df.columns:
        #print('col: ', col, 'dest: ', dest)
        val = df[col][dest].split('/')
        tmp1 = int(val[0])
        if col == source:
            tmp1 = tmp1 + 1
        tmp2 = str(int(val[1])+1)
        # print(str(tmp1)+"/"+tmp2)
        df[col][dest] = str(tmp1)+"/"+tmp2
    df.to_csv('s20383_markov_model.csv', sep=';', index=True)
    source = dest
if score < 0:
    print('Haha I won looser')
else:
    print("Well, maybe you have a few brain cells. I lost :(")

print("At the end:")
display(df)
