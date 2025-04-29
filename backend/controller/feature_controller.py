from models import connect
from flask import session, jsonify
import json

conn = connect.connection()
cursor = conn.cursor()

# Create Feature
def create_draw_feature(data):
    if not data or 'features' not in data or 'layer_name' not in data:
        return jsonify({
            "message": "Not enough information to create draw feature",
            "status": "404"
        }), 404
    features = data['features']
    layer_name = data['layer_name']
    get_layer_id_query = f"""
    SELECT layer_id FROM "Layer_Schema"."Layer" WHERE layer_name = '{layer_name}'
    """
    try:
        cursor.execute(get_layer_id_query)
        result = cursor.fetchone()[0]
        layer_id = int(result)
    except Exception as e:
        return jsonify({
            "message": "Error in get layer id by layer name",
            "status": "500",
            "error": str(e)
        }), 500
        
    for feature in features:
        name = feature['name']
        geom = json.dumps(feature['geom'])
        properties = feature['properties']
        try:
            cursor.execute(
                    """
                    INSERT INTO "Layer_Schema"."Features" (name, geom, properties, layer_id)
                    VALUES (%s, ST_GeomFromGeoJSON(%s), %s, %s)
                    """,
                    (name, geom.wkt if hasattr(geom, 'wkt') else str(geom), properties, layer_id)
                )
        except Exception as e:
            return jsonify({
                "message": "Error in create draw feature",
                "status": "500",
                "error": str(e),
            }), 500
    conn.commit()
    return jsonify({
        "message":"Create draw feature successful",
        "status": "200"
    }), 200
    
# Get All Feature
def get_default_feature():
    get_default_state_feature_query = f"""
        SELECT id, ST_AsGeoJSON(geom) as geometry FROM "Feature_Schema"."MD_State" ORDER BY id ASC
    """
    get_default_district_feature_query = f"""
        SELECT id, ST_AsGeoJSON(geom) as geometry FROM "Feature_Schema"."MD_District" ORDER BY id ASC
    """
    get_default_vn_feature_query = f"""
        SELECT id, ST_AsGeoJSON(geom) as geometry FROM "Feature_Schema"."VN_Lv0" ORDER BY id ASC
    """
    try:
        cursor.execute(get_default_vn_feature_query)
        vn_rows = cursor.fetchall()
        cursor.execute(get_default_district_feature_query)
        district_rows = cursor.fetchall()
        cursor.execute(get_default_state_feature_query)
        state_rows = cursor.fetchall()
        
        conn.commit()
        state_list_feature = []
        district_list_feature = []
        vn_list_feature = []
        
        for row in vn_rows:
            vn_feature = {
                "type": "Feature",
                "properties": {
                    "id": row[0],
                },
                "geometry": json.loads(row[1])  # Parse GeoJSON
            }
            vn_list_feature.append(vn_feature)

        vn_geojson_data = {
            "type": "FeatureCollection",
            "features": vn_list_feature
        }
        
        for row in district_rows:
            district_feature = {
                "type": "Feature",
                "properties": {
                    "id": row[0],
                },
                "geometry": json.loads(row[1])  # Parse GeoJSON
            }
            district_list_feature.append(district_feature)

        district_geojson_data = {
            "type": "FeatureCollection",
            "features": district_list_feature
        }
        
        for row in state_rows:
            state_feature = {
                "type": "Feature",
                "properties": {
                    "id": row[0],
                },
                "geometry": json.loads(row[1])  # Parse GeoJSON
            }
            state_list_feature.append(state_feature)

        state_geojson_data = {
            "type": "FeatureCollection",
            "features": state_list_feature
        }
        
        return jsonify({
            "message":"Get all default feature successful!!!",
            "features": [vn_geojson_data, district_geojson_data, state_geojson_data],
            "status": 200
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "Error in get all default deature API",
            "status": "500",
            "error": str(e)
        }), 500
        
# Get Feature By Layer ID
def get_feature_by_layer_id(layer_id):
    get_feature_by_layer_id_query = f"""
    SELECT id, name, ST_AsGeoJSON(geom) as geometry, properties FROM "Layer_Schema"."Features" WHERE layer_id = {layer_id} ORDER BY id ASC 
    """
    try:
        cursor.execute(get_feature_by_layer_id_query)
        feature_rows = cursor.fetchall()
        conn.commit()
        layer = []
        for row in feature_rows:
            feature = {
                "type": "Feature",
                "properties": {
                    "id": row[0],
                    "name": row[1],
                    "prop": row[3],
                },
                "geometry": json.loads(row[2])  # Parse GeoJSON
            }
            
            layer.append(feature)

        layer_data = {
            "type": "FeatureCollection",
            "features": layer,
        }
        return jsonify({
            "message":"Get feature by layer id successful!!!",
            "features": layer_data,
            "status": "200"
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "Error in get deature by layer id API",
            "status": "500",
            "error": str(e)
        }), 500
  
# Get Feature By Layer ID
def get_default_feature_by_layer_id(feature_id, layer_name):
    if not feature_id or not layer_name:
        return jsonify({
            "message":"Not enough information to get default feature",
            "status": "400",
        }), 400
    if layer_name == 'VN':
        get_default_feature_by_layer_id_query = f"""
            SELECT * FROM "Feature_Schema"."VN_Lv0" WHERE id = {feature_id} ORDER BY id ASC 
        """
        print(get_default_feature_by_layer_id_query)
        try:
            cursor.execute(get_default_feature_by_layer_id_query)
            feature_rows = cursor.fetchone()
            feature = {
                "type": "Feature",
                "properties": {
                    "fid": feature_rows[2],
                    "GID_0": feature_rows[3],
                    "COUNTRY": feature_rows[4],
                },
            }
            conn.commit()
            return jsonify({
                "message":"Get default feature by layer id successful!!!",
                "features": feature,
                "status": "200"
            }), 200
        
        except Exception as e:
            return jsonify({
                "message": "Error in get default deature by layer id API",
                "status": "500",
                "error": str(e)
        }), 500
    else: 
        if layer_name == 'MD_State':
            get_default_feature_by_layer_id_query = f"""
                SELECT * FROM "Feature_Schema"."MD_State" WHERE id = {feature_id} ORDER BY id ASC 
            """
            print(get_default_feature_by_layer_id_query)
            try:
                cursor.execute(get_default_feature_by_layer_id_query)
                feature_rows = cursor.fetchone()
                feature = {
                    "GID_1": feature_rows[2],
                    "GID_0": feature_rows[3],
                    "COUNTRY": feature_rows[4],
                    "NAME_1": feature_rows[5],
                    "VAR_NAME_1": feature_rows[6],
                    "NL_NAME_1": feature_rows[7],
                    "TYPE_1": feature_rows[8],
                    "ENG_TYPE_1": feature_rows[9],
                    "CC_1": feature_rows[10],
                    "HASC_1": feature_rows[11],
                    "ISO_1": feature_rows[12],
                }
                conn.commit()
                return jsonify({
                    "message":"Get default feature by layer id successful!!!",
                    "features": feature,
                    "status": "200"
                }), 200
            
            except Exception as e:
                return jsonify({
                    "message": "Error in get default deature by layer id API",
                    "status": "500",
                    "error": str(e)
            }), 500
        else:
            if layer_name == 'MD_District':
                get_default_feature_by_layer_id_query = f"""
                    SELECT * FROM "Feature_Schema"."MD_District" WHERE id = {feature_id} ORDER BY id ASC 
                """
                print(get_default_feature_by_layer_id_query)
                try:
                    cursor.execute(get_default_feature_by_layer_id_query)
                    feature_rows = cursor.fetchone()
                    feature = {
                        "GID_2": feature_rows[2],
                        "GID_0": feature_rows[3],
                        "COUNTRY": feature_rows[4],
                        "GID_1": feature_rows[5],
                        "NAME_1": feature_rows[6],
                        "NL_NAME_1": feature_rows[7],
                        "NAME_2": feature_rows[8],
                        "VAR_NAME_2": feature_rows[9],
                        "NL_NAME_2": feature_rows[10],
                        "TYPE_2": feature_rows[11],
                        "ENG_TYPE_2": feature_rows[12],
                        "CC_2": feature_rows[13],
                        "HASC_2": feature_rows[14]
                        
                    }
                    conn.commit()
                    return jsonify({
                        "message":"Get default feature by layer id successful!!!",
                        "features": feature,
                        "status": "200"
                    }), 200
                
                except Exception as e:
                    return jsonify({
                        "message": "Error in get default deature by layer id API",
                        "status": "500",
                        "error": str(e)
                }), 500
        
def get_feature_by_id(feature_id,layer_name):
    if not feature_id or not layer_name:
        return jsonify({
                "message":"Not enough information to get feature",
                "status": "400",
            }), 400
    get_feature_by_id_query = f"""
    SELECT properties FROM "Layer_Schema"."Features" WHERE id = {feature_id}
    """
    try:
        cursor.execute(get_feature_by_id_query)
        properties = cursor.fetchone()
        return jsonify({
            "message": "Get inform feature by id successfull",
            "status": "200",
            "properties": properties,
        }),200
    except Exception as e:
        return jsonify({
            "message": "Error in get feature by id API",
            "status": "500",
            "error": str(e)
        }),500
    
# Update Feature

# Delete Feature
def delete_feature(feature_id):
    if not feature_id:
        return jsonify({
            "message": "Not enough information to delete feature!!!",
            "status": "400"
        }), 400
    delete_feature_query = f"""
    DELETE FROM "Layer_Schema"."Features" WHERE id = {feature_id};
    """
    try:
        cursor.execute(delete_feature_query)
        conn.commit()
        return jsonify({
            "message": "Delete feature API successfull!",
            "status": "200" 
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "500",
        }),500