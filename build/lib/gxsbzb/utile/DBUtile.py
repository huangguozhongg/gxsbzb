# mysql
import pymysql, pymongo, redis, re


# MYsql数据库
class MysqlUtile(object):
    #  连接数据库
    # host:主机名, port:端口号, user:用户名, password:用户密码, db:数据库名
    def __init__(self, host: str, port: int, user: str, password: str, db: str) -> pymysql.connect:
        try:
            # 初始连接
            self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
            print("成功连接数据库！")
        except Exception as e:
            print(e)

    ##  查询数据库（单行）
    # tablename:表名, columns:列名, where:条件, groupby:分组, having:分组条件, orderby:排序, limit:限制
    def fetch_one(self, tablename: str, columns: str = '*', where: str = None, groupby: str = None, having: str = None,
                 orderby: str = None, limit: int = None) -> tuple:
        sql = 'select ' + columns + ' from ' + tablename
        # where
        if where != None and groupby == None and having == None and orderby == None and limit == None:
            sql = sql + ' where ' + where
            ## where groupby
        elif where != None and groupby != None and having == None and orderby == None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby
            ### where groupby having
        elif where != None and groupby != None and having != None and orderby == None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having
            #### where groupby having orderby
        elif where != None and groupby != None and having != None and orderby != None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby
            ##### where groupby having orderby limit
        elif where != None and groupby != None and having != None and orderby != None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby
            #### where groupby having limit
        elif where != None and groupby != None and having != None and orderby == None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having + ' limit ' + str(limit)
            ### where groupby orderby
        elif where != None and groupby != None and having == None and orderby != None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' order by ' + orderby
            #### where groupby orderby limit
        elif where != None and groupby != None and having == None and orderby != None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' order by ' + orderby + ' limit ' + limit
            ### where groupby limit
        elif where != None and groupby != None and having == None and orderby == None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' limit ' + str(limit)
            ## where orderby
        elif where != None and groupby == None and having == None and orderby != None and limit == None:
            sql = sql + ' where ' + where + ' order by ' + orderby
            ### where orderby limit
        elif where != None and groupby == None and having == None and orderby != None and limit != None:
            sql = sql + ' where ' + where + ' order by ' + orderby + ' limit ' + str(limit)
            ## where limit
        elif where != None and groupby == None and having == None and orderby == None and limit != None:
            sql = sql + ' where ' + where + ' limit ' + str(limit)
        # Group by
        elif where == None and groupby != None and having == None and orderby == None and limit == None:
            sql = sql + ' group by ' + groupby
            ## groupby having
        elif where == None and groupby != None and having != None and orderby == None and limit == None:
            sql = sql + ' group by ' + groupby + ' having ' + having
            ### groupby having orderby
        elif where == None and groupby != None and having != None and orderby != None and limit == None:
            sql = sql + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby
            #### groupby having orderby  limit
        elif where == None and groupby != None and having != None and orderby != None and str(limit) != None:
            sql = sql + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby + ' limmit ' + limit
            ## groupby orderby
        elif where == None and groupby != None and having == None and orderby != None and limit == None:
            sql = sql + ' group by ' + groupby + ' order by ' + orderby
            ### groupby orderby limit
        elif where == None and groupby != None and having == None and orderby != None and limit != None:
            sql = sql + ' group by ' + groupby + ' order by ' + orderby + ' limmit ' + str(limit)
            ## groupby limit
        elif where == None and groupby != None and having == None and orderby == None and limit != None:
            sql = sql + ' group by ' + groupby + ' limmit ' + str(limit)
        # orderby
        elif where == None and groupby == None and having == None and orderby != None and limit == None:
            sql = sql + ' order by ' + orderby
            ## orderby limit
        elif where == None and groupby == None and having == None and orderby != None and limit != None:
            sql = sql + ' order by ' + orderby + ' limit ' + str(limit)
        #  limit
        elif where == None and groupby == None and having == None and orderby == None and limit != None:
            sql = sql + ' limit ' + str(limit)
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            return None
        return cur.fetchone()

    #  查询表数据（多行）
    # tablename:表名, columns:列名, where:条件, groupby:分组, having:分组条件, orderby:排序, limit:限制
    def fetch_all(self, tablename: str, columns: str = '*', where: str = None, groupby: str = None, having: str = None,
                 orderby: str = None, limit: int = None) -> list:
        sql = 'select ' + columns + ' from ' + tablename
        # where
        if where != None and groupby == None and having == None and orderby == None and limit == None:
            sql = sql + ' where ' + where
            ## where groupby
        elif where != None and groupby != None and having == None and orderby == None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby
            ### where groupby having
        elif where != None and groupby != None and having != None and orderby == None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having
            #### where groupby having orderby
        elif where != None and groupby != None and having != None and orderby != None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby
            ##### where groupby having orderby limit
        elif where != None and groupby != None and having != None and orderby != None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby
            #### where groupby having limit
        elif where != None and groupby != None and having != None and orderby == None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' having ' + having + ' limit ' + str(limit)
            ### where groupby orderby
        elif where != None and groupby != None and having == None and orderby != None and limit == None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' order by ' + orderby
            #### where groupby orderby limit
        elif where != None and groupby != None and having == None and orderby != None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' order by ' + orderby + ' limit ' + limit
            ### where groupby limit
        elif where != None and groupby != None and having == None and orderby == None and limit != None:
            sql = sql + ' where ' + where + ' group by ' + groupby + ' limit ' + str(limit)
            ## where orderby
        elif where != None and groupby == None and having == None and orderby != None and limit == None:
            sql = sql + ' where ' + where + ' order by ' + orderby
            ### where orderby limit
        elif where != None and groupby == None and having == None and orderby != None and limit != None:
            sql = sql + ' where ' + where + ' order by ' + orderby + ' limit ' + str(limit)
            ## where limit
        elif where != None and groupby == None and having == None and orderby == None and limit != None:
            sql = sql + ' where ' + where + ' limit ' + str(limit)
        # Group by
        elif where == None and groupby != None and having == None and orderby == None and limit == None:
            sql = sql + ' group by ' + groupby
            ## groupby having
        elif where == None and groupby != None and having != None and orderby == None and limit == None:
            sql = sql + ' group by ' + groupby + ' having ' + having
            ### groupby having orderby
        elif where == None and groupby != None and having != None and orderby != None and limit == None:
            sql = sql + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby
            #### groupby having orderby  limit
        elif where == None and groupby != None and having != None and orderby != None and str(limit) != None:
            sql = sql + ' group by ' + groupby + ' having ' + having + ' order by ' + orderby + ' limmit ' + limit
            ## groupby orderby
        elif where == None and groupby != None and having == None and orderby != None and limit == None:
            sql = sql + ' group by ' + groupby + ' order by ' + orderby
            ### groupby orderby limit
        elif where == None and groupby != None and having == None and orderby != None and limit != None:
            sql = sql + ' group by ' + groupby + ' order by ' + orderby + ' limmit ' + str(limit)
            ## groupby limit
        elif where == None and groupby != None and having == None and orderby == None and limit != None:
            sql = sql + ' group by ' + groupby + ' limmit ' + str(limit)
        # orderby
        elif where == None and groupby == None and having == None and orderby != None and limit == None:
            sql = sql + ' order by ' + orderby
            ## orderby limit
        elif where == None and groupby == None and having == None and orderby != None and limit != None:
            sql = sql + ' order by ' + orderby + ' limit ' + str(limit)
        #  limit
        elif where == None and groupby == None and having == None and orderby == None and limit != None:
            sql = sql + ' limit ' + str(limit)
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()
            return []
        return cur.fetchall()

    ## 插入表数据(单行)
    # tablename:表名, values:输入值, columns:列名
    def insert_one(self, tablename: str, values: tuple, columns: str = None) -> bool:
        sql = "insert into " + tablename + " values(" + ",".join(["'%s'"] * len(values)) + ")"
        if columns != None:
            sql = "insert into " + tablename + "(" + columns + ")" + " values(" + ",".join(["'%s'"] * len(values)) + ")"
        sql = sql % values
        sql = sql.replace("'DEFAULT'", "DEFAULT").replace("'NULL'", "NULL")
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
            print('插入成功！')
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        return False

    ## 插入表数据(多行)
    # tablename:表名, values:输入值, columns:列名
    def insert_all(self, tablename: str, values: list, columns: str = None) -> bool:
        sql = "insert into " + tablename + " values(" + ",".join(["%s"] * len(values[0])) + ")"
        if columns != None:
            sql = "insert into " + tablename + "(" + columns + ")" + " values(" + ",".join(["%s"] * len(values[0])) + ")"
        cur = self.conn.cursor()
        try:
            cur.executemany(sql, values)
            self.conn.commit()
            print('插入成功！')
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        return False

    ## 更新表数据
    # tablename:表名, set: 设置值, where:条件
    def update(self, tablename:str, set:str, where:str = None):
        sql = 'update ' + tablename + ' set ' + set
        if where != None:
            sql = sql + ' where ' + where
            self.conn.commit()
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
            print('更新成功！')
        except Exception as e:
            print(e)
            self.conn.rollback()

    ## 删除表数据
    # tablename:表名, where:条件
    def delete(self, tablename: str, where: str = None) -> list:
        sql = 'TRUNCATE TABLE  ' + tablename
        if where != None:
            sql = 'DELETE FROM ' + tablename + ' where ' + where
            self.conn.commit()
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
            print('删除成功！')
        except Exception as e:
            print(e)
            self.conn.rollback()

    ## 关闭数据库连接
    def close(self) -> bool:
        try:
            self.conn.close()
            print('数据库连接已关闭！')
            return True
        except Exception as e:
            print(e)
        return False


