from database.DB_connect import DBConnect
from model.actor import Actor
from model.rating import Rating


class DAO():
    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct r.avg_rating 
                from ratings r 
                order by avg_rating ASC
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllActors(r1, r2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct n.*
                    from names n, role_mapping rm, ratings r
                    where n.id = rm.name_id and rm.movie_id = r.movie_id 
                    and date_of_birth is Not null
                    and r.avg_rating between %s and %s """

        cursor.execute(query, (r1, r2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(r1, r2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select rm1.name_id as Actor1, rm2.name_id as Actor2, sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as Weight
                    from role_mapping rm1, role_mapping rm2, ratings r, names n1, names n2, movie m 
                    where rm1.movie_id = rm2.movie_id and r.movie_id = rm1.movie_id 
                    and m.id = rm1.movie_id and rm2.movie_id = m.id 
                    and n1.id = rm1.name_id and n2.id = rm2.name_id 
                    and rm1.name_id < rm2.name_id 
                    and m.worlwide_gross_income is not null
                    and m.worlwide_gross_income like '$%'
                    and n1.date_of_birth is not null and n2.date_of_birth is not null and r.avg_rating between %s and %s 
                    group by rm1.name_id, rm2.name_id  """

        cursor.execute(query, (r1, r2))

        for row in cursor:
            results.append((row['Actor1'], row['Actor2'], row['Weight']))

        cursor.close()
        conn.close()
        return results
