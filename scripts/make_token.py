from app.services import security
# generate token for user id 2 with role 'subadmin'
print(security.create_access_token(subject='2', role='subadmin'))
