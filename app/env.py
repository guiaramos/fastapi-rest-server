# this file represents the variable environment, so in production we should transfer this values to env

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "0a19e92911da2a0d3a5088d3cafc978cf3089ab966c1c5c2b37ac70981c19ee6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_ACCESS_KEY = "todo.access-token"
