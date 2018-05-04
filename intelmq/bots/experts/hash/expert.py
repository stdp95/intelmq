# -*- coding: utf-8 -*-

from intelmq.lib.bot import Bot


class HashExpertBot(Bot):

    def process(self):
        message = self.receive_message()
        message_hash = message.hash()
        if "extra.message_hash" not in message:
            message.add('extra', {'message_hash': message_hash})
        self.send_message(message)
        self.acknowledge_message()


BOT = HashExpertBot
