import json
import argparse

parser = argparse.ArgumentParser(description='get information from a tetra league JSON dump')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--get-user', '-u', metavar='USERNAME', type=str, help='get information of user')
group.add_argument('--get-rank', metavar='RANKING', type=int, help='get information on the nth-best player')
group.add_argument('--print-ranks', '-r', action='store_true', help='get a list of the TR required to reach certain ranks')
parser.add_argument('--input-file', '-i', metavar='PATH', type=str, default='tetraleaguerankings.json', help='path to json file from https://ch.tetr.io/api/users/lists/league/all (defaults to tetraleaguerankings.json)')
args = parser.parse_args()

with open(args.input_file, 'r') as file:
    database = json.loads(file.read())

# interesting information:
# TR = GLIXARE probability of beating the average unrated player (0-100) times 250
# GLIXARE = round(10000 / (1 + 10^(((1500 - RATING) * pi / sqrt(3 * ln(10)^2 * DEVIATION^2 + 2500 * (64 * pi^2 + 147 * ln(10)^2)))))) / 100
# level = (XP/500)^0.6 + XP/(5000 + max(0, XP-4000000)/5000) + 1

def ordinal(n):
    if n % 100 // 10 == 1: # if second-last digit is one
        return str(n)+'th'
    else:
        if n % 10 == 1:
            return str(n)+'st'
        elif n % 10 == 2:
            return str(n)+'nd'
        elif n % 10 == 3:
            return str(n)+'rd'
        else:
            return str(n)+'th'

def xp_to_level(xp):
    return int((xp/500)**0.6 + xp/(5000 + max(0, xp-4000000)/5000) + 1)

ranks = ['x', 'u', 'ss', 's+', 's', 's-', 'a+', 'a', 'a-', 'b+', 'b', 'b-', 'c+', 'c', 'c-', 'd+', 'd']
percentiles = [1, 5, 11, 17, 23, 30, 38, 46, 54, 62, 70, 78, 84, 90, 95] # only goes down to C-

ratings = []
for user in database['data']['users']:
    if user['league']['rank'] in ranks:
        ratings.append(user['league']['rating'])
ratings.sort(reverse=True)

def print_rank_ratings():
    for rank, percentile in zip(ranks, percentiles):
        required_rating = ratings[len(ratings) * percentile // 100]
        print(rank.upper()+':', round(required_rating))

def print_data(user):
    print('Username:', user['username'], '(id: '+user['_id']+')')
    print('Level:', xp_to_level(user['xp']), '(XP: '+str(user['xp'])+')')
    print('-----------------------------')
    print(user['league']['gamesplayed'], 'ranked games played;', user['league']['gameswon'], 'won', '('+'{:.2%}'.format(user['league']['gameswon']/user['league']['gamesplayed'])+')')
    print('TR:', int(user['league']['rating']), '(estimated '+'{:.2%}'.format(user['league']['rating']/25000)+' chance of beating the average unranked player)')
    print('Glicko-2 rating:', str(int(user['league']['glicko']))+'+'+str(int(user['league']['rd'])))
    print('Global rank:', ratings.index(user['league']['rating'])+1, '(top '+'{:.2%}'.format(ratings.index(user['league']['rating'])/len(ratings))+')')
    
    if user['country'] != None:
        # i should really have used dataframes
        local_ratings = []
        country = user['country']
        for player in database['data']['users']:
            if player['league']['rank'] in ranks and player['country'] == country:
                local_ratings.append(player['league']['rating'])
        local_ratings.sort(reverse=True)
        print('Country rank ('+country+'):', local_ratings.index(user['league']['rating'])+1, '(top '+'{:.2%}'.format(local_ratings.index(user['league']['rating'])/len(local_ratings))+')')

def get_user(username):
    for user in database['data']['users']:
        if user['username'] == username:
            print_data(user)
            return None
    print('user not found')

def get_rank(rank):
    if rank < 1: raise IndexError("list index out of range")
    rating = ratings[rank-1]
    for user in database['data']['users']:
        if user['league']['rating'] == rating:
            print_data(user)
            return None
    print('user not found')

if __name__ == '__main__':
    if args.get_user:
        get_user(args.get_user)
    elif args.get_rank:
        get_rank(args.get_rank)
    elif args.print_ranks:
        print_rank_ratings()
