import geopandas as gpd
from zipfile import ZipFile
from io import BytesIO
from pykml import parser as kml_parser
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, shape
from shapely.geometry.base import BaseGeometry
import json
import os
import tempfile
import shutil
from geojson import loads as geojson_loads
#GeoJSON
def process_json(file):
    geojson_data = geojson_loads(file.read().decode('utf-8'))
    features = []
    
    if 'features' in geojson_data:
        for feature in geojson_data['features']:
            geom = shape(feature['geometry'])  # Chuyển GeoJSON geometry thành shapely object
            properties = feature.get('properties', {})
            features.append({
                'geometry': geom,
                'properties': properties
            })
    return features
    
#KMZ
# Hàm chuyển đổi tọa độ KML sang shapely geometry
def parse_coordinates(coord_str):
    coords = []
    for coord in coord_str.strip().split():
        lon, lat = map(float, coord.split(',')[:2])  # Lấy kinh độ, vĩ độ, bỏ qua độ cao nếu có
        coords.append((lon, lat))
    return coords

# Hàm xử lý Placemark và trả về geometry cùng properties
def process_placemark(placemark):
    properties = {'name': str(placemark.name)} if hasattr(placemark, 'name') else {}
    geometry = None

    print(f"Processing Placemark: {properties.get('name', 'Unnamed')}")

    # Kiểm tra các loại geometry
    if hasattr(placemark, 'Point'):
        print("  Found Point")
        coords = parse_coordinates(placemark.Point.coordinates.text)
        geometry = Point(coords[0])

    elif hasattr(placemark, 'LineString'):
        print("  Found LineString")
        coords = parse_coordinates(placemark.LineString.coordinates.text)
        geometry = LineString(coords)

    elif hasattr(placemark, 'Polygon'):
        print("  Found Polygon")
        if hasattr(placemark.Polygon, 'outerBoundaryIs') and hasattr(placemark.Polygon.outerBoundaryIs, 'LinearRing'):
            outer_coords = parse_coordinates(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text)
            geometry = Polygon(outer_coords)
        else:
            print("  Polygon missing outerBoundaryIs or LinearRing")

    elif hasattr(placemark, 'MultiGeometry'):
        print("  Found MultiGeometry")
        geometries = []
        for geom in placemark.MultiGeometry.getchildren():
            geom_tag = geom.tag.split('}')[-1]  # Lấy tên thẻ không namespace
            print(f"    MultiGeometry child: {geom_tag}")
            
            if geom_tag == 'Point':
                coords = parse_coordinates(geom.coordinates.text)
                geometries.append(Point(coords[0]))
            elif geom_tag == 'LineString':
                coords = parse_coordinates(geom.coordinates.text)
                geometries.append(LineString(coords))
            elif geom_tag == 'Polygon':
                if hasattr(geom, 'outerBoundaryIs') and hasattr(geom.outerBoundaryIs, 'LinearRing'):
                    outer_coords = parse_coordinates(geom.outerBoundaryIs.LinearRing.coordinates.text)
                    geometries.append(Polygon(outer_coords))
                else:
                    print("    Polygon in MultiGeometry missing outerBoundaryIs or LinearRing")
        
        # Xác định loại MultiGeometry
        if geometries:
            if all(isinstance(g, Point) for g in geometries):
                geometry = MultiPoint(geometries)
            elif all(isinstance(g, LineString) for g in geometries):
                geometry = MultiLineString(geometries)
            elif all(isinstance(g, Polygon) for g in geometries):
                geometry = MultiPolygon(geometries)
            else:
                geometry = geometries  # Trả về danh sách nếu hỗn hợp
        else:
            print("  No valid geometries in MultiGeometry")

    else:
        print("  No supported geometry found in Placemark")

    return {
        'geometry': geometry,
        'properties': properties
    }

