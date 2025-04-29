from flask import Flask, request, jsonify, Response
import requests

def proxy_wms_capabilities(wms_url):
    
    if not wms_url:
        return jsonify({
            "error": "No WMS URL provided",
            "status": '200',
            }), 400

    capabilities_url = f"{wms_url}?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0"
    try:
        response = requests.get(capabilities_url, timeout=10)
        return Response(response.content, mimetype='text/xml')
    
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500