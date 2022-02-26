# POST Create user
# PUT Update user (must be logged in as this user)
# DELETE Delete user by id (must be logged in as this user)
# Params:
# @ username : string
# @ firstName : string
# @ lastName : string
# @ email : string
# @ password : string

URL_USER = '/user/'

# GET Get user id you are authorizes as OR get 0 if not authorized
URL_AUTH = '/user/auth'

# POST Logs user into the system
# Params:
# @ email : string
# @ password : string
URL_LOGIN = "/user/login"

