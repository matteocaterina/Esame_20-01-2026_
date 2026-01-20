from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_soglia(soglia):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a.id, a.name
                from album alb, artist a
                where alb.artist_id = a.id 
                group by a.id 
                having COUNT(*) >= %s
                """
        cursor.execute(query, (soglia,))           ##
        for row in cursor:
            result.append(Artist(row['id'], row['name']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_conn_art_track(soglia):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select a1.id as id1, a2.id as id2, COUNT(distinct t1.genre_id) as w
                    from artist a1, album a11, track t1, track t2, album a12, artist a2
                    where a1.id = a11.artist_id 
                    and a11.id = t1.album_id 
                    and t1.genre_id = t2.genre_id
                    and t2.album_id = a12.id 
                    and a12.artist_id = a2.id 
                    and a1.id < a2.id and a1.id in (
                    select a.id 
                    from artist a, album a1
                    where a.id = a1.artist_id 
                    group by a.id 
                    having COUNT(a.id) >= %s
                    )
                    and a2.id in (
                    select a.id 
                    from artist a, album a1
                    where a.id = a1.artist_id 
                    group by a.id
                    having count(a.id) >= %s
                    )
                    group by a1.id, a2.id
                """
        cursor.execute(query, (soglia,soglia))
        for row in cursor:
            result.append((row['id1'], row['id2'], row['w']))

        cursor.close()
        conn.close()
        return result

    @staticmethod

    def durate():

        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """            
                    select a.id, t.milliseconds/60000 as N
                    from artist a, track t
                    where a.id = t.id 
                """
        cursor.execute(query)  ##
        for row in cursor:
            result[row['id']] = row['N']
        cursor.close()
        conn.close()
        return result

