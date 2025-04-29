from models import connect
from flask import jsonify
conn = connect.connection()
cursor = conn.cursor()

def get_inform_flood_area():
    get_inform_flood_area_query = 'SELECT id, "NAME_1", "NAME_2", "ENGTYPE_3", elve_mean  FROM "GeoTIFF"."Flood_Area"'
    try:
        cursor.execute(get_inform_flood_area_query)
        data = cursor.fetchall()
        conn.commit()
        result = []
        for row in data:
            if row[4] != None:
                element = {
                    "id": row[0],
                    "State": row[1],
                    "Name": row[2],
                    "Type": row[3],
                    "Elve_mean": row[4],
                }
                result.append(element)
            
        return jsonify({
            "floodata": result,
            "status": "200",
            "message": "Successfull in get_inform_flood_area_API",
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "500",
            "message": e,
        }), 500
        