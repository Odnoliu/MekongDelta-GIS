from models import connect
from flask import jsonify, session
conn = connect.connection()
cursor = conn.cursor()

#Create community
def create_community(data):
    layer_id = data.get('layer_id')
    layer_name = data.get('layer_name')
    user = session['user'].get('email')
    layer_type = data.get('layer_type')
    search_layer_query = f"""
    SELECT * FROM "Layer_Schema"."Community" WHERE layer_id = {layer_id}
    """
    try:
        cursor.execute(search_layer_query)
        result = cursor.fetchall()
        if result:
            return jsonify({
                "message": "Layer is already in Community",
                "status": "200",
            }),200
        else:
            insert_layer_query = f"""
            INSERT INTO "Layer_Schema"."Community" (layer_id, layer_name, owner, layer_type)
            VALUES ('{layer_id}', '{layer_name}', '{user}', '{layer_type}')
            """
            try:
                cursor.execute(insert_layer_query)
                conn.commit()
                return jsonify({
                    "message": "Insert new layer into Community API successfull",
                    "status": "200",
                }), 200
            except Exception as e:
                return jsonify({
                    "error": str(e),
                    "status": "500",
                }), 500
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "500",
        }), 500
        
#Get All community
# Get All Layer
def get_all_community():
    get_all_community_query  = f"""
        SELECT * FROM "Layer_Schema"."Community" ORDER BY layer_id ASC
    """
    try:
        cursor.execute(get_all_community_query)
        layers = cursor.fetchall()
        conn.commit()
        return jsonify({
            "message": "Get all community API successful",
            "layers": layers,
            "status" : "200",
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Error in get all community API",
            "error": str(e),
            "status": "500",
        }), 500
        
#Delete community
def delete_community(data):
    layer_id = data.get('layer_id')
    delete_layer_query = f"""
    DELETE FROM "Layer_Schema"."Community" WHERE layer_id = {layer_id}
    """
    try:
        cursor.execute(delete_layer_query)
        conn.commit()
        return jsonify({
            "message": "Delete community API successful",
            "status": "200"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "500",
        }), 500