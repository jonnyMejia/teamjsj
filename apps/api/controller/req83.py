import psycopg2
from ..db import Database

def selectAll():
    
    db = Database()

    try:
        query = "SELECT id_oferta, descripcion FROM OFERTA_DETALLE LIMIT 100"

        db.cur.execute(query)



    except (Exception, psycopg2.Error) as error:
    
        print("Error in selecting the data:", error)
    
    return db.cur.fetchall()

def selectReq83():

    db = Database()

    try:
        query = """select distinct o.htitulo_cat, o.htitulo from webscraping w inner join oferta o 
                ON (w.id_webscraping = o.id_webscraping)
                WHERE o.id_estado is null
                ORDER BY 1, 2 limit 500"""

        db.cur.execute(query)

    except (Exception, psycopg2.Error) as error:
    
        print("Error in selecting the data:", error)
    
    return db.cur.fetchall()