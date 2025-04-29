from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
import json
import requests
from config import Config
from auth.google_auth import init_google_oauth, login, authorize
from auth.facebook_auth import facebook_login, facebook_callback
from auth.local_auth import local_login, local_register
from controller import project_controller, feature_controller, flood_and_temp_area_controller, layer_type_controller, layer_controller, community_controller, feature_inform_controller
from module import wms

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

google = init_google_oauth(app)

@app.route('/login_google')
def login_google():
    return login(google)

@app.route('/authorize')
def authorize_google():
    return authorize(google)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({"message": "Goodbye!",
                    "statusCode":"200"})

@app.route('/user-info-google')
def user_info():
    # Lấy thông tin người dùng từ session
    user = session.get('user')
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(user)

@app.route('/facebook/login')
def facebook_login_route():
    return facebook_login()

@app.route('/facebook/callback')
def facebook_callback_route():
    code = request.args.get('code')
    if code:
        return facebook_callback(code)

@app.route('/user-info-facebook')
def user_info_fb():
    user_info = session.get('user_data')
    if not user_info:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(user_info)

@app.route('/login', methods=['POST'])
def local_login_route():
    data = request.get_json()
    return local_login(data)

@app.route('/register', methods=['POST'])
def local_register_route():
    data = request.get_json()
    return local_register(data)

@app.route('/get_user_from_session', methods=['GET'])
def get_user_from_session_route():
    if 'user' in session:
        return jsonify(session['user'])
    return jsonify({"message": "User not logged in"}), 401

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'user' in session:
        return jsonify({"logged_in": True, "user": session['user']})
    return jsonify({"logged_in": False}), 401 


# CRUD PROJECT ROUTE

@app.route('/create_project', methods=['POST'])
def create_project_route():
    data = request.form
    image = request.files.get('image')
    return project_controller.create_project(data, image)

@app.route('/get_all_project', methods=['GET'])
def get_all_project_route():
    return project_controller.get_all_project()

@app.route('/get_project_by_id', methods=['GET'])
def get_project_by_id_route():
    data = request.args.get("id")
    return project_controller.get_project_by_id(data)

@app.route('/update_project', methods=['POST'])
def upate_project_route():
    data = request.form
    image = request.files.get('image')
    return project_controller.update_project(data, image)

@app.route('/delete_project', methods=['GET'])
def delete_project_route():
    id = request.args.get("id")
    return project_controller.delete_project(id)

#CRUD LAYER ROUTE
@app.route('/create_default_layer', methods=['POST'])
def create_default_layer_route():
    data = request.data.decode("utf-8").strip()
    return layer_controller.create_default_layer(data[1])

@app.route('/create_file_layer', methods=['POST'])
def create_file_layer_route():
    data = request.form
    file = request.files.get('file')
    return layer_controller.create_file_layer(data, file)

@app.route('/proxy_wms_capabilities', methods=['GET'])
def proxy_wms_capabilities_route():
    wms_url = request.args.get("wms_url")
    return wms.proxy_wms_capabilities(wms_url)

@app.route('/create_wms_layer', methods=['POST'] )
def create_wms_layer_route():
    data = request.form
    return layer_controller.create_wms_layer(data)

@app.route('/create_layer_from_layer', methods=['POST'])
def create_layer_from_layer_route():
    data = request.form
    return layer_controller.create_layer_from_layer(data)

@app.route('/get_all_layer', methods=['GET'])
def get_all_layer_route():
    project_id = request.args.get("project_id")
    return layer_controller.get_all_layer(project_id)

@app.route('/get_layer_by_type', methods=['GET'])
def get_all_layer_by_type_route():
    project_id = request.args.get('project_id')
    layer_type = request.args.get('layer_type')
    return layer_controller.get_all_layer_by_type(project_id, layer_type)

@app.route('/get_layer_by_id', methods=['GET'])
def get_layer_by_id_route():
    layer_id = request.args.get('layer_id')
    return layer_controller.get_layer_by_id(layer_id)

@app.route('/get_max_z_index', methods=['GET'])
def get_max_z_index_route():
    project_id = request.args.get("project_id")
    return layer_controller.get_max_zindex(project_id)

@app.route('/update_status', methods=['POST'])
def update_status_layer_route():
    data = request.get_json()
    layer_id = data.get('id')
    new_status = data.get('status')
    return layer_controller.update_status_layer(layer_id, new_status)

@app.route('/update_priority', methods=['POST'])
def update_priority_layer_route():
    data = request.get_json()
    layer_id = data.get('id')
    priority = data.get('priority')
    print("layer_id", layer_id)
    print("priority", priority)
    return layer_controller.update_priority_layer(layer_id, priority)

@app.route('/update_vector_layer', methods=['POST'])
def update_vector_layer_route():
    data = request.form
    return layer_controller.update_vector_layer(data)

@app.route('/update_tile_layer', methods=['POST'])
def update_tile_layer_route():
    data = request.form
    return layer_controller.update_tile_layer(data)

@app.route('/delete', methods=['GET'])
def delete_layer_route():
    layer_id = request.args.get('layer_id')
    return layer_controller.delete_layer(layer_id)

#CRUD FEATURE ROUTE
@app.route('/get_default_feature', methods=['GET'])
def get_default_feature_route():
    return feature_controller.get_default_feature()

@app.route('/get_feature_by_layer_id', methods=['GET'])
def get_feature_by_layer_id_route():
    layer_id = request.args.get("layer_id")
    return feature_controller.get_feature_by_layer_id(layer_id)

@app.route('/get_default_feature_by_feature_id', methods=['GET'])
def get_default_feature_by_id_route():
    feature_id = request.args.get('feature_id')
    layer_name = request.args.get('layer_name')
    return feature_controller.get_default_feature_by_layer_id(feature_id,layer_name)

@app.route('/get_feature_by_feature_id', methods=['GET'])
def get_feature_by_id_route():
    feature_id = request.args.get('feature_id')
    layer_name = request.args.get('layer_name')
    return feature_controller.get_feature_by_id(feature_id, layer_name)
    

@app.route('/create_draw_feature', methods=['POST'])
def create_draw_features_route():
    data = request.get_json()['body']
    body_data = json.loads(data)
    return feature_controller.create_draw_feature(body_data)

@app.route('/delete_feature', methods=['GET'])
def delete_feature_route():
    feature_id = request.args.get('feature_id')
    return feature_controller.delete_feature(feature_id)


#FLOOD AREA API
@app.route('/get_inform_flood_area', methods=['GET'])
def get_inform_flood_area_route():
    return flood_and_temp_area_controller.get_inform_flood_area()

#CRUD LAYER TYPE ROUTE
@app.route('/get_all_layer_type', methods=['GET'])
def get_all_layer_type_route():
    return layer_type_controller.get_all_layer_type()

#CRUD COMMUNITY ROUTE
@app.route('/create_community', methods=['POST'])
def create_community_route():
    data = request.get_json()
    return community_controller.create_community(data)

@app.route('/get_all_community', methods=['GET'])
def get_all_community_route():
    return community_controller.get_all_community()

@app.route('/delete_community', methods=['POST'])
def delete_community_route():
    data = request.get_json()
    return community_controller.delete_community(data)

# CRUD FEATURE INFORM
@app.route('/create_feature_inform', methods=['POST'])
def create_feature_inform_route():
    data = request.get_json()
    print(data)
    return feature_inform_controller.create_feature_inform(data)

@app.route('/get_feature_inform_by_feature_id', methods=['GET'])
def get_feature_inform_by_id_route():
    feature_id = request.args.get('feature_id')
    layer_name = request.args.get('layer_name')
    return feature_inform_controller.get_feature_inform_by_id(feature_id, layer_name)

@app.route('/update_feature_inform', methods=['PUT'])
def update_feature_inform_route():
    data = request.get_json()
    return feature_inform_controller.update_feature_inform(data)

@app.route('/delete_feature_inform', methods=['DELETE'])
def delete_feature_inform_route():
    data = request.get_json()
    return feature_inform_controller.delete_feature_inform(data)

@app.route('/search_feature_data', methods=['GET'])
def search_data_route():
    title = request.args.get('title')
    print(title)
    return feature_inform_controller.search_title(title)
if __name__ == '__main__':
    app.run(debug=True)