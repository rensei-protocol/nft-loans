"""
command: "python manage.py shell" and insert all code into shell
todo-remove: remove or move to other place, e.g. one_time_scripts package
"""

# x2y2
from aggregators.fetchers.x2y2.main import X2Y2Fetcher

fetcher = X2Y2Fetcher()
fetcher.handle()

# nftfi
from aggregators.fetchers.nftfi.main import NftfiFetcher

fetcher = NftfiFetcher()
fetcher.handle()

# arcade
from aggregators.fetchers.arcade.main import ArcadeFetcher

fetcher = ArcadeFetcher()
fetcher.handle()

# benddao
from aggregators.fetchers.benddao.main import BenddaoFetcher

fetcher = BenddaoFetcher()
fetcher.handle()
