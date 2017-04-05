import MySQLdb

from InstagramAPI import InstagramException
from InstagramAPI.src.InstagramException import ErrorCode


class SettingsMysql(object):
    dbTableName = 'user_settings'

    def __init__(self, username, mysqlOptions):

        self.sets = None
        self.pdo = None
        self.instagramUsername = None

        self.sets = dict()
        self.instagramUsername = username

        if 'db_tablename' in mysqlOptions and mysqlOptions['db_tablename']:
            self.dbTableName = mysqlOptions['db_tablename']

        # if mysqlOptions['pdo']:
        #    # Pre-provided PDO object.
        #    self.pdo = mysqlOptions['pdo']
        # else:
        # We should connect for the user.
        username = mysqlOptions['db_username'] if 'db_username' in mysqlOptions and mysqlOptions[
            'db_username'] else 'root'
        password = mysqlOptions['db_password'] if 'db_password' in mysqlOptions and mysqlOptions['db_password'] else ''
        host = mysqlOptions['db_host'] if 'db_host' in mysqlOptions and mysqlOptions['db_host'] else 'localhost'
        dbName = mysqlOptions['db_name'] if 'db_name' in mysqlOptions and mysqlOptions['db_name'] else 'instagram'

        self.connect(username, password, host, dbName)

        self.autoInstall()
        self.populateObject()

    def maybeLoggedIn(self):
        """
        Does a preliminary guess about whether we're logged in.

        The session it looks for may be expired, so there's no guarantee.

        :rtype: bool
        """
        if (self.get('id') != None) and (self.get('username_id') != None) and (self.get('token') != None):
            return True
        else:
            return False

    def get(self, key, default=None):
        if key == 'sets':
            return self.sets  # Return 'sets' itself which contains all data.

        if self.sets[key]:
            return self.sets[key]

        return default

    def set(self, key, value):
        if (key == 'sets') or (key == 'username'):
            return  # // Don't allow writing to special 'sets' or 'username' keys.

        self.sets[key] = value
        self.Save()

    def Save(self):
        # // Special key where we store what username these settings belong to.
        self.sets['username'] = self.instagramUsername
        bindList = {}

        # // Update if user already exists in db, otherwise insert.
        if 'id' in self.sets and self.sets['id']:
            sql = "update {} set ".format(self.dbTableName)
            bindList['id'] = self.sets['id']
        else:
            sql = "insert into {} set ".format(self.dbTableName)

        # // Add all settings to storage.
        fieldList = []
        for key, value in self.sets.iteritems():
            if key == 'id':
                continue

            fieldList.append("{} = %({})s".format(key, key))
            bindList[key] = value

        sql = sql + ','.join(fieldList) + (' where id=%(id)s' if ('id' in self.sets and self.sets['id']) else '')

        std = self.pdo.cursor()
        try:
            std.execute(sql, bindList)
            self.pdo.commit()
        except MySQLdb.IntegrityError as e:
            print e

        # // Keep track of which database row id the user has been assigned as.
        if not ('id' in self.sets and self.sets['id']):
            self.sets['id'] = std.lastrowid

    def connect(self, username, password, host, dbName):
        try:
            pdo = MySQLdb.connect(host, username, password, dbName)

            # $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
            # $pdo->query('SET NAMES UTF8');
            # $pdo->setAttribute(PDO::ERRMODE_WARNING, PDO::ERRMODE_EXCEPTION);
            self.pdo = pdo

        except Exception as e:
            print e
            raise InstagramException('Cannot connect to MySQL settings adapter.', ErrorCode.INTERNAL_SETTINGS_ERROR)

    def autoInstall(self):

        cursor = self.pdo.cursor()

        # // Detect the name of the MySQL database that PDO is connected to.
        cursor.execute('select database()')
        dbName = cursor.fetchone()[0]

        cursor.execute('SHOW TABLES WHERE tables_in_' + dbName + ' = %s', (self.dbTableName,))

        if cursor.rowcount:
            return True

        cursor.execute('CREATE TABLE `' + self.dbTableName + "` (\
            `id` INT(10) NOT NULL AUTO_INCREMENT,\
            `username` VARCHAR(50) NULL DEFAULT NULL,\
            `version` VARCHAR(10) NULL DEFAULT NULL,\
            `user_agent` VARCHAR(255) NULL DEFAULT NULL,\
            `username_id` BIGINT(20) NULL DEFAULT NULL,\
            `token` VARCHAR(255) NULL DEFAULT NULL,\
            `manufacturer` VARCHAR(255) NULL DEFAULT NULL,\
            `device` VARCHAR(255) NULL DEFAULT NULL,\
            `model` VARCHAR(255) NULL DEFAULT NULL,\
            `device_id` VARCHAR(255) NULL DEFAULT NULL,\
            `phone_id` VARCHAR(255) NULL DEFAULT NULL,\
            `uuid` VARCHAR(255) NULL DEFAULT NULL,\
            `cookies` TEXT NULL,\
            `date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,\
            `last_login` BIGINT NULL DEFAULT 0,\
            PRIMARY KEY (`id`),\
            UNIQUE KEY `idx_username` (`username`)\
            )\
            COLLATE='utf8_general_ci'\
            ENGINE=InnoDB;\
        ")

    def populateObject(self):
        cursor = self.pdo.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from {} where username=%s".format(self.dbTableName), (self.instagramUsername,))

        result = cursor.fetchone()
        if result:
            for key, value in result.iteritems():
                self.sets[key] = value
