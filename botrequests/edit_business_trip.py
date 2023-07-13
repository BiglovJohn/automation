import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import bot, dp, BusinessTripEditForm
from database import Employee, BusinessTrip, session


@dp.message_handler(lambda message: message.text in ["Выйти"])
async def close_current_business_trip(message: types.Message) -> None:
    """
    Эмитация выхода из режима редактирования

    :param message:
    :return: None
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
    current_business_trip.is_active = False
    session.commit()

    await bot.send_message(
        message.chat.id,
        f"Командировка {current_business_trip} отредактирована!",
        reply_markup=types.ReplyKeyboardRemove())


async def edit_current_business_trip(message: types.Message) -> None:
    """

    :param message:
    :return:
    """
    await asyncio.sleep(0.5)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Редактировать", "Закрыть")
    await bot.send_message(
        message.chat.id,
        "Выберите действие для текущей командировки",
        reply_markup=markup,
        parse_mode="HTML"
    )


@dp.message_handler(lambda message: message.text in ["Редактировать"])
async def choose_the_parameter(message: types.Message) -> None:
    """
    Проверяем запрос пользователя и перенаправляем по нужному сценарию:
        - редактировать текущую командировку
        - закрыть командировку

    :param message:
    :return: None
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(
        "Город",
        "Дату начала",
        "Дату окончания",
        "Транспортные расходы",
        "Представительские расходы",
        "Выйти"
    )
    await bot.send_message(
        message.chat.id,
        "Какой параметр Вы планируете отредактировать?",
        reply_markup=markup,
        parse_mode="HTML"
    )


@dp.message_handler(lambda message: message.text in ["Закрыть"])
async def close_current_business_trip(message: types.Message) -> None:
    """
    Проверяем запрос пользователя и перенаправляем по нужному сценарию:
        - редактировать текущую командировку
        - закрыть командировку

    :param message:
    :return: None
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
    current_business_trip.is_active = False
    session.commit()

    await bot.send_message(message.chat.id, f"Командировка {current_business_trip} закрыта! Можете создать новую!")


@dp.message_handler(lambda message: message.text in ["Город", "Дату начала", "Дату окончания", "Транспортные расходы",
                                                     "Представительские расходы"])
async def editing(message: types.Message) -> None:
    """
    Редактирование города командировки

    :param message:
    :return: None
    """

    if message.text == "Город":
        await bot.send_message(
            message.chat.id,
            "Введите город",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await BusinessTripEditForm.city.set()

    elif message.text == "Дату начала":
        await bot.send_message(
            message.chat.id,
            "Введите актуальную дату начала командировки",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await BusinessTripEditForm.first_date.set()

    elif message.text == "Дату окончания":
        await bot.send_message(
            message.chat.id,
            "Введите актуальную дату окончания командировки",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await BusinessTripEditForm.last_date.set()

    elif message.text == "Транспортные расходы":
        await bot.send_message(
            message.chat.id,
            "Введите актуальную сумму транспортных расходов",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await BusinessTripEditForm.transfer_expenses.set()

    elif message.text == "Представительские расходы":
        await bot.send_message(
            message.chat.id,
            "Введите актуальную сумму представительских расходов",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await BusinessTripEditForm.representative_expenses.set()


@dp.message_handler(state=BusinessTripEditForm.city)
async def edit_city(message: types.Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    with session as db:
        current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
        current_business_trip.city = message.text
        db.commit()
    await message.reply("Сохранил")
    await state.finish()
    await choose_the_parameter(message)


@dp.message_handler(state=BusinessTripEditForm.first_date)
async def edit_city(message: types.Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    with session as db:
        current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
        current_business_trip.first_date = message.text
        db.commit()
    await message.reply("Сохранил")
    await state.finish()
    await choose_the_parameter(message)


@dp.message_handler(state=BusinessTripEditForm.last_date)
async def edit_city(message: types.Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    with session as db:
        current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
        current_business_trip.last_date = message.text
        db.commit()
    await message.reply("Сохранил")
    await state.finish()
    await choose_the_parameter(message)


@dp.message_handler(state=BusinessTripEditForm.transfer_expenses)
async def edit_city(message: types.Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    with session as db:
        current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
        current_business_trip.transfer = message.text
        db.commit()
    await message.reply("Сохранил")
    await state.finish()
    await choose_the_parameter(message)


@dp.message_handler(state=BusinessTripEditForm.representative_expenses)
async def edit_city(message: types.Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """

    employee_id = Employee.get_employee(message.from_user.id).id
    with session as db:
        current_business_trip = BusinessTrip.get_current_business_trip(employee_id)
        current_business_trip.representative = message.text
        db.commit()
    await message.reply("Сохранил")
    await state.finish()
    await choose_the_parameter(message)
