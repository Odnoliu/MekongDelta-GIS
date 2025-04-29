from flask import jsonify
from models import connect

conn = connect.connection()
cursor = conn.cursor()

def create_feature_inform(data):
    if not data:
        return jsonify({
            "message":"Not enough information to create new feature inform",
            "status": "400"
        }),400
    layer_name = data.get('layer_name')
    feature_id = data.get('feature_id')
    title = data.get('title')
    content = data.get('content')
    if layer_name == 'VN':
        create_feature_inform_query = f"""
        INSERT INTO "Layer_Schema"."Feature_Inform" (vn_feature_id, title, content) VALUES (%s, %s, %s)
        """
    else: 
        if layer_name == 'MD_State':
            create_feature_inform_query = f"""
            INSERT INTO "Layer_Schema"."Feature_Inform" (state_feature_id, title, content) VALUES (%s, %s, %s)
            """   
        else:
            if layer_name == 'MD_District':
                create_feature_inform_query = f"""
                INSERT INTO "Layer_Schema"."Feature_Inform" (district_feature_id, title, content) VALUES (%s, %s, %s)
                """    
            else:
                create_feature_inform_query = f"""
                INSERT INTO "Layer_Schema"."Feature_Inform" (user_feature_id, title, content) VALUES (%s, %s, %s)
                """   
    values = (feature_id, title, content)
    try:
        cursor.execute(create_feature_inform_query, values)
        conn.commit()
        return jsonify({
            "message": "Create feature inform successful",
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify ({
            "message": "Error in create feature inform API",
            "status": "500",
            "error": str(e)
        }), 500
        
def get_feature_inform_by_id(feature_id, layer_name):
    if not feature_id or not layer_name:
        return jsonify({
            "message":"Not enough information to update feature inform",
            "status": "400"
        }),400
    if layer_name == 'VN':
        get_feature_inform_query = f"""
        SELECT * FROM "Layer_Schema"."Feature_Inform" WHERE vn_feature_id = {feature_id}
        """
    else:
        if layer_name == 'MD_State':
            get_feature_inform_query = f"""
            SELECT * FROM "Layer_Schema"."Feature_Inform" WHERE state_feature_id = {feature_id}
            """
        else:
            if layer_name == 'MD_District':
                get_feature_inform_query = f"""
                SELECT * FROM "Layer_Schema"."Feature_Inform" WHERE district_feature_id = {feature_id}
                """
            else:
                get_feature_inform_query = f"""
                SELECT * FROM "Layer_Schema"."Feature_Inform" WHERE user_feature_id = {feature_id}
                """    
    try:
        cursor.execute(get_feature_inform_query)
        feature_inform = cursor.fetchall()
        conn.commit()
        return jsonify({
            "message": "Get feature inform successful",
            "status": "200",
            "feature_inform": feature_inform
        }), 200
    except Exception as e:
        return jsonify ({
            "message": "Error in get feature inform API",
            "status": "500",
            "error": str(e)
        }), 500
        
def update_feature_inform(data):
    if not data:
        return jsonify({
            "message":"Not enough information to update feature inform",
            "status": "400"
        }),400
    id = data.get('id')
    title = data.get('title')
    content = data.get('content')
    
    update_feature_inform_query = f"""
    UPDATE "Layer_Schema"."Feature_Inform"
    SET title = %s, content = %s
    WHERE id = %s
    """
    values = (title, content, id)
    try:
        cursor.execute(update_feature_inform_query, values)
        conn.commit()
        return jsonify({
            "message": "Update feature inform successful",
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify ({
            "message": "Error in update feature inform API",
            "status": "500",
            "error": str(e)
        }), 500
        
        
def delete_feature_inform(data):
    if not data:
        return jsonify({
            "message":"Not enough information to delete feature inform",
            "status": "400"
        }),400
    id = data.get('id')
    delete_feature_inform_query = f"""
    DELETE FROM "Layer_Schema"."Feature_Inform" WHERE id = {id}
    """
    try:
        cursor.execute(delete_feature_inform_query)
        conn.commit()
        return jsonify({
            "message": "Delete feature inform successful",
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify ({
            "message": "Error in delete feature inform API",
            "status": "500",
            "error": str(e)
        }), 500
        
def search_title(data):
    if not data:
        return jsonify({
            "message": "Not enough information to find data",
            "status": "400"
        }), 400
    search_data_query = f"""
    SELECT * FROM "Layer_Schema"."Feature_Inform" WHERE title = '{data}'
    """
    try:
        cursor.execute(search_data_query)
        result = cursor.fetchall()
        conn.commit()
        return jsonify({
            "message": "Search data feature successful",
            "status": "200",
            "inform": result
        }),200
    except Exception as e:
        return jsonify({
            "message": "Error in search data API",
            "status": "500",
            "error": str(e)
        })