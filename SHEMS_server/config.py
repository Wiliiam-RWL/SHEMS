class Config(object):
    DATABASE_HOST = 'db-project.clt5dhnemxsz.us-east-2.rds.amazonaws.com'
    DATABASE_NAME = 'shems'
    DATABASE_USER = 'admin'
    DATABASE_PASSWORD = '12345678'
    DATABASE_PORT = '3306'

    # Construct the DATABASE_URI using the individual components
    DATABASE_URI = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

    SECRET_KEY = '123456'  # Remember to set a strong secret key
