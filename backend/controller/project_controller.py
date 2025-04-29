from models import connect
from flask import jsonify, session
import json
import base64
import psycopg2

conn = connect.connection()
cursor = conn.cursor()

# Create Project
def create_project(data, image):
    if not data or not image:
        return jsonify({
            "message": "Not enough data to create project",
            "status": "400" 
        }), 400
        
    user = session['user']
    id = user['id']
    project_name = data['name']
    project_description= data['description']
    project_image = image.read()
    create_project_query = 'INSERT INTO "Project_Schema"."Projects" (project_name, project_img, project_type_id, owner, description) VALUES (%s, %s, 1, %s, %s) RETURNING project_id'

    try:
        cursor.execute(create_project_query,(project_name, psycopg2.Binary(project_image), id, project_description))
        project_id = cursor.fetchone()
        conn.commit()
        return jsonify({
        "message":"Successful get_all_project API",
        "project_id": project_id,
        "status": "200",
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": str(e),
            "message":"Eror in create_project API",
            "status": "500",
        }), 500


# Get All Project
def get_all_project():
    user = session['user']
    id = user['id']
    get_all_project_query = f""" SELECT * FROM  "Project_Schema"."Projects" WHERE owner = '{id}' ORDER BY project_id ASC """
    try:
        cursor.execute(get_all_project_query)
        conn.commit()
        results = cursor.fetchall()
        projects = [
            {
                "project_id": res[0],
                "project_name": res[1],
                "project_image": f"data:image/jpeg;base64,{base64.b64encode(res[2]).decode('utf-8')}",
                "project_type": res[3],
                "project_owner": res[4],
                "update_date": res[5],
                "project_description": res[6]
            } for res in results
        ]
        projects_sorted = sorted(projects, key=lambda x: x["project_id"])
        return jsonify({
            "data": projects_sorted,
            "message":"Successful get_all_project API",
            "status": "200",
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "messae":"Eror in get_all_project API",
            "status": "500",
        }), 500
 

# Get Project By ID 
def get_project_by_id(id):
    if not id:
        return jsonify({
            "message": "Not enough data to get project",
            "status": "400" 
        }), 400
    user = session['user']
    user_id = user['id']
    get_project_by_id_query = f"""SELECT * FROM "Project_Schema"."Projects" WHERE owner = '{user_id}' AND project_id = {id} ORDER BY project_id ASC"""
    try:
        cursor.execute(get_project_by_id_query)
        result = cursor.fetchone()
        project = [
            {
                "project_id": result[0],
                "project_name": result[1],
                "project_image": f"data:image/jpeg;base64,{base64.b64encode(result[2]).decode('utf-8')}",
                "project_type": result[3],
                "project_owner": result[4],
                "update_date": result[5],
                "project_description": result[6]
            }
        ]
        conn.commit()
        return jsonify({
            "data": project,
            "message": "Successful get_project_by_id API",
            "status": "200",
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error in get_project_by_id API",
            "status": "500",
        }), 500


# Update Project
def update_project(data, image):
    if not data:
        return jsonify({
            "message": "Not enough data to update project",
            "status": "400" 
        }), 400
    user = session['user']
    id = user['id']
    project_name = data['name']
    project_id = data['id']
    project_description= data['description']
    if not image:
        update_project_query = f"""UPDATE "Project_Schema"."Projects"
                                SET project_name = '{project_name}',
                                description = '{project_description}'
                                WHERE project_id = {project_id} AND owner = '{id}';"""
    else:
        project_image = image.read()
        update_project_query = f"""UPDATE "Project_Schema"."Projects"
                                SET project_name = '{project_name}',
                                project_img = {psycopg2.Binary(project_image)},
                                description = '{project_description}'
                                WHERE project_id = {project_id} AND owner = '{id}';"""
    try:
        cursor.execute(update_project_query)
        conn.commit()
        return jsonify({
            "message": "Your project has been updated successfully!!!",
            "status": "200",
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error in get_project_by_id API",
            "status": "500"
        }), 500


# Delete Project  
def delete_project(data):
    if not data:
        return jsonify({
            "message": "Not enough data to get project",
            "status": "400" 
        }), 400
    user = session['user']
    id = user['id']
    delete_project_query = f"""DELETE FROM "Project_Schema"."Projects" WHERE project_id = {data} AND owner = '{id}';"""
    try:
        cursor.execute(delete_project_query)
        conn.commit()
        return jsonify({
            "message": "Delete project successful",
            "status": "200"
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error in delete project API",
            "status": "500"
        }), 500
    
    
    