from flask import Blueprint
from app.services.CertificateManager import CertificateManagerService
from flask import Response
from flask import request
import json
from app.errors.parse_request import ParseRequestError
from app.errors.certificate import *
from app.config.CertificateManagerConfig import Config
from app.config.CertificateManagerConfig import Config
from app.services.CertificateManager import CertificateManagerService

config  = Config()
ca_manager = CertificateManagerService(config.root_authority_conf, config.sign_algorithm, config.app_path)

bp = Blueprint("certificate_manager", __name__)

mime_type = 'application/json'

@bp.route('server/create', methods=['POST'])
def create_server_certificate():
	try:
		name, bits, valid_for, intermediate_name, export_format = parse_create_server_certificate_request(request)
	except ParseRequestError as e:
		return Response(json.dumps({"message" : e.error_desc}), status=400, mimetype=mime_type)
    
	try:
		ca_manager.create_server_certificate(name, intermediate_name, bits, valid_for, export_format)
	except IntermediateCertificateNotFound as e:
		return Response(json.dumps({"message" : e.error_desc}), status=400, mimetype=mime_type)
	except SaveCertificateInFileSystemError as e:
		return Response(json.dumps({"message" : e.error_desc}), status=400, mimetype=mime_type)
		
	return Response(json.dumps({"message" : f'Certificate Server - {name} - CREATED'}), status=201, mimetype=mime_type)

def parse_create_server_certificate_request(request):
	try:
		json_request = request.get_json(force=True)
		name = str(json_request['Certificate']['Name'])
		bits = int(json_request['Certificate']['Bits'])
		valid_for = int(json_request['Certificate']['ValidFor'])
		intermediate_name = str(json_request['Certificate']['Signer'])
		export_format = str(json_request['Certificate']['Format'])
	
		if name and bits and valid_for and intermediate_name and export_format:
	  		return name, bits, valid_for, intermediate_name, export_format
	except Exception as e:
		raise ParseRequestError("Invalid Parameters")


@bp.route('intermediate/create', methods=['POST'])
def create_intermediate_authority():
	try:
		name, bits, valid_for = parse_create_intermediate_authority(request)
	except ParseRequestError as e:
		return Response(json.dumps({"message" : e.error_desc}), status=400, mimetype=mime_type)
    
	try:
		ca_manager.create_intermediate_ca(name, bits, valid_for)
	except IntermediateCertificateAlreadyExists as e:
		return Response(json.dumps({"message" : e.error_desc}), status=409, mimetype=mime_type)
	except SaveCertificateInFileSystemError as e:
		return Response(json.dumps({"message" : e.error_desc}), status=400, mimetype=mime_type)
		
	return Response(json.dumps({"message" : f'Intermediate Certificate Authority - {name} - CREATED'}), status=201, mimetype=mime_type)

def parse_create_intermediate_authority(request):
	try:
		json_request = request.get_json(force=True)
		name = str(json_request['IntermediateCertificateAuthority']['Name'])
		bits = int(json_request['IntermediateCertificateAuthority']['Bits'])
		valid_for = int(json_request['IntermediateCertificateAuthority']['ValidFor'])
	
		if name and bits and valid_for:
	  		return name, bits, valid_for
	except Exception as e:
		raise ParseRequestError("Invalid Parameters")