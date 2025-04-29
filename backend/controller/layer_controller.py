from models import connect
from flask import session, jsonify, Flask
import geopandas as gpd
import json
from shapely.geometry import shape
from shapely.geometry import mapping
import zipfile
import os
import shutil
import tempfile
from fastkml import kml

from module import read_file_gis


conn = connect.connection()
cursor = conn.cursor()

# Create Layer
def create_default_layer(data):
    if not data:
        return jsonify({
            "message": "Not enough information to create Layer!!!",
            "status": "400"
        }), 400
    user = session['user']
    id = user['id']
    state_layer_name = 'Default MD State'
    state_fill = '#8B5A2B'
    state_stroke = '#FFA500'
    state_layer_type = 'L001'
    state_z_index = 3
    state_layer_project_id = data
    state_stroke_width = 2
    
    district_layer_name = 'Default MD District'
    district_fill = '#8B5A2B'
    district_stroke = '#FFA500'
    district_layer_type = 'L001'
    district_z_index = 2
    district_layer_project_id = data
    district_stroke_width = 1
    
    vn_layer_name = 'Default Viet Nam'
    vn_fill = '#D32F2F'
    vn_stroke = '#212121'
    vn_layer_type = 'L001'
    vn_z_index = 1
    vn_layer_project_id = data
    vn_stroke_width = 2
    
    create_default_layer_query = f"""
    INSERT INTO "Layer_Schema"."Layer" (layer_name, fill, stroke, layer_type, project_id, stroke_width, z_index)
    VALUES ('{state_layer_name}', '{state_fill}', '{state_stroke}', '{state_layer_type}', {state_layer_project_id}, {state_stroke_width}, {state_z_index}),
            ('{district_layer_name}', '{district_fill}', '{district_stroke}', '{district_layer_type}', {district_layer_project_id}, {district_stroke_width}, {district_z_index}),
            ('{vn_layer_name}', '{vn_fill}', '{vn_stroke}', '{vn_layer_type}', {vn_layer_project_id}, {vn_stroke_width}, {vn_z_index});
    """
    try:
        cursor.execute(create_default_layer_query)
        conn.commit()
        return jsonify({
            "message": "Create default layer successfull!!!",
            "status": "200"
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "500"
        })
        
def create_file_layer(form, file):
    print(form, file)
    user = session['user']
    id = user['id']
    layer_name = form['name']
    layer_type = 'L002'
    layer_status = 'private'
    description = form['description']
    fill_color = form['fill_color']
    stroke_color = form['stroke_color']
    stroke_width = form['stroke_width']
    z_index = form['priority']
    project_id = form['project_id']
    create_layer_query = f"""
    INSERT INTO "Layer_Schema"."Layer" (layer_name, layer_type, project_id, description, fill, stroke, stroke_width, z_index, status)
    VALUES ('{layer_name}', '{layer_type}', {project_id}, '{description}', '{fill_color}', '{stroke_color}', '{stroke_width}', {z_index}, '{layer_status}')
    RETURNING layer_id;
    """
    print(create_layer_query)
    try:
        cursor.execute(create_layer_query)
        layer_id = cursor.fetchone()[0]
        print(layer_id)
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 500
        }), 500
    
    filename = file.filename
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    print(extension)
    try:
        # Đọc file dựa trên định dạng
        if extension == 'json':
            features = read_file_gis.process_json(file)
        elif extension == 'kmz':
            features = read_file_gis.process_kmz(file)
        elif extension == 'zip':
            features = read_file_gis.process_zip(file)
        elif extension == 'gpkg':
            features = read_file_gis.process_gpkg(file)

        feature_ids = []   
        for feature in features:
                geom = feature['geometry']
                properties = json.dumps(feature['properties'])
                name = feature['properties'].get('name', 'Unnamed')

                cursor.execute(
                    """
                    INSERT INTO "Layer_Schema"."Features" (name, geom, properties, layer_id)
                    VALUES (%s, ST_GeomFromText(%s, 4326), %s, %s)
                    RETURNING id
                    """,
                    (name, geom.wkt if hasattr(geom, 'wkt') else str(geom), properties, layer_id)
                )
                feature_id = cursor.fetchone()[0]
                feature_ids.append(feature_id)
        conn.commit()
        return jsonify({
            'message': 'Create layer successfull!!!',
            'layer_id': layer_id,
            'type_layer': layer_type,
            'feature_count': len(features),
            'feature_ids': feature_ids,
            'status': '200',
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': str(e),
            'status': '500',
        }), 500
        
def create_wms_layer(form):
    print(form)
    if not form:
        return jsonify({
            "message": "Not enough data to create wms layer",
            "status": "400" 
        }), 400
    
    user = session['user']
    id = user['id']
    layer_name = form['name']
    layer_type = 'L006'
    description = form['description']
    project_id = form['project_id']
    wms_url = form['wms_url']
    z_index = form['priority']
    layer_status = 'private'
    print(wms_url)
    create_layer_query = f"""
    INSERT INTO "Layer_Schema"."Layer" (layer_name, layer_type, project_id, description, "WMS", z_index, status)
    VALUES ('{layer_name}', '{layer_type}', {project_id}, '{description}', '{wms_url}', {z_index}, '{layer_status}')
    RETURNING layer_id;
    """   
    print(create_layer_query)
    try:
        cursor.execute(create_layer_query)
        layer_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({
            'message': 'Create layer successfull!!!',
            'layer_id': layer_id,
            'type_layer': layer_type,
            'status': '200',
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 500
        }), 500
        
def create_layer_from_layer(data):
    if not data:
        return jsonify({
            "message": "Not enough data to create layer from layer",
            "status": "400" 
        }), 400
    print(data)
    layer_name = data['name']
    print('Name: ', layer_name)
    layer_type = 'L004'
    description = data['description']
    print('Description: ', description)
    project_id = data['project_id']
    print("Project_id: ", project_id)
    list_layer = data['layers']
    print("list_layer: ",list_layer)
    fill_color = data['fill_color']
    z_index = data['priority']
    stroke_color = data['stroke_color']
    status = 'private'
    try:
        selected_layers = json.loads(list_layer)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    # Lấy danh sách layer_id từ selected_layers
    l002_layer_ids = [layer['id'] for layer in selected_layers if layer['type'] == 'L002']
    try:
        # Khởi tạo biến để lưu layer_id mới
        new_layer_id = None
        
        # 1. Tạo một dòng mới trong bảng layer
        cursor.execute("""
            INSERT INTO "Layer_Schema"."Layer" (layer_name, created_at, fill, stroke, layer_type, project_id, description, z_index, status)
            VALUES (%s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)
            RETURNING layer_id;
        """, (layer_name, fill_color, stroke_color, layer_type, project_id, description, z_index, status))
        new_layer_id = cursor.fetchone()[0]  # Lấy layer_id mới
            
        # 2. Sao chép feature từ bảng "Layer_Schema"."Layer" cho L002
        if l002_layer_ids:
            cursor.execute("""
                INSERT INTO "Layer_Schema"."Features" (name, geom, properties, layer_id)
                SELECT
                    name, 
                    geom,
                    properties,
                    %s
                FROM "Layer_Schema"."Features"
                WHERE layer_id = ANY(%s);
            """, (new_layer_id, l002_layer_ids))
        # Commit giao dịch
        conn.commit()
        # Trả về phản hồi
        return jsonify({
            "message": "Layer and features created successfully",
            "status": "200",
            "new_layer_id": new_layer_id
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": str(e),
            "status": "500",
        }), 500
             
    
# Get All Layer
def get_all_layer(project_id):
    if not project_id:
        return jsonify({
            "message": "Not enough information to find Layer!!!",
            "status": "400"
        }), 400
    project_id = int(project_id)
    get_all_layer_query  = f"""
        SELECT * FROM "Layer_Schema"."Layer" WHERE project_id = {project_id} ORDER BY layer_id ASC
    """
    try:
        cursor.execute(get_all_layer_query)
        layers = cursor.fetchall()
        conn.commit()
        return jsonify({
            "message": "Get all layer API successful",
            "layers": layers,
            "status" : "200",
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Error in get all layer API",
            "error": str(e),
            "status": "500",
        }), 500
        
# Get Layer By Layer_Type
def get_all_layer_by_type(project_id, layer_type):
    if not project_id or not layer_type:
        return jsonify({
            "message": "Not enough information to find Layer by type!!!",
            "status": "400"
        }), 400
    get_layer_by_type_query  = f"""
        SELECT * FROM "Layer_Schema"."Layer" WHERE project_id = {project_id}  AND layer_type = '{layer_type}' ORDER BY layer_id ASC
    """
    try:
        cursor.execute(get_layer_by_type_query)
        layers = cursor.fetchall()
        conn.commit()
        return jsonify({
            "message": "Get layer by type API successful",
            "layers": layers,
            "status" : "200",
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Error in get all layer API",
            "error": str(e),
            "status": "500",
        }), 500
       