# Hàm duyệt qua Folder để tìm Placemark
def process_folder(folder, features):
    print("Processing Folder...")
    for element in folder.getchildren():
        if element.tag.endswith('Placemark'):
            feature = process_placemark(element)
            if feature['geometry']:
                features.append(feature)
        elif element.tag.endswith('Folder'):
            process_folder(element, features)  # Đệ quy nếu có Folder lồng nhau

# Hàm chính để đọc và xử lý KMZ
def process_kmz(file_path):
    with ZipFile(BytesIO(file_path.read())) as kmz:
        kml_file = [f for f in kmz.namelist() if f.endswith('.kml')][0]
        print(f"Found KML file in KMZ: {kml_file}")
        with kmz.open(kml_file) as kml:
            kml_content = kml.read()
            root = kml_parser.fromstring(kml_content)

            features = []
            print("Root elements:", [child.tag for child in root.getchildren()])

            # Kiểm tra Document
            if hasattr(root, 'Document'):
                print("Processing Document...")
                for element in root.Document.getchildren():
                    if element.tag.endswith('Placemark'):
                        feature = process_placemark(element)
                        if feature['geometry']:
                            features.append(feature)
                    elif element.tag.endswith('Folder'):
                        process_folder(element, features)
            else:
                print("No Document found, checking root for Placemarks...")
                for element in root.getchildren():
                    if element.tag.endswith('Placemark'):
                        feature = process_placemark(element)
                        if feature['geometry']:
                            features.append(feature)
                    elif element.tag.endswith('Folder'):
                        process_folder(element, features)

            return features
        
#GeoPackage
# Hàm xử lý GeoDataFrame và trả về danh sách features
def process_gpkg(file_path):
    # Đọc file GeoPackage bằng geopandas
    gdf = gpd.read_file(BytesIO(file_path.read()), driver='GPKG')
    print(f"Found {len(gdf)} features in GPKG file.")

    features = []
    for _, row in gdf.iterrows():
        feature = {
            'geometry': row['geometry'],
            'properties': row.drop('geometry').to_dict()  # Loại bỏ cột geometry khỏi properties
        }
        features.append(feature)
    
    return features


#ShapeFile
# Hàm kiểm tra các file cần thiết trong ZIP
def check_shapefile_components(zip_ref):
    files = zip_ref.namelist()
    shp_file = [f for f in files if f.endswith('.shp')]
    shx_file = [f for f in files if f.endswith('.shx')]
    dbf_file = [f for f in files if f.endswith('.dbf')]
    
    if not shp_file:
        raise ValueError("No .shp file found in ZIP.")
    if not shx_file:
        raise ValueError("Missing .shx file in ZIP.")
    if not dbf_file:
        raise ValueError("Missing .dbf file in ZIP.")
    
    return shp_file[0]

# Hàm xử lý file ZIP chứa Shapefile và trả về danh sách features
def process_zip(file_path):
    with ZipFile(BytesIO(file_path.read())) as zip_ref:
        # Kiểm tra các file cần thiết
        shp_file = check_shapefile_components(zip_ref)
        print(f"Found Shapefile in ZIP: {shp_file}")
        
        # Tạo thư mục tạm để giải nén
        temp_dir = tempfile.mkdtemp()
        try:
            # Giải nén tất cả file vào thư mục tạm
            zip_ref.extractall(temp_dir)
            shp_path = os.path.join(temp_dir, shp_file)
            
            # Đọc Shapefile bằng geopandas
            gdf = gpd.read_file(shp_path, driver='ESRI Shapefile')
            print(f"Found {len(gdf)} features in ZIP file.")

            features = []
            for _, row in gdf.iterrows():
                feature = {
                    'geometry': row['geometry'],
                    'properties': row.drop('geometry').to_dict()  # Loại bỏ cột geometry khỏi properties
                }
                features.append(feature)
            
            return features
        finally:
            # Xóa thư mục tạm sau khi xử lý
            shutil.rmtree(temp_dir)