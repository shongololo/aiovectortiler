import os
import sys
import logging
import argparse
from aiohttp import web
from utilery.config_handler import Configs


# parse arguments
ARGS = argparse.ArgumentParser(description="asyncio python tile server")
ARGS.add_argument('--server_configs',
                  action="store",
                  dest='server_configs',
                  default='../configs_server_example.yaml',
                  help='The YAML database config file')
ARGS.add_argument('--layer_configs',
                  action="store",
                  dest="layer_configs",
                  default='../configs_layers_example.yaml',
                  help='The YAML layers configs file')
args = ARGS.parse_args()


# write configs
Configs.init_server_configs(os.path.abspath(args.server_configs))
Configs.init_layer_configs(os.path.abspath(args.layer_configs))


# setup logging
logging.basicConfig(stream=sys.stdout, level=Configs.layers['log_level'].upper())
logger = logging.getLogger(__name__)
logger.warning('STARTING TILE SERVER APP')


from utilery.tile_handler import ServePBF, ServeGeoJSON, ServeJSON, TileJson


# setup app
app = web.Application()


# setup url routes and corresponding handlers
async def request_pbf(request):
    response = ServePBF.serve(request)
    return web.Response(body=response)
app.router.add_route('GET', '/{layer}/{z}/{x}/{y}.pbf', request_pbf)
app.router.add_route('GET', '/{layer}/{z}/{x}/{y}.mvt', request_pbf)

async def request_geojson(request):
    response = ServeGeoJSON.serve(request)
    return web.Response(body=response)
app.router.add_route('GET', '/{layer}/{z}/{x}/{y}.geojson', request_geojson)

async def request_json(request):
    response = ServeJSON.serve(request)
    return web.Response(body=response)
app.router.add_route('GET', '/{layer}/{z}/{x}/{y}.json', request_json)

async def request_tilejson(request):
    response = TileJson.get()
    return web.Response(body=response)
app.router.add_route('GET', '/tilejson/mvt.json', request_tilejson)


# start the server
web.run_app(app)