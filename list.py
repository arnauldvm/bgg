#!/usr/bin/env python3

from sys import argv

from boardgamegeek import BGGClient, BGGClientLegacy
from boardgamegeek.cache import CacheBackendSqlite

DEFAULT_LIST_ID = '253162'
CACHE_TTL = 3600*24

argnum = 1
list_id = argv[argnum] if len(argv) > argnum else DEFAULT_LIST_ID

cache1 = CacheBackendSqlite(path=".cache.bgg1", ttl=CACHE_TTL)
bgg1 = BGGClientLegacy(cache=cache1)
list = bgg1.geeklist(list_id, comments=True)
print(f"[{list.id}] {list.name}\n{list.description}")

cache2 = CacheBackendSqlite(path=".cache.bgg2", ttl=CACHE_TTL)
bgg2 = BGGClient(cache=cache2)
games_id_list = [
        item.object.id for item in list
        if item.object.type == 'thing' and item.object.subtype == 'boardgame'
    ]
games = bgg2.game_list(games_id_list)
games_dict = {game.id: game for game in games}

for item in list:
    print(f"  [{item.object.id}]"
          f" img:{item.object.imageid} {item.object.name}", end='')
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
