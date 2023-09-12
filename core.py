import aiogram
from dotenv import load_dotenv
from botrequests.create_new_business_trip import initial_creating
from botrequests.edit_business_trip import edit_current_business_trip
from service import WorkDocuments
from config import bot, dp, BusinessTripForm
from database import Employee, BusinessTrip
from aiogram import executor

load_dotenv()


@dp.message_handler(commands=['start'])
async def start_message(message: aiogram.types.Message) -> None:
    """
    Стартовая функция при запуске бота

    :param
        message: telebot.types.Message
        return: None
    """
    current_user_telegram_id = Employee.get_employee(telegram_id=message.from_user.id).telegram_id

    if message.chat.id != current_user_telegram_id:
        await bot.send_message(message.chat.id, "Вы не зарегистрированы! Обратитесь к администратору @biglov_e!")
    else:
        await bot.send_message(message.chat.id,
                               f"Здравствуйте, {Employee.get_employee(telegram_id=message.chat.id)}! "
                               f"Выберите нужный пункт меню!")


@dp.message_handler(commands=['plan_report'])
async def plan_report_message(message: aiogram.types.Message) -> None:
    """
    Функция для получения формы плана-отчета.

    :param message: telebot.types.Message
    :return: None
    """

    current_user_telegram_id = Employee.get_employee(telegram_id=message.from_user.id).telegram_id

    if message.chat.id != current_user_telegram_id:
        await bot.send_message(message.chat.id, "Вы не зарегистрированы! Обратитесь к администратору @biglov_e!")
    else:

        current_employee = Employee.get_employee(message.from_user.id)
        current_business_trip = BusinessTrip.get_current_business_trip(current_employee.id)

        file = WorkDocuments.post_trip_report(
            current_employee.last_name,
            current_business_trip.city,
            current_business_trip.first_date,
            current_business_trip.last_date
        )

        doc_file = open(file, 'rb')
        await bot.send_document(message.chat.id, doc_file)


@dp.message_handler(commands=['for_accounting'])
async def for_accounting_message(message: aiogram.types.Message) -> None:
    """
    Функция для получения заполненного файла для бухгалтерии при подготовке новой командировки.

    :param message: telebot.types.Message
    :return: None
    """

    current_user_telegram_id = Employee.get_employee(telegram_id=message.from_user.id).telegram_id

    if message.chat.id != current_user_telegram_id:
        await bot.send_message(message.chat.id, "Вы не зарегистрированы! Обратитесь к администратору @biglov_e!")
    else:
        current_employee = Employee.get_employee(message.from_user.id)
        current_business_trip = BusinessTrip.get_current_business_trip(current_employee.id)

        file = WorkDocuments.for_accounting(
            current_employee.last_name,
            current_business_trip.city,
            current_business_trip.first_date,
            current_business_trip.last_date,
            current_business_trip.transfer,
            current_business_trip.representative
        )

        doc_file = open(file, 'rb')
        await bot.send_document(message.chat.id, doc_file)


@dp.message_handler(commands=['accounting_report'])
async def accounting_report_message(message: aiogram.types.Message) -> None:
    """
    Функция для получения Авансового отчета по возвращении из командировки.

    :param message: telebot.types.Message
    :return: None
    """

    current_user_telegram_id = Employee.get_employee(telegram_id=message.from_user.id).telegram_id

    if message.chat.id != current_user_telegram_id:
        await bot.send_message(message.chat.id, "Вы не зарегистрированы! Обратитесь к администратору @biglov_e!")
    else:
        current_employee = Employee.get_employee(message.from_user.id)
        current_business_trip = BusinessTrip.get_current_business_trip(current_employee.id)
        file = WorkDocuments.accounting_report(
            current_employee.last_name,
            f"{current_employee.last_name} {current_employee.name} {current_employee.middle_name}",
            current_business_trip.city,
            current_business_trip.first_date,
            current_business_trip.last_date,
            current_business_trip.transfer,
            current_business_trip.representative
        )

        doc_file = open(file, 'rb')
        await bot.send_document(message.chat.id, doc_file)


@dp.message_handler(commands=['create_new_business_trip'])
async def create_new_business_trip(message: aiogram.types.Message) -> None:
    """
    Функция для создания нововй командировки.

    :param message: telebot.types.Message
    :return: None
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
    current_user_telegram_id = Employee.get_employee(telegram_id=message.from_user.id).telegram_id

    if message.chat.id != current_user_telegram_id:
        await bot.send_message(message.chat.id, "Вы не зарегистрированы! Обратитесь к администратору @biglov_e!")
    elif current_business_trip.is_active:
        await bot.send_message(
            message.chat.id,
            f"У Вас есть незакрытая командировка {current_business_trip}",
        )
        await edit_current_business_trip(message)
    else:
        await BusinessTripForm.city.set()
        await initial_creating(message)


if __name__ == "__main__":
    executor.start_polling(dp)
