from flask import Blueprint
from app.services.CertificateManager import CertificateManagerService

bp = Blueprint("ca_manager", __name__)


@bp.route('/create', methods=['POST'])
def create_new_ca():
    ca_manager = CertificateManagerService('HSBC')
    if not ca_manager.check_ca_exists():
    		return 'Certificate Authority Exists'
    ca_manager.create_new_ca()

    return "pong"
