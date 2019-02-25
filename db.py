class DB:
    def __init__(self,host="10.2.0.10",user = "katana",passwd = 'YqY2gjijmajn',database = 'gg'):
        import psycopg2

        self.host = "10.2.0.10"
        self.user = "katana"
        self.passwd = 'YqY2gjijmajn'
        self.database = 'gg'

        self.conn = psycopg2.connect("dbname="+database+" user="+user+" host="+host+" password="+passwd)
        self.curs = self.conn.cursor()
        
    def query(self,query):
        self.curs.execute(query)
        data = self.curs.fetchall()
        return data