# MongoDB数据库
class MongoUtile(object):
    ## 连接数据库
    # host:主机, port:端口, db：数据库
    def __init__(self, host: str = 'localhost', port: int = 27017, db: str = 'test') -> pymongo.MongoClient:
        try:
            self.__client = pymongo.MongoClient(host, port)
            self.__db = self.__client['%s' % db]
            print('成功连接数据库！')
        except Exception as e:
            print(e)

    ## 获取文档（单个）
    # collecion:集合, document:文档
    def find_one(self, collection: str, document: dict = {}):
        return self.__db['%s' % collection].find_one({})

    ## 获取文档（多个）
    # collecion:集合, document:文档
    def find_many(self, collection: str, document: dict = {}):
        return self.__db['%s' % collection].find({})

    ## 插入文档(单个)
    # collecion:集合, document:文档
    def insert_one(self, collection: str, document: dict = {}):
        try:
            self.__db['%s' % collection].insert_one(document)
        except Exception as e:
            print(e)

    ## 插入文档(多个)
    # collecion:集合, document:文档
    def insert_many(self, collection: str, document: list = []):
        try:
            self.__db['%s' % collection].insert_many(document)
        except Exception as e:
            print(e)

    ## 修改文档（单个）
    # collecion:集合, spec:条件, document:文档
    def update_one(self, collection: str, spec={}, document: dict = {}):
        try:
            self.__db['%s' % collection].update_one(spec, {"$set": document})
        except Exception as e:
            print(e)

    ## 修改文档（多个）
    # collecion:集合, spec:条件， document:文档
    def update_many(self, collection: str, spec={}, document: dict = {}):
        try:
            self.__db['%s' % collection].update_many(spec, {"$set": document})
        except Exception as e:
            print(e)

    ## 删除文档（单个）
    # collecion:集合, spec:条件， document:文档
    def delete_one(self, collection: str, spec_or_id={}):
        try:
            self.__db['%s' % collection].delete_one(spec_or_id)
        except Exception as e:
            print(e)

    ## 删除文档（多个）
    # collecion:集合, spec:条件， document:文档
    def delete_many(self, collection: str, spec_or_id={}):
        try:
            self.__db['%s' % collection].delete_many(spec_or_id)
        except Exception as e:
            print(e)

    ## 关闭数据库连接
    def close(self):
        try:
            self.__client.close()
            print("数据库连接关闭！")
        except Exception as e:
            print(e)


# Redis
class RedisUtile(object):
    def __init__(self, host: str = 'localhost', port: int = 6379):
        try:
            pool = redis.ConnectionPool(host=host, port=port)
            self.__r = redis.Redis(connection_pool=pool)
            print('成功连接数据库！')
        except Exception as e:
            print(e)

    ## 添加
    # name:键, values:值
    def add(self, name, values):
        try:
            self.__r.sadd(name, values)
        except Exception as e:
            print(e)

    ## 获取
    # name:键
    def get(self, name):
        return self.__r.smembers(name)