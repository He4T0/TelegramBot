import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor


import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

counter = 0


class TelegramBot(Bot):
    db = None

    async def _send_message(self, user_id: int, text: str, disable_notification: bool = False) -> bool:
        """
        Safe messages sender

        :param user_id:
        :param text:
        :param disable_notification:
        :return:
        """
        try:
            await self.send_message(user_id, text, disable_notification=disable_notification)
        except exceptions.BotBlocked:
            log.error(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            log.error(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            return await self._send_message(user_id, text)  # Recursive call
        except exceptions.UserDeactivated:
            log.error(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            log.exception(f"Target [ID:{user_id}]: failed")
        else:
            log.info(f"Target [ID:{user_id}]: success")
            return True
        return False

    async def broadcaster(self, msg) -> int:
        """
        Simple broadcaster

        :return: Count of messages
        """
        count = 0
        try:
            for user_id in await self.db.conn.fetch(f"Select id from users"):
                if await self._send_message(user_id["id"], f'{msg}'):
                    count += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
        finally:
            log.info(f"{count} messages successful sent.")
        return count

    async def serve_client(self, reader, writer):
        global counter
        cid = counter
        counter += 1  # Потоко-безопасно, так все выполняется в одном потоке
        print(f'Client #{cid} connected')

        request = await self.read_request(reader)
        if request is None:
            print(f'Client #{cid} unexpectedly disconnected')
        else:
            await self.write_response(writer, request, cid)

    async def read_request(self, reader, delimiter=b'#END'):
        request = bytearray()
        while True:
            chunk = await reader.read(2 ** 10)
            if not chunk:
                # Клиент преждевременно отключился.
                break
            request += chunk
            if delimiter in request:
                return request[:-4]
        return None

    async def write_response(self, writer, response, cid):
        await self.broadcaster(response.decode())
        writer.write(response)
        await writer.drain()
        writer.close()
        print(f'Client #{cid} has been served')

    async def run_server(self, host, port):
        server = await asyncio.start_server(self.serve_client, host, port)
        await server.serve_forever()

