PATHS = {
    'cogs': 'cogs',
    'pictures': 'pictures',
    'storage': 'storage',
}

def add_paths(prefix: str, folds, ext: str = None):
    for k in folds:
        PATHS[k] = f'{prefix}/{k}{"." + ext if ext is not None else ""}'

add_paths(PATHS['cogs'], ['admin',
                          'events',
                          'math',
                          'poll',
                          'tournament',
                          'troll',
                          'archive'], '.py')
add_paths(PATHS['cogs'], ['math'])
add_paths(PATHS['cogs'], ['loops'])

REACT_COLORS = [f'<:number_{k}:{i}>' for k, i in enumerate([f'1135985{x}'
                                                            for x in
                                                            ['729504284712',
                                                             '726392119388',
                                                             '677104853032',
                                                             '675016097842',
                                                             '673367728219',
                                                             '670188441663',
                                                             '669253116035',
                                                             '667499901018',
                                                             '665251749898',
                                                             '663444009011',
                                                             '660994519132',
                                                             '659602022450',
                                                             '658264039545',
                                                             '655940386866']])]
PICTURES_ETXTENSIONS = ["jpg", "png", "jpeg", "rgb", "gif", "pbm", "pgm", "ppm", "tiff", "rast", "xbm", "bmp", "webp", "exr"]
DAYS = [1*24*60*60, 3*24*60*60, 6*24*60*60, 15*24*60*60, 31*24*60*60, 91*24*60*60]