from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///nic.db")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Employee(Base):
    """Модель описывающая сотрудника"""

    __tablename__ = 'employee'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    telegram_id = Column('telegram_id', Integer)
    name = Column('name', String(100), nullable=False)
    middle_name = Column('middle_name', String(100), nullable=False)
    last_name = Column('last_name', String(100), nullable=False)
    business_trip = relationship('BusinessTrip', backref="employee")

    def __repr__(self):
        """
        :return (str): Возвращает полное ФИО сотрудника
        """
        return f'{self.last_name} {self.name} {self.middle_name}'

    @classmethod
    def get_employee(cls, telegram_id):
        """
        Получение пользователя по его Telegram ID

        :param telegram_id: Telegram ID пользователя (сотрудника)
        :return: Текущего пользователя
        """
        return session.query(Employee).filter(cls.telegram_id == telegram_id).first()


class BusinessTrip(Base):

    """Модель описывающая командировку"""

    __tablename__ = 'business_trip'

    id = Column('id', Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    city = Column('city', String(100), nullable=False)
    first_date = Column('first_date', String(20), nullable=False)
    last_date = Column('last_date', String(20), nullable=False)
    transfer = Column('transfer', Integer, nullable=False)
    representative = Column('representative', Integer, nullable=False)
    is_active = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return f'{self.city}-{self.first_date}-{self.last_date}'

    @classmethod
    def get_current_business_trip(cls, current_employee):
        """
        Получение текущей командировки

        :param current_employee:
        :return:
        """
        return session.query(BusinessTrip).filter(
            cls.employee_id == current_employee).order_by(BusinessTrip.id.desc()).first()

    @classmethod
    def get_total_expenses(cls):
        """
        Получение общей суммы по затратам на командировку

        :return:
        """
        start_date = datetime.strptime(str(cls.first_date), '%d.%m.%Y')
        end_date = datetime.strptime(str(cls.last_date), '%d.%m.%Y')
        duration_of_business_trip = end_date - start_date
        total_expenses = cls.transfer + cls.representative + (duration_of_business_trip * 1000)
        return total_expenses


Base.metadata.create_all(bind=engine)
