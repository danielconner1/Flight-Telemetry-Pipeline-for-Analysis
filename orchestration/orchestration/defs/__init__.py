from dagster import Definitions, load_assets_from_modules

from . import ingest
from . import process
from . import features
all_assets = load_assets_from_modules([ingest,process,features])

defs = Definitions(
    assets=all_assets,
)
