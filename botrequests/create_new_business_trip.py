import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config import bot, BusinessTripForm, dp
from database import BusinessTrip, Employee, session


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Функция для выхода из текущего состояния
    :param message:
    :param state:
    :return:
    """

    current_state = await state.get_state()

    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await bot.send_message(message.chat.id, 'Вы вышли в главное меню.', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def initial_creating(message) -> None:
    """Получаем команду"""

    await bot.send_message(message.chat.id, "Введите город, в который Вы планируете командировку.")


@dp.message_handler(state=BusinessTripForm.city)
async def process_city(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """

    async with state.proxy() as data:
        data['city'] = message.text
    await BusinessTripForm.next()
    await bot.send_message(message.chat.id, "Введите дату начала командировки")


@dp.message_handler(state=BusinessTripForm.first_date)
async def process_first_date(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """

    async with state.proxy() as data:
        data['first_date'] = message.text
    await BusinessTripForm.next()
    await bot.send_message(message.chat.id, "Введите дату окончания командировки")


@dp.message_handler(state=BusinessTripForm.last_date)
async def process_last_date(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """

    async with state.proxy() as data:
        data['last_date'] = message.text
    await BusinessTripForm.next()
    await bot.send_message(message.chat.id, "Введите сумму транспортных расходов")


@dp.message_handler(state=BusinessTripForm.transfer_expenses)
async def process_transfer_expenses(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """

    async with state.proxy() as data:
        data['transfer_expenses'] = message.text
    await BusinessTripForm.next()
    await bot.send_message(message.chat.id, "Введите сумму представительских расходов")


@dp.message_handler(state=BusinessTripForm.representative_expenses)
async def process_representative_expenses(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """

    async with state.proxy() as data:
        data['representative_expenses'] = message.text

    employee_id = Employee.get_employee(message.from_user.id).id
    with session as db:
        current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
        if current_business_trip is None or not current_business_trip.is_active:
            current_business_trip = BusinessTrip(
                employee_id=employee_id,
                city=data["city"],
                first_date=data["first_date"],
                last_date=data["last_date"],
                transfer=data["transfer_expenses"],
                representative=data["representative_expenses"],
                is_active=True
            )
            db.add(current_business_trip)
            db.commit()
    await state.finish()
    await bot.send_message(message.chat.id, "Командировка создана")
