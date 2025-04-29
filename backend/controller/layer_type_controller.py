from flask import jsonify
from models import connect

conn = connect.connection()
cursor = conn.cursor()

#Get All Layer_Type
def get_all_layer_type():
    get_all_layer_type_query = f"""
    SELECT * FROM "Layer_Schema"."Layer_Type" ORDER BY type_id ASC
    """
    try:
        cursor.execute(get_all_layer_type_query)
        layer_type = cursor.fetchall()
        conn.commit()
        return jsonify({
            "message": "Get all layer type API successful",
            "layer_type": layer_type,
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "500",
        }), 500