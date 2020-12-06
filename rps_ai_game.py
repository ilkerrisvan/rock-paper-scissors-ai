# importing the libraries that we use

import random
import numpy as np
import math
import itertools
import time

choice = 0

rock_data = []
paper_data = []
scissors_data = []

next_move_rock = []
next_move_paper = []
next_move_scissors = []

## We keep the times of the moves in these lists.
player0_rock = []
player0_paper = []
player0_scissors = []

##ai move's times
player1_rock = []
player1_paper = []
player1_scissors = []

## move time
counter = 1

## counters for possible states
player0_won = 0
player1_won = 0
draw = 0

## for select mode ai vs user or ai vs comp
mode = int(input("which mode (1)user vs ai (2)comp vs ai"))

## how many times do you want
n_times = int(input("how many times do you want to play ?"))


## we use this method for compare the moves and get result.we can learn who is winner with this method.
def compare(counter, player0_rock, player0_paper, player0_scissors, player1_rock, player1_paper, player1_scissors) :
    global draw
    global player0_won
    global player1_won

    ## this conditions for get the winner side,these return boolean values
    rock_result_0 = counter in player0_rock
    rock_result_1 = counter in player1_rock

    paper_result_0 = counter in player0_paper
    paper_result_1 = counter in player1_paper

    scissors_result_0 = counter in player0_scissors
    scissors_result_1 = counter in player1_scissors

    ## we compare the couple result,we get winner side and number of their win,lose and so on.
    if rock_result_0 and rock_result_1 :
        print("DRAW")
        draw += 1
    if paper_result_0 and paper_result_1 :
        print("DRAW")
        draw += 1
    if scissors_result_0 and scissors_result_1 :
        print("DRAW")
        draw += 1

    if rock_result_0 and paper_result_1 :
        print("PLAYER AI WON")
        player1_won += 1
    if rock_result_0 and scissors_result_1 :
        print("PLAYER COMP/USER WON")
        player0_won += 1

    if paper_result_0 and scissors_result_1 :
        print("PLAYER AI WON")
        player1_won += 1
    if paper_result_0 and rock_result_1 :
        print("PLAYER COMP/USER WON")
        player0_won += 1

    if scissors_result_0 and rock_result_1 :
        print("PLAYER AI WON")
        player1_won += 1
    if scissors_result_0 and paper_result_1 :
        print("PLAYER COMP/USER WON")
        player0_won += 1

    return draw, player0_won, player1_won


def player0(counter) :
    global player0_rock
    global player0_paper
    global player0_scissors
    global choice

    ## if user play, user need to choice R,P or S
    if mode == 1 :
        choice_user = str(input("enter R,P or S  "))

        if choice_user == 'R' :
            choice = 1
        if choice_user == "P" :
            choice = 2
        if choice_user == "S" :
            choice = 3
            ## if comp play, comp will play randomly.
    if mode == 2 :
        choice = random.choice([1, 2, 3])

    if choice == 1 :
        player0_rock.append(counter)
    if choice == 2 :
        player0_paper.append(counter)
    if choice == 3 :
        player0_scissors.append(counter)
    ## exception case
    if choice < 1 or choice > 3 or choice == " " :
        print("select again")
        player0(counter)

    return choice, player0_rock, player0_paper, player0_scissors


## our ai player . ai player moves with using probability of rock,paper and scissors.
def player1(counter) :  ## counter as a paramter that used for time of move.
    if counter < 10 :  ## ai starts with 10 random moves so there is no enough data for move logical.
        choice = random.choice([1, 2, 3])
        if choice == 1 :
            player1_rock.append(counter)
        if choice == 2 :
            player1_paper.append(counter)
        if choice == 3 :
            player1_scissors.append(counter)
        print("draw,player,ai,#ofgame \n",
              compare(counter, player0_rock, player0_paper, player0_scissors, player1_rock, player1_paper, player1_scissors),
              counter)  ## show the result
    else :
        ## ai get the robability of rock,paper and scissors,and decide the move via a rule base system.
        prock = p_rock(player0_rock, counter)
        ppaper = p_paper(player0_paper, counter)
        pscissors = p_scissors(player0_scissors, counter)
        if prock > ppaper and prock > pscissors:
            if ppaper > pscissors :
                player1_paper.append(counter)
            if ppaper < pscissors :
                player1_rock.append(counter)
        if ppaper > prock and ppaper > pscissors :
            if pscissors > prock :
                player1_scissors.append(counter)
            if pscissors < prock :
                player1_paper.append(counter)
        if pscissors > ppaper and pscissors > prock :
            if prock > ppaper :
                player1_rock.append(counter)
            if prock < ppaper :
                player1_scissors.append(counter)
        print(prock, ppaper, pscissors)  ## we can check the probability of rock,paper and scissors.
        ## if you want to show results step by step you can use these several prints.
        """ 
        print(player0_rock)
        print(player0_paper)
        print(player0_scissors)
        print(player1_rock)
        print(player1_paper)
        print(player1_scissors)
                                """

        print("draw,player,ai,#ofgame \n",
              compare(counter, player0_rock, player0_paper, player0_scissors, player1_rock, player1_paper, player1_scissors),
              counter)  ## shot the result

    return player1_rock, player1_paper, player1_scissors



# We used Naive Bayes Classification to calculate probability of the moves according to the our previous datas
# https://en.wikipedia.org/wiki/Naive_Bayes_classifier
""" 
With this mathematical function,
we are trying to calculate what the next move will be with the previously played data 
by making a naive bayes classification.
"""


def p_rock(rock_data, counter) :
    var_rock = np.var(rock_data, ddof=1)
    mean_rock = np.mean(rock_data)
    p_rock = abs((1 / math.sqrt(2 * math.pi * var_rock)) * math.exp(- pow((counter - mean_rock), 2) / abs((2 * var_rock))))
    return p_rock


def p_paper(paper_data, counter) :
    var_paper = np.var(paper_data, ddof=1)
    mean_paper = np.mean(paper_data)
    p_paper = abs(
        (1 / math.sqrt(2 * math.pi * var_paper)) * math.exp(- pow((counter - mean_paper), 2) / abs((2 * var_paper))))
    return p_paper


def p_scissors(scissors_data, counter) :
    var_scissors = np.var(scissors_data, ddof=1)
    mean_scissors = np.mean(scissors_data)
    p_scissors = abs(
        (1 / math.sqrt(2 * math.pi * var_scissors)) * math.exp(- pow((counter - mean_scissors), 2) / abs((2 * var_scissors))))
    return p_scissors


## counter must be bigger than zero for play the game and it must be smaller than n_times(how many time you want to play?)
while counter > 0 and counter <= n_times :
    player0(counter)
    player1(counter)
    counter += 1

if (player1_won > player0_won):
    print("* AI WON THE GAME *")
if (player0_won > player1_won):
    print("* COMP/USER WON THE GAME *")
