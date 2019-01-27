def create_box(input_corners):
    x = (float(input_corners[0][0]), float(input_corners[1][0]))
    y = (float(input_corners[0][1]), float(input_corners[1][1]))
    
    windmill_lats, windmill_lons = zip(*[
        (max(x), max(y)),
        (min(x), max(y)),
        (min(x), min(y)),
        (max(x), min(y)),
        (max(x), max(y))
        ])
    
    return windmill_lats, windmill_lons
    
