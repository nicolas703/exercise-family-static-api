"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(_name_)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/members/<int:member_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def members(member_id=None):

    if request.method == "GET":
        if member_id is None:
            return jsonify(jackson_family.get_all_members()), 200

        else:
            jack = jackson_family.get_member(member_id)
            if not jack:
                return jsonify({"msg":"this ID not exist"}), 400
            return jsonify(jack), 200


    elif request.method == "POST":
        idd = jackson_family._generateId()
        name = request.json.get("name", "")
        if not name:
            return jsonify({"msg": "name is required"}), 400
        new_member = {
            "id": idd,
            "first_name": name,
            "last_name": "Jackson"
        }
        add = jackson_family.add_member(new_member)
        return jsonify(jackson_family.get_all_members()), 200


    elif request.method == "DELETE":
        jack = jackson_family.delete_member(member_id)
        if not jack:
            return jsonify({"msg":"this ID not exist"}), 400
        return jsonify(jackson_family.get_all_members()), 200
    

@app.route("/example", methods=["GET","POST"])
def example():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(members), 200

# this only runs if `$ python src/app.py` is executed
if _name_ == '_main_':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)