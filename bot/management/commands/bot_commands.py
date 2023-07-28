from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, GoalCategory


class BotCommands:
    def __init__(self, tg_user: TgUser, tg_client: TgClient):
        self.tg_user = tg_user
        self.tg_client = tg_client

    def case_goals(self, msg: Message):
        """
        Выборка категорий пользователя
        """
        goals = Goal.objects.filter(
            user=self.tg_user.user,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

        goals_str: list[str] = [
            f'{goal.id} {goal.title}\n'
            for goal in goals
        ]
        if goals_str:
            self.tg_client.send_message(msg.msg_from.id, '\n'.join(goals_str))
        else:
            self.tg_client.send_message(msg.msg_from.id, 'Цели не найдены')

    def create_goal(self, offset) -> int:
        """
        Создание цели
        """
        self.goal_category: GoalCategory
        self.goal_title: str
        self.goal_description: str

        categories = GoalCategory.objects.filter(user_id=self.tg_user.user_id,
                                                 is_deleted=False)
        dict_of_categories = {item.title: item for item in categories}
        text = f''
        for category in categories:
            text += f'{category.title}\n'
        message_text = f'Выберите категорию: \n{text}\n Для отмены выберите /cancel'
        self.tg_client.send_message(self.tg_user.chat_id, message_text)

        flag = True
        while flag:
            category, offset = self.processing_an_empty_field(offset=offset)
            if category in dict_of_categories:
                self.goal_category = dict_of_categories.get(category)
                flag = False
            elif category == '/cancel':
                self.tg_client.send_message(self.tg_user.chat_id, 'Создание цели отменено.')
                return offset
            else:
                self.tg_client.send_message(self.tg_user.chat_id, "Такой категории не существует! \n "
                                                                  "Выберите категорию еще раз:\n "
                                                                  "Для отмены выберите /cancel")

        self.tg_client.send_message(self.tg_user.chat_id, 'Введите название цели\n'
                                                          'Для отмены выберите /cancel')
        self.goal_title, offset = self.processing_an_empty_field(offset=offset)
        if self.goal_title == '/cancel':
            self.tg_client.send_message(self.tg_user.chat_id, 'Создание цели отменено.')
            return offset

        self.tg_client.send_message(self.tg_user.chat_id, 'Введите описание цели \n'
                                                          'Для отмены выберите /cancel')
        self.goal_description, offset = self.processing_an_empty_field(offset=offset)
        if self.goal_description == '/cancel':
            self.tg_client.send_message(self.tg_user.chat_id, 'Создание цели отменено.')
            return offset

        goal = Goal(
            title=self.goal_title,
            category=self.goal_category,
            description=self.goal_description,
            user=self.tg_user.user)
        goal.save()
        self.tg_client.send_message(self.tg_user.chat_id, f'Цель создана: #{goal.id} {goal.title}')
        return offset

    def processing_an_empty_field(self, offset: int) -> (str, int):
        """
        Обрабатываем пустое поле
        """
        flag = True
        text: str = ''
        while flag:
            response = self.tg_client.get_updates(offset=offset)
            for item in response.result:
                offset = item.update_id + 1
                text = item.message.text
                flag = False
        return text, offset

    def case_command_empty(self, msg: Message):
        """
        Обрабатываем пустую команду
        """
        self.tg_client.send_message(msg.msg_from.id,
                                    'Некорректная команда, выберите команду: \n/goals \n/create')
