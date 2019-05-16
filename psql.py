import psycopg2
import psycopg2.extras


class dbCon():

    def createCon(self):
        d = "postgres"
        u = "postgres"
        p = "root"
        h = "35.244.114.220"
        q = "5432"
        conn = psycopg2.connect(database=d, user=u, password=p, host=h, port=q)
        return conn

    def closeCon(self, conn):
        """defination to create connection

        Arguments:
            conn {psql connection} -- used to create connection for psql
        """
        conn.close()

    def selectQ(self, qs, *argv):
        """def to run and get result of select query

        Arguments:
            qs {string} -- query being executed
            *argv {variable dataTypes arguments} -- query variables

        Returns:
            sql rows -- rows returned by select query
        """
        conn = self.createCon()
        cur = conn.cursor()
        cur.execute(qs, argv)
        rows = cur.fetchall()
        self.closeCon(conn)
        return rows

    def selectQName(self, qs, *argv):
        """def to run and get result of select query

        Arguments:
            qs {string} -- query being executed
            *argv {variable dataTypes arguments} -- query variables

        Returns:
            sql rows -- rows returned by select query
        """
        conn = self.createCon()
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(qs, argv)
        rows = cur.fetchall()
        self.closeCon(conn)
        return rows

    def insUpDel(self, qs, *argv):
        """Def to execute insert, update or delete queries

        Arguments:
            qs {string} -- query being executed

        Returns:
            integer -- number of rows effected
        """
        conn = self.createCon()
        cur = conn.cursor()
        cur.execute(qs, argv)
        conn.commit()
        count = cur.rowcount
        self.closeCon(conn)
        return count
