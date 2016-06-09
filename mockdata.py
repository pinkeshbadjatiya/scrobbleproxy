import os
import binascii
import mysql.connector


class db_connect:

        def __init__(self):
                self.__con = None
                self.__cur = None

        def __enter__(self):
                self.__con = mysql.connector.connect(
                                database = 'scrobble_proxy',
                                user = "root",
                                password = "123456789"
                                )
                self.__cur = self.__con.cursor()
                return self.__cur

        def __exit__(self, exception_type, exception_value, traceback):
                self.__con.commit()
                if self.__cur is not None:
                        self.__cur.close()
                if self.__con is not None:
                        self.__con.close()



class User(object):
    @staticmethod
    def load_by_name(name):
        with db_connect() as c:
            c.execute('SELECT * FROM users WHERE name="%s"' % (name))
            row = c.fetchone()
            if row:
                return User(row)
            return None

    @staticmethod
    def load_by_id(id):
        with db_connect() as c:
            c.execute('SELECT * FROM users WHERE id=%s' % (id))
            row = c.fetchone()
            if row:
                return User(row)
            return None

    def __init__(self, row):
        id, name, timestamp = row
        self.id = id
        self.name = name
        self.timestamp = timestamp

    def scrobble(self, timestamp, artist, track, album, albumArtist):
        with db_connect() as cn:
            c.execute('INSERT INTO scrobbles (user, timestamp, artist, track, album, albumArtist) values ("%s","%s","%s","%s","%s","%s");' % (self.id, timestamp, artist, track, album, albumArtist))
        

class Session(object):
    @staticmethod
    def load(session):
        with db_connect() as c:
            c.execute('SELECT * FROM sessions WHERE id="%s"' % (session))
            row = c.fetchone()
            if row:
                return Session(row)
            return None

    @staticmethod
    def create(user):
        session = binascii.b2a_hex(os.urandom(20))
        with db_connect() as c:
            c.execute('INSERT INTO sessions (id, user) VALUES ("%s","%s");' % (session, user.id))
        return Session.load(session)

    def __init__(self, row):
        id, user, timestamp = row
        self.id = id
        self.user = User.load_by_id(user)
        self.timestamp = timestamp


class Token(object):
    @staticmethod
    def load(token):
        with db_connect() as c:
            c.execute('SELECT * FROM tokens WHERE token="%s"' % (token))
            row = c.fetchone()
            if row:
                return Token(row)
            return None

    @staticmethod
    def generate():
        token = binascii.b2a_hex(os.urandom(20))
        with db_connect() as c:
            c.execute('INSERT INTO tokens (token) VALUES ("%s");' % (token))
        return Token.load(token)

    def __init__(self, row):
        token, user, timestamp = row
        self.token = token
        self.timestamp = timestamp
        self.user = None
        if user:
            self.user = User.load_by_id(user)

    def validate(self, user):
        with db_connect() as c:
            c.execute('UPDATE tokens SET user = "%s" WHERE token="%s"' % (user, self.token))

    def consume(self):
        with db_connect() as c:
            c.execute('DELETE FROM tokens WHERE token="%s"' % (self.token))
