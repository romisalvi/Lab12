from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct gr.Country 
                    from go_retailers gr 
                    order by gr.Country
                                   """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

        pass

    @staticmethod
    def getRetNat(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select  gr.*
                    from go_retailers gr 
                    where gr.Country=%s
                                           """

        cursor.execute(query,(nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getPeso(id1,id2,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select count(distinct gds.Product_number) as peso
from  go_sales.go_daily_sales gds
join go_sales.go_daily_sales gds2 on gds2.Product_number = gds.Product_number
 where gds.Retailer_code=%s and gds2.Retailer_code = %s and year(gds2.`Date`)=%s and year(gds.`Date`)=%s   
                                           """

        cursor.execute(query,(id1,id2,anno,anno,))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result

