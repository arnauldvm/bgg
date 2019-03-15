#!/usr/bin/env python3

from sys import argv

from boardgamegeek import BGGClient, BGGClientLegacy
from boardgamegeek.cache import CacheBackendSqlite

DEFAULT_LIST_ID = '253162'
CACHE_TTL = 3600*24
USERNAME = 'arnauldvm'

argnum = 1
if len(argv) > argnum and argv[argnum] in ['-f', '--force']:
    print("Forcing cache refresh")
    CACHE_TTL = 0
    argnum += 1
list_id = argv[argnum] if len(argv) > argnum else DEFAULT_LIST_ID

cache = CacheBackendSqlite(path=".cache.bgg", ttl=CACHE_TTL)

bgg1 = BGGClientLegacy(cache=cache)
list = bgg1.geeklist(list_id, comments=True)
print(f"[{list.id}] {list.name}\n{list.description}")

bgg2 = BGGClient(cache=cache)
games_id_list = [
    item.object.id for item in list
    if item.object.type == 'thing' and item.object.subtype == 'boardgame'
]
games = bgg2.game_list(games_id_list)
games_dict = {game.id: game for game in games}

collection = bgg2.collection(user_name=USERNAME)
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
