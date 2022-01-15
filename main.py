import random
from os.path import isfile
import json

FILE_QUESTION = 'questions.json'


class GenericQuestion:

    def __init__(self, text_question, author_question, level_question, answer_question,
                 topic_question, is_asked=None):
        self.text_question = text_question
        self.author_question = author_question
        self.level_question = level_question
        self.is_asked = is_asked
        self.answer_question = answer_question
        self.topic_question = topic_question
        self.answer_user = None
        self.scores_question = 0


class Question(GenericQuestion):

    def get_points(self):
        scores_question = int(self.level_question) * 10
        return scores_question

    def is_correct(self):
        if self.answer_user.lower() == self.answer_question:
            return True
        return False

    def build_question(self, number):
        return f'Вопрос {number}\n' \
               f'тема: {self.topic_question}\n' \
               f'сложность: {self.level()}\n' \
               f'{self.text_question} '

    def level(self):
        """
        Функция для превращение числового обозначениф уровня сложности в текстовой
        :return: str
        """
        level = ''
        if int(self.level_question) == 1:
            level = 'Легко'
        elif int(self.level_question) == 2:
            level = 'Средне'
        elif int(self.level_question) == 3:
            level = 'Трудно'
        return level


def load_json():
    """
    Загрузка и проверка файла
    :return: json
    """
    if isfile('questions.json'):
        file = open(FILE_QUESTION)
        return json.load(file)
    else:
        print('Файл не найден')


def get_questions():
    """
    создаем список объектов вопроса
    :return: list
    """
    questions_list = []

    for key in load_json():
        questions_list.append(Question(load_json()[key]['question'],
                                       load_json()[key]['author'],
                                       load_json()[key]['level'],
                                       load_json()[key]['answer'],
                                       load_json()[key]['topic']))
    random.shuffle(questions_list)
    return questions_list


def validate_correct(question):
    """
    Валидация ответа на вопрос
    :param question:
    :return:
    """
    user_points = 0
    if question.is_correct():
        user_points += question.get_points()
        question.is_asked = True
        print(f'Ответ верный, получено {question.get_points()}')
    else:
        question.is_asked = False
        print(f'Ответ не верный! Верный ответ - {question.answer_question}')


def faq():
    """
    Задаем вопросы и вызываем функцтю результата
    :return:
    """
    questions_list = get_questions()
    for number_question, question in enumerate(questions_list):
        print(question.build_question(number_question + 1))
        question.answer_user = input('Введите ваш ответ ')
        validate_correct(question)
    result(questions_list)


def result(questions):
    """
    Выводим результат
    :param questions:
    :return:
    """
    count_question = len(load_json())
    count_correct_answer = 0
    for question in questions:
        if question.is_asked:
            count_correct_answer += 1
    print(f'Вот и все! Отвечено {count_correct_answer} из {count_question}')


def main():
    faq()


if __name__ == '__main__':
    main()
