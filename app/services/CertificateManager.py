from OpenSSL import crypto
import os
from uuid import uuid4
from app.errors.certificate import *
from app.models.certificate import Certificate
from app.utils.logger import Logger
from datetime import datetime

class CertificateManagerService:
    def __init__(self, root_config, sign_algorithm, app_path):
        self.app_path = app_path
        self.root_authority_name = root_config['name']
        self.config_root_authority_bit_size = root_config['bit_size']
        self.config_root_authority_valid_for_years = root_config['valid_years']
        
        self.sign_algorithm = sign_algorithm
        
        root_path = f'{self.app_path}/{self.root_authority_name}'
        self.certificate_paths = {
            "root" : root_path,
            "intermediate" : f'{root_path}/intermediate',
            "server" : f'{root_path}/server'
        }
        self.intermediate_authorities = []

        self.create_folders()
        if self.exists_root_certificate_authority():
            self.root_certificate_authority = self.get_root_certificate_authority()
        else:
            self.root_certificate_authority = self.create_root_certificate_authority()

    def create_root_certificate_authority(self):
        try:
            ca_key = crypto.PKey()
            ca_key.generate_key(crypto.TYPE_RSA, self.config_root_authority_bit_size)

            ca_cert = crypto.X509()
            ca_cert.set_version(2)
            ca_cert.set_serial_number(int(uuid4()))

            ca_subj = ca_cert.get_subject()
            ca_subj.commonName = self.root_authority_name

            ca_cert.add_extensions([
                crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=ca_cert),
            ])

            ca_cert.add_extensions([
                crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always,issuer:always', issuer=ca_cert),
                crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
                crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign')
            ])
            ca_cert.set_issuer(ca_subj)
            ca_cert.set_pubkey(ca_key)
            ca_cert.sign(ca_key, self.sign_algorithm)

            ca_cert.gmtime_adj_notBefore(0)
            ca_cert.gmtime_adj_notAfter(self.config_root_authority_valid_for_years*365*24*60*60)
            certificate = Certificate(ca_key, ca_cert, self.root_authority_name, "root")
            self._save_cert_in_file_system(certificate)

            self.root_authority = certificate
            response = {
                "name" : self.root_authority_name,
                "certificate" : crypto.dump_certificate(crypto.FILETYPE_PEM, certificate.cert).decode('ascii'),
                "certificateType": "intermediate"
            }
            return response
        except Exception as e:
            error = f'Create Root CA Error - {self.root_authority_name} - Error: [{e}]'
            Logger.log_error(error)
            raise CreateRootCertificateError(error)

        message = f'Create Root CA - OK - {self.root_authority_name}'
        Logger.log_info(message)


        

    def create_intermediate_ca(self, common_name, bits, validation_years):
        if self.exists_intermediate_certificate_authority(common_name):
            error = f'Intermediate Certificate Authority - {common_name} - Already Exists'
            raise IntermediateCertificateAlreadyExists(error)

        intermediate_key = crypto.PKey()
        intermediate_key.generate_key(crypto.TYPE_RSA, bits)
        intermediate_cert = crypto.X509()
        intermediate_cert.get_subject().commonName = common_name
        intermediate_cert.set_issuer(self.root_certificate_authority.cert.get_subject())
        intermediate_cert.set_pubkey(intermediate_key)
        intermediate_cert.gmtime_adj_notBefore(0)
        intermediate_cert.gmtime_adj_notAfter(validation_years*365*24*60*60)
        caext = crypto.X509Extension(b'basicConstraints', False, b'CA:true')
        intermediate_cert.add_extensions([caext])
        intermediate_cert.set_serial_number(0)
        intermediate_cert.sign(self.root_certificate_authority.key, self.sign_algorithm)

        intermediate_authority = {
            "name" : common_name,
            "key"  : intermediate_key,
            "cert" : intermediate_cert
        }

        certificate = Certificate(intermediate_key, intermediate_cert, common_name, "intermediate")
        self._save_cert_in_file_system(certificate)
        
        response = {
            "name" : common_name,
            "certificate" : crypto.dump_certificate(crypto.FILETYPE_PEM, certificate.cert).decode('ascii'),
            "certificateType": "intermediate"
        }

        self.intermediate_ca = certificate
        return response

    def create_server_certificate(self, common_name, intermediate_name, bits, validation_years):
        if self.exists_intermediate_certificate_authority(intermediate_name):
            intermediate_cert = self.get_intermediate_certificate(intermediate_name)
        else:
            error = f'Intermediate Certificate Authority - {intermediate_name} - Not Found'
            raise IntermediateCertificateNotFound(error)

        server_key = crypto.PKey()
        server_key.generate_key(crypto.TYPE_RSA, bits)
        server_cert = crypto.X509()
        server_cert.get_subject().commonName = common_name
        server_cert.set_issuer(intermediate_cert.cert.get_subject())
        server_cert.set_pubkey(server_key)
        server_cert.gmtime_adj_notBefore(0)
        server_cert.gmtime_adj_notAfter(validation_years*365*24*60*60)
        server_cert.add_extensions([crypto.X509Extension(b'basicConstraints', True, b'CA:false')])
        server_cert.set_serial_number(0)
        server_cert.sign(intermediate_cert.key, self.sign_algorithm)
        
        certificate = Certificate(server_key, server_cert, common_name, "server")
        self._save_cert_in_file_system(certificate)
        
        message = f'Server Certificate Create - OK - {common_name}'
        Logger.log_info(message)

        root_cert_ascii = crypto.dump_certificate(crypto.FILETYPE_PEM, self.root_certificate_authority.cert).decode('ascii')
        intermediate_cert_ascii = crypto.dump_certificate(crypto.FILETYPE_PEM, intermediate_cert.cert).decode('ascii')
        response = {
            "name" : common_name,
            "key": crypto.dump_privatekey(crypto.FILETYPE_PEM, certificate.key).decode('ascii'),
            "certificate" : crypto.dump_certificate(crypto.FILETYPE_PEM, certificate.cert).decode('ascii'),
            "certificateType": "server",
            "certificateChain" : root_cert_ascii + intermediate_cert_ascii
        }
        return response

    def _save_cert_in_file_system(self, certificate):
        try:
            key_file, crt_file = self.path_file_certificate_builder(certificate.name, certificate.cert_type)

            with open(crt_file, "wt") as file:
                cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, certificate.cert).decode('ascii')
                file.write(cert_str)
            with open(key_file, "wt") as file:
                key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, certificate.key).decode('ascii')
                file.write(key_str)
        except Exception as e:
            error = f'Save Certificate - Name: {certificate.name} - Type: {certificate.cert_type} - Error [{e}]'
            Logger.log_error(error)
            raise SaveCertificateInFileSystemError(error)
        
        message = f'Save Certificate - Name: {certificate.name} - Type: {certificate.cert_type} - OK'
        Logger.log_info(message)

    def create_folders(self):
        try:
            if not os.path.isdir(self.app_path):
                os.mkdir(self.app_path, 755)
                message = f'Create Folder {self.app_path} - OK'
                Logger.log_info(message)

            for path in self.certificate_paths:
                path = self.certificate_paths.get(path)
                if not os.path.isdir(path):
                    os.mkdir(path, 755)
                    message = f'Create Folder {path} - OK'
                    Logger.log_info(message)

        except Exception as e:
            error = f'Create Folders Error [{e}]'
            Logger.log_error(error)
            raise CreateFolderError(error)

    def exists_root_certificate_authority(self):
        key_root, crt_root = self.path_file_certificate_builder(self.root_authority_name, "root")

        if os.path.isfile(key_root) and os.path.isfile(crt_root):
            message = f'Root CA - Found - {self.root_authority_name}'
            Logger.log_info(message)
            return True

        warning = f'Root CA - Not Found - {self.root_authority_name}'
        Logger.log_warning(warning)

    def exists_intermediate_certificate_authority(self, name):
        key_file, crt_file = self.path_file_certificate_builder(name, "intermediate")

        if os.path.isfile(key_file) and os.path.isfile(crt_file):
            return True
    
    def load_certificate_from_file_system(self, name, cert_type):
        try:
            key_file, crt_file = self.path_file_certificate_builder(name, cert_type)
            
            st_cert=open(crt_file, 'rt').read()
            cert=crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)
            
            st_key=open(key_file, 'rt').read()
            key=crypto.load_privatekey(crypto.FILETYPE_PEM, st_key)

            return key, cert
        except Exception as e:
            error = f'LoadCertificate - {name} - Error [{e}]'
            Logger.log_error(error)
            raise LoadCertificateFromFileSystemError(error)

    def get_root_certificate_authority(self):
        key, cert = self.load_certificate_from_file_system(self.root_authority_name, "root")
        message = f'Load Root CA - OK'
        Logger.log_info(message)

        return Certificate(key, cert, self.root_authority_name, "root")

    def get_intermediate_certificate(self, name):
        key, cert = self.load_certificate_from_file_system(name, "intermediate")
        message = f'Load Intermediate CA - {name} - OK'
        Logger.log_info(message)

        return Certificate(key, cert, name, "intermediate")

    def path_file_certificate_builder(self, name, cert_type):
        path = self.certificate_paths.get(cert_type)
        if path:
            crt_file = f'{path}/{name}.crt'
            key_file = f'{path}/{name}.key'

            return key_file, crt_file

