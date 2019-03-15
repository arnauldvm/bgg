#!/usr/bin/env python3

from sys import argv
import argparse

from boardgamegeek import BGGClient, BGGClientLegacy
from boardgamegeek.cache import CacheBackendSqlite

DEFAULT_LIST_ID = '253162'
DEFAULT_CACHE_TTL = 3600*24
DEFAULT_USERNAME = 'arnauldvm'

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    # -> shows default values in help message
)
parser.add_argument('-f', '--force', action='store_true',
                    help="force cache refresh")
parser.add_argument('-t', '--cache_ttl', type=int, default=DEFAULT_CACHE_TTL,
                    help="time-to-live, in seconds, for the HTTP cache")
parser.add_argument('-u', '--username', default=DEFAULT_USERNAME,
                    help="username for collection")
parser.add_argument('list_id', nargs='?', default=DEFAULT_LIST_ID,
                    help="identifier of the boardgame geeklist")
args = parser.parse_args()

effective_cache_ttl = args.cache_ttl
if args.force:
    print("Forcing cache refresh")
    effective_cache_ttl = 0

cache = CacheBackendSqlite(path=".cache.bgg", ttl=effective_cache_ttl)

bgg1 = BGGClientLegacy(cache=cache)
list = bgg1.geeklist(args.list_id, comments=True)
print(f"[{list.id}] {list.name}\n{list.description}")

bgg2 = BGGClient(cache=cache)
games_id_list = [
    item.object.id for item in list
    if item.object.type == 'thing' and item.object.subtype == 'boardgame'
]
games = bgg2.game_list(games_id_list)
games_dict = {game.id: game for game in games}

collection = bgg2.collection(user_name=args.username)
collection_dict = {colgame.id: colgame for colgame in collection}

for item in list:
    colgame = collection_dict.get(item.object.id, None)
    effective_name = (
        colgame.name if colgame is not None
        else f"({item.object.name})")
    print(f"  [{item.object.id}]"
          f" img:{item.object.imageid} {effective_name}", end='')
    game = games_dict[item.object.id]
    print(f" #{game.bgg_rank}", end='')
    print(f" year:{game.year}", end='')
    print(f" players:[{game.min_players}-{game.max_players}]", end='')
    print(f" age:>={game.min_age}yr", end='')
    print(f" time:{game.playing_time}'", end='')
    print(f" weight:{game.rating_average_weight:.1f}/5", end='')
    print(f" by:{', '.join(game.designers)}", end='')
    print()
    if item.description:
        print(f"    . {item.description}")
