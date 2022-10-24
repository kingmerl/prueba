
class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
class DevelopmentConfig(Config):
    #DEBUG=True
    #MYSQL_HOST ='localhost'
    #MYSQL_USER = 'root'
    #MYSQL_PASSWORD = ''
    #MYSQL_DB = '1107p1'
    DEBUG=True
    MYSQL_HOST ='b10gwjscmkvpdkeu9pfx-mysql.services.clever-cloud.com'
    MYSQL_USER = 'ukcxcpmdhcyncprw'
    MYSQL_PASSWORD = 'QI0IElFeN0PCtnQGUwgP'
    MYSQL_DB = 'b10gwjscmkvpdkeu9pfx'
    
config={
    'development': DevelopmentConfig
}