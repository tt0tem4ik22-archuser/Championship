from random import random
from itertools import combinations


def championship(group):
    matches = list(combinations(group.keys(), 2))

    counter = {}

    for country in group:
        counter[country] = 0

    for match in matches:
        counter_={}

        for country in match:
            counter_[country] = 0

        p_teams = group[match[0]]/(group[match[0]]+group[match[1]])
        ran = random()
        if ran < p_teams:
            counter_[match[0]] += 1
        else:
            counter_[match[1]] += 1
        for team1, team2, *_ in [match]:
            team1s = counter_[team1]
            team2s = counter_[team2]
            if team1s > team2s:
                counter[team1] += 3
            elif team1s < team2s:
                counter[team2] += 3
            else:
                counter[team1] += 1
                counter[team2] += 1

    sorted_items = sorted(counter.items(), key=lambda item: item[1])
    winners = dict(sorted_items)
    
    wins = {}
    counter_ = 1

    for i in winners:
        wins[i] = counter_
        counter_ += 1   

    return wins


def count_center(group, iters):
    ships = []
    center = {}

    for country in group:
        center[country] = 0

    for i in range(iters):
        for country in (cship := championship(group)):
            score = cship[country]
            center[country] += score

    for country in center:
        score = center[country]
        center[country] = score / iters

    return center


def count_places(center):
    sorted_dict_asc = dict(sorted(center.items(), key=lambda item: item[1]))
    counter = 1
    places = []

    for i in list(sorted_dict_asc.keys())[::-1]:
        places.append({i: counter})
        counter += 1

    return places


def make_a_champion_ship(group, iters):
    center = count_center(group=group, iters=iters)
    ships = count_places(center=center)

    return ships


def count_places_for_championship(group_a, group_b, iters):
    ship_a = make_a_champion_ship(group_a, iters=iters)
    ship_b = make_a_champion_ship(group_b, iters=iters)

    candidates_a_ = ship_a[0:2]
    candidates_a = []
    for i in candidates_a_:
        candidates_a.append(list(i.keys()))

    candidates_b_ = ship_b[0:2]
    candidates_b = []
    for i in candidates_b_:
        candidates_b.append(list(i.keys()))

    candidates_c = candidates_a+candidates_b
    group_c = {}

    for country in candidates_c:
        country = country[0]
        for a in group_a:
            if country == a:
                group_c[country] = group_a[country]
        for b in group_b:
            if country == b:
                group_c[country] = group_b[country] 

    ship_c = make_a_champion_ship(group_c, iters)
    
    return list(ship_c[0].keys())[0], list(ship_c[1].keys())[0], list(ship_c[2].keys())[0]


def count_statistics(group_a, group_b, iters):
    first_ = {}
    second_ = {}
    third_ = {}

    for i in range(iters):
        first, second, third = count_places_for_championship(group_a, group_b, iters)
        if not first in list(first_.keys()):
            first_[first] = 1
        else: 
            first_[first] += 1
        if not second in list(second_.keys()):
            second_[second] = 1
        else: 
            second_[second] += 1
        if not third in list(third_.keys()):
            third_[third] = 1
        else: 
            third_[third] += 1

    return [first_, second_, third_]


def count_probability(group_a, group_b, iters):
    stat = count_statistics(group_a, group_b, iters)
    probs = [{} for i in stat]
    for i in range(len(stat)):
        for winner in stat[i]:
            probs[i][winner] = stat[i][winner]/iters
    return probs


def main():
    group_a = {
        "Франция": 85,
        "Австралия": 65,
        "Дания": 55,
        "Тунис": 20,
    }

    group_b = {
        "Германия": 85,
        "Япония": 65,
        "Коста-Рика": 55,
        "Испания": 85,
    }

    print("WARNING: calculations would take some time, please be patient")

    winner, final, medal = count_probability(group_a, group_b, 100)

    print("winner: ", winner, "\nfinal: ", final, "\nmedal: ", medal)


if __name__ == "__main__":
    main()