import requests
import json
import os

def main():
	payload = {
		"Certificate" : {
			"Name" : "uade-tp-seginf.edu",
			"Bits" : 2048,
			"ValidFor" : 2,
			"Signer" : "UADE SegInf TP Intermediate"
		}
	}

	url = "http://0.0.0.0:8080/api/v1/certificate_manager/server/create"
	headers = {'content-type': 'application/json'}

	r = requests.post(url=url, data=json.dumps(payload), headers=headers)
	if r.status_code == 201:
		response =  json.loads(r.text)
		certificate_chain = response['certificateChain']
		server_cert = response['certificate']
		server_key = response['key']
		server_name = response['name']
		save_file(certificate_chain, os.environ["CERTIFICATE_CHAIN_FILE"])
		save_file(server_cert, os.environ["CERTIFICATE_FILE"])
		save_file(server_key, os.environ["KEY_FILE"])
	else:
		error = {
			"http_code" : r.status_code,
			"message" : r.text,
			"request" : {
				"url" : r.request.path_url,
				"method" : r.request.method,
				"data" : r.request.body
			}
		}
		print(error)

def save_file(text, file_name):
	with open(file_name, "wt") as file:
		file.write(text)

if __name__ == "__main__":  # only in dev
	main()
