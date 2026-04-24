from dagster import Definitions, load_assets_from_modules

from . import ingest
from . import process

all_assets = load_assets_from_modules([ingest,process])

defs = Definitions(
    assets=all_assets,
)
