import argparse
from copy import deepcopy
import requests
import json
from prettytable import PrettyTable

def _get_data():
    resp = requests.get('http://worldcup.sfg.io/matches')
    return json.loads(resp.text)

def nice_date(date_string):
    split_data = date_string.split('-')
    year = int(split_data[0])
    month = int(split_data[1])
    day = int(split_data[2][0:2])
    return '%d-%d-%d' % (year, month, day)

def parse_args():
    parser = argparse.ArgumentParser(description='World Cup')
    subparser = parser.add_subparsers(dest='command')
    matches = subparser.add_parser('matches', help='Show all matches')
    matches.add_argument('--countries', nargs='+',
                         help='Show only games with specific countries')
    match = subparser.add_parser('match', help='Show one match')
    match.add_argument('match-num', type=int, help='Match to Show')
    records = subparser.add_parser('records', help='Show records')
    records.add_argument('--countries', nargs='+',
                         help='Show only records of certain countries')
    subparser.add_parser('upcomming', help='Show upcomming matches')
    return parser.parse_args()

def all_matches(countries):
    table = PrettyTable(['Match Num',
                         'Home Team', 'Home Goals',
                         'Away Team', 'Away Goals',
                         'Winner', 'Date'])
    table.padding_width = 1
    for game in _get_data():
        if game['status'] != 'future':
            number = game['match_number']
            home_team = game['home_team']['country']
            home_goals = game['home_team']['goals']
            away_team = game['away_team']['country']
            away_goals = game['away_team']['goals']
            if countries != None:
                skip = True
                if away_team in countries:
                    skip = False
                if home_team in countries:
                    skip = False
                if skip:
                    continue
            winner = game['winner']
            date = nice_date(game['datetime'])
            table.add_row([number,
                           home_team, home_goals,
                           away_team, away_goals,
                           winner, date])
    print table

def _add_goal(goal_table, event_dict, game_dict, team_type):
    player = event_dict['player']
    team = game_dict[team_type]['country']
    time = event_dict['time']
    goal_type = event_dict['type_of_event'].split('-')
    if len(goal_type) == 1:
        goal_type = 'regular'
    else:
        goal_type = goal_type[1]
    goal_table.add_row([team, player, time, goal_type])

def _add_card(card_table, event_dict, game_dict, team_type):
    player = event_dict['player']
    team = game_dict[team_type]['country']
    time = event_dict['time']
    card_type = event_dict['type_of_event'].split('-')[0]
    card_table.add_row([team, player, time, card_type])

def _add_sub(sub_table, event_dict, game_dict, team_type):
    player = event_dict['player']
    team = game_dict[team_type]['country']
    time = event_dict['time']
    sub_type = event_dict['type_of_event'].split('-')[1]
    sub_table.add_row([team, player, time, sub_type])

def show_match(match_num):
    basic_info = PrettyTable(['Home Team', 'Home Goals',
                              'Away Team', 'Away Goals',
                              'Winner', 'Date', 'Location'])
    goals = PrettyTable(['Team', 'Player', 'Time', 'Goal Type'])
    cards = PrettyTable(['Team', 'Player', 'Time', 'Card Type'])
    subs = PrettyTable(['Team', 'Player', 'Time', 'Sub Type'])
    for game in _get_data():
        if game['match_number'] == match_num:
            if game['status'] == 'future':
                print "Cant show you shit, game hasnt happened"
                return
            home_team = game['home_team']['country']
            home_goals = game['home_team']['goals']
            away_team = game['away_team']['country']
            away_goals = game['away_team']['goals']
            winner = game['winner']
            date = nice_date(game['datetime'])
            location = game['location']
            basic_info.add_row([home_team, home_goals,
                                away_team, away_goals,
                                winner, date, location])
            for i in game['home_team_events']:
                if 'goal' in i['type_of_event']:
                    _add_goal(goals, i, game, 'home_team')
                if 'card' in i['type_of_event']:
                    _add_card(cards, i, game, 'home_team')
                if 'sub' in i['type_of_event']:
                    _add_sub(subs, i, game, 'home_team')
            for i in game['away_team_events']:
                if 'goal' in i['type_of_event']:
                    _add_goal(goals, i, game, 'away_team')
                if 'card' in i['type_of_event']:
                    _add_card(cards, i, game, 'away_team')
                if 'sub' in i['type_of_event']:
                    _add_sub(subs, i, game, 'away_team')

    print 'Basic'
    print basic_info
    print 'Goals'
    print goals
    print 'Cards'
    print cards
    print 'Subs'
    print subs

def upcoming_matches():
    table = PrettyTable(['Away Team',
                         'Home Team',
                         'Date'])
    for game in _get_data():
        if game['status'] != 'completed':
            home_team = game['home_team']
            away_team = game['away_team']
            date = nice_date(game['datetime'])
            if isinstance(home_team, list):
                home_team = 'TBA'
            else:
                home_team = home_team['country']
            if isinstance(away_team, list):
                away_team = 'TBA'
            else:
                away_team = away_team['country']

            table.add_row([away_team, home_team, date])
    print table


def team_records(countries):
    records = dict()
    team_dict = {'Wins' : 0, 'Loses' : 0, 'Draws' : 0}
    for game in _get_data():
        if game['status'] == 'completed':
            home_team = game['home_team']['country']
            away_team = game['away_team']['country']
            records.setdefault(home_team, deepcopy(team_dict))
            records.setdefault(away_team, deepcopy(team_dict))
            if game['winner'] == home_team:
                records[home_team]['Wins'] += 1
                records[away_team]['Loses'] += 1
            if game['winner'] == away_team:
                records[home_team]['Loses'] += 1
                records[away_team]['Wins'] += 1
            if game['winner'] == 'Draw':
                records[home_team]['Draws'] += 1
                records[away_team]['Draws'] += 1
    table = PrettyTable(['Country', 'Wins', 'Loses', 'Draws', 'Points'])
    for team, results in records.iteritems():
        points = results['Wins'] * 3 + results['Draws']
        if countries != None:
            if team not in countries:
                continue
        table.add_row([team,
                       results['Wins'],
                       results['Loses'],
                       results['Draws'],
                       points])
    print table.get_string(sortby='Points', reversesort=True)

def main():
    args = vars(parse_args())
    if args['command'] == 'matches':
        all_matches(args['countries'])
    if args['command'] == 'match':
        show_match(args['match-num'])
    if args['command'] == 'records':
        team_records(args['countries'])
    if args['command'] == 'upcomming':
        upcoming_matches()
if __name__ == '__main__':
    main()
