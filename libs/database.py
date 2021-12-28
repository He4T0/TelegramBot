import asyncpg
from credentials import *

cred = {"user": db_user, "password": db_password, "database": db_name, "host": db_host}


# def db_connection(**kwargs):
#     """
#     @db_connection(user="...", password="...", database="...", host="...")
#     getData(connection):
#         await = connection.fetch("SELECT * FROM ...")
#     """

#     def _wrapper(func):
#         async def wrapper(*args):
#             connection = await asyncpg.connect(**kwargs)
#             result = await func(*args, connection=connection)
#             await connection.close()
#             return result

#         return wrapper

#     return _wrapper


def db_connection(**kwargs):
    """
    @db_connection(user="...", password="...", database="...", host="...")
    getData(connection):
        await = connection.fetch("SELECT * FROM ...")
    """

    def _wrapper(func):
        async def wrapper(*args, **params):
            connection = await asyncpg.connect(**kwargs)
            params["connection"] = connection
            result = await func(*args, **params)
            await connection.close()
            return result

        return wrapper

    return _wrapper

class DataBase:

    @db_connection(**cred)
    async def get_all_id(self, connection):
        return await connection.fetch(f"Select id from users")

    @db_connection(**cred)
    async def add_user(self, data, connection):
        await connection.fetch(
            f"""INSERT into users (id, is_bot, first_name, last_name, group_id, language_code) 
            Values({data["id"]},{data["is_bot"]},'{data["first_name"]}', '{data["last_name"]}', '3', '{data["language_code"]}')"""
        )
        await connection.fetch(
            f"""INSERT into subscribes (uid, debug, from_users, result_tests) 
            Values({data["id"]}, '0', '0', '0')"""
        )

    @db_connection(**cred)
    async def get_user(self, id, connection):
        if type(id) == int:
            return await connection.fetch(f"Select * from users where id = {id}")
        elif type(id) == tuple:
            return await connection.fetch(f"Select * from users where id in {id}")


    @db_connection(**cred)
    async def get_attrForColumn(sels, columns: str, table: str, connection, param=None):
        if param is None:
            return await connection.fetch(f"Select {columns} from {table}")
        else:
            # print(f"Select {columns} from {table} where {param}")
            return await connection.fetch(f"Select {columns} from {table} where {param}")

    @db_connection(**cred)
    async def updateData(sels, column, table, param, where, id, connection):
        return await connection.fetch(f"UPDATE {table} SET {column}='{param}' where {where}={id}")


    @db_connection(**cred)
    async def fetch(self, request: str, connection):
        return await connection.fetch(request)