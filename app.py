from aiohttp import web

from application.router.Router import Router

app = web.Application()

router = Router(app, web)

web.run_app(app)

