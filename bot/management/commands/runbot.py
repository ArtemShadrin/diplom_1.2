from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal
from bot.management.commands.bot_commands import BotCommands


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.offset = 0

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bot start handling...'))

        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message) -> None:
        tg_user, _ = TgUser.objects.get_or_create(chat_id=msg.msg_from.id, defaults={'username': msg.msg_from.username})
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(msg.msg_from.id, text=f'Ваш код верификации: {tg_user.verification_code}')
        else:
            self.handle_auth_user(tg_user, msg)

    def handle_auth_user(self, tg_user: TgUser, msg: Message) -> None:
        bot_commands = BotCommands(tg_user=tg_user, tg_client=self.tg_client)
        if msg.text and msg.text.startswith('/'):
            match msg.text:
                case '/goals':
                    bot_commands.case_goals(msg=msg)
                case '/create':
                    self.offset = bot_commands.create_goal(offset=self.offset)
                case _:
                    bot_commands.case_comand_empty(msg=msg)

        else:
            self.tg_client.send_message(
                msg.msg_from.id, 'Некорректная команда, задайте команду через "/"')
