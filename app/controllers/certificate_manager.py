from flask import Blueprint
from app.services.CertificateManager import CertificateManagerService
from flask import Response
from flask import request
import json
from app.errors.parse_request import ParseRequestError

bp = Blueprint("ca_manager", __name__)

mime_type = 'application/json'

@bp.route('/create', methods=['POST'])
def create_new_ca():
	try:
		name, bits, valid_for = parse_create_ca_request(request)
	except ParseRequestError as e:
		return Response(json.dumps({"message" : e.error_desc}), status=400, mimetype=mime_type)
    
	ca_manager = CertificateManagerService(name)
	if ca_manager.check_ca_exists():
		return Response(json.dumps({"message" : "Certificate Authority Exists"}), status=409, mimetype=mime_type)
    
	ca_manager.create_new_ca(bits=bits, validation_years=valid_for)
	return Response(json.dumps({"message" : f'CertificateAuthority - {name} created'}), status=201, mimetype=mime_type)

def parse_create_ca_request(request):
	try:
		json_request = request.get_json(force=True)
		name = str(json_request['CertificateAuthority']['Name'])
		bits = int(json_request['CertificateAuthority']['Bits'])
		valid_for = int(json_request['CertificateAuthority']['ValidFor'])
	
		if name and bits and valid_for:
	  		return name, bits, valid_for
	except Exception as e:
		raise ParseRequestError("Invalid Parameters")