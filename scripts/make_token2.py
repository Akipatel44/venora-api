import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services import security
print(security.create_access_token(subject='2', role='subadmin'))