#Get max priority
def get_max_zindex(project_id):
    if not project_id:
        return jsonify({
            "message": "Not enough information to get max z-index!!!",
            "status": "400"
        }), 400
    get_max_zindex_query = f"""
    SELECT MAX(z_index) FROM "Layer_Schema"."Layer" WHERE project_id = {project_id}
    """
    try:
        cursor.execute(get_max_zindex_query)
        max_z_index = cursor.fetchone()
        conn.commit()
        return jsonify({
            "message": "Get max z-index API successful!",
            "status": "200",
            "z_index": max_z_index
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "500"
        }), 500
        
#Get layer by id
def get_layer_by_id(layer_id):
    get_layer_by_id_query = f"""
    SELECT * FROM "Layer_Schema"."Layer" WHERE layer_id = {layer_id}
    """
    try:
        cursor.execute(get_layer_by_id_query)
        layer = cursor.fetchone()
        conn.commit()
        return jsonify({
            "message":"Get layer by id APi successful!",
            "status": 200,
            "layer": layer,
        }),200
    except Exception as e:
        return jsonify({
            "message": "Error in get layer by id API",
            "status": 500,
            "error": str(e),
        }), 500
        
# Update Layer
def update_status_layer(layer_id, layer_status):
    update_status_layer_query = f"""
    UPDATE "Layer_Schema"."Layer"
    SET status = '{layer_status}'
    WHERE layer_id = {layer_id};
    """
    try:
        cursor.execute(update_status_layer_query)
        conn.commit()
        return jsonify({
            "message": "Update status API successful",
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Error in update status API",
            "status": "500",
            "error": str(e),
        }), 500
       
def update_priority_layer(layer_id, layer_priority):
    update_priority_layer_query = f"""
    UPDATE "Layer_Schema"."Layer"
    SET z_index = '{layer_priority}'
    WHERE layer_id = {layer_id};
    """
    try:
        cursor.execute(update_priority_layer_query)
        conn.commit()
        return jsonify({
            "message": "Update priority API successful",
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Error in update priority API",
            "status": "500",
            "error": str(e),
        }), 500
        
def update_vector_layer(data):
    if not data:
        return jsonify({
            "status": 404,
            "message": "Not enough information to update layer",
        }), 404
    layer_id = data['layer_id']
    layer_name = data['name']
    fill = data['fill']
    stroke = data['stroke']
    stroke_width = data['stroke_width']
    description = data['des']
    update_vector_layer_query = f"""
    UPDATE "Layer_Schema"."Layer"
    SET layer_name = '{layer_name}',
        fill = '{fill}',
        stroke = '{stroke}',
        stroke_width = {stroke_width},
        description = '{description}'
    WHERE layer_id = {layer_id}
    """
    try:
        cursor.execute(update_vector_layer_query)
        conn.commit()
        return jsonify({
            "message": "Update vector layer API successful",
            "status": 200,
        })
    except Exception as e:
        return jsonify({
            "message": "Error in update vector layer API",
            "status": 500,
            "error": str(e)
        }), 500
        
def update_tile_layer(data):
    if not data:
        return jsonify({
            "status": 404,
            "message": "Not enough information to update layer",
        }), 404
    layer_id = data['layer_id']
    layer_name = data['name']
    description = data['des']
    update_tile_layer_query = f"""
    UPDATE "Layer_Schema"."Layer"
    SET layer_name = '{layer_name}',
        description = '{description}'
    WHERE layer_id = {layer_id}
    """
    try:
        cursor.execute(update_tile_layer_query)
        conn.commit()
        return jsonify({
            "message": "Update tile layer API successful",
            "status": 200,
        })
    except Exception as e:
        return jsonify({
            "message": "Error in update tile layer API",
            "status": 500,
            "error": str(e)
        }), 500
# Delete Layer
def delete_layer(layer_id):
    if not layer_id:
        return jsonify({
            "message": "Not enough information to delete layer!!!",
            "status": "400"
        }), 400
    delete_layer_query = f"""
    DELETE FROM "Layer_Schema"."Layer" WHERE layer_id = {layer_id};
    """
    try:
        cursor.execute(delete_layer_query)
        conn.commit()
        return jsonify({
            "message": "Delete layer API successfull!",
            "status": "200" 
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "500",
        }),500
