
from application.modules.getfreq import GetFrequency


class Router:

    def __init__(self, app, web):
        self.app = app
        self.web = web
        self.appData = GetFrequency()
        routes = [
            { 'method': 'GET', 'path': '/', 'handler': self.handleStatic},
            { 'method': 'POST', 'path': '/upload-song', 'handler': self.handleUploadSong },
            { 'method': 'GET', 'path': '/get-numbers-values', 'handler': self.handleNumbersValues }
        ]
        app.router.add_static('/css/', path=str('./client/css/'))
        app.router.add_static('/js/', path=str('./client/js/'))
        for route in routes:
            app.router.add_route(route['method'], route['path'], route['handler'])

    def handleStatic(self, request):
        return self.web.FileResponse('./client/index.html')

    async def handleUploadSong(self, request):
        request._client_max_size = 1024 ** 2 * 100  # 100MB max size
        start = None
        end = None
        if 'start' in request.query.keys() and 'end' in request.query.keys()\
                and request.query['start'] != '' and request.query['end'] != '':
            start = float(request.query['start']) or None
            end = float(request.query['end']) or None
        song = await request.post()  # Песня приходит в формате MultiDictProxy
        imageInBase64 = self.appData.getfreq(song['file'].file, start, end)
        return self.web.json_response({ 'img': imageInBase64 })

    def handleNumbersValues(self, request):
        values = self.appData.dict_max_freq
        return self.web.json_response({ 'data': values })

