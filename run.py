from server.app     import app
from server.errors  import *
from server.website import Website
from server.backend import Backend_Api
from webbrowser     import open as wopen

if __name__ == '__main__':
    config = {
        'host' : '0.0.0.0',
        'port' : 1337,
        'debug': False
    }
    
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func = site.routes[route]['function'],
            methods   = site.routes[route]['methods'],
        )

    backend_api  = Backend_Api(app)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func = backend_api.routes[route]['function'],
            methods   = backend_api.routes[route]['methods'],
        )
    
    wopen('http://localhost:1337')
    print('Запущено на порту 1337')
    app.run(**config)