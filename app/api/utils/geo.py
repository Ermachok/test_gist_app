from shapely.geometry import Point
from shapely.ops import transform
import pyproj
import geojson


def generate_circle_polygon(lat: float, lon: float, radius_m: float, num_points: int = 64):
    """
    Возвращает GeoJSON-полигон в виде круга и площадь в м²
    """
    # центр круга
    center = Point(lon, lat)

    # азимутальная проекция с центром в заданной точке
    proj_aeqd = pyproj.Proj(proj="aeqd", lat_0=lat, lon_0=lon)

    # WGS84(широта/долгота) в метры и обратно
    project_to_m = pyproj.Transformer.from_proj(pyproj.Proj('epsg:4326'), proj_aeqd, always_xy=True).transform
    project_to_latlon = pyproj.Transformer.from_proj(proj_aeqd, pyproj.Proj('epsg:4326'), always_xy=True).transform

    # центр в метрическую систему
    center_m = transform(project_to_m, center)

    # круг в метрах
    circle_m = center_m.buffer(radius_m, resolution=num_points)

    # обратно в WGS84
    circle_latlon = transform(project_to_latlon, circle_m)

    # GeoJSON
    geojson_polygon = geojson.Feature(geometry=geojson.Polygon([list(circle_latlon.exterior.coords)]))

    # площадь круга
    area_m2 = circle_m.area
    area_km2 = area_m2 / 1_000_000

    return geojson_polygon, area_km2
