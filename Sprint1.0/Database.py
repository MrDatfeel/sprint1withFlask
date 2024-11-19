import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, ForeignKey, LargeBinary, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модели для таблиц
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15))
    full_name = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Coord(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True)
    latitude = Column(DECIMAL(9, 6), nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)
    height = Column(Integer, nullable=False)


class PerevalAdded(Base):
    __tablename__ = 'pereval_added'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_added = Column(TIMESTAMP, default=datetime.utcnow)
    beauty_title = Column(String(255))
    title = Column(String(255), nullable=False)
    other_titles = Column(Text)
    connect = Column(Text)
    add_time = Column(TIMESTAMP)
    coord_id = Column(Integer, ForeignKey('coords.id'))
    level_winter = Column(String(50))
    level_summer = Column(String(50))
    level_autumn = Column(String(50))
    level_spring = Column(String(50))

    user = relationship("User ", back_populates="perevals")
    coord = relationship("Coord")


class PerevalImage(Base):
    __tablename__ = 'pereval_images'

    id = Column(Integer, primary_key=True)
    pereval_id = Column(Integer, ForeignKey('pereval_added.id'), nullable=False)
    img = Column(LargeBinary, nullable=False)  # Изменено на LargeBinary
    title = Column(String(255), nullable=False)
    date_added = Column(TIMESTAMP, default=datetime.utcnow)

    pereval = relationship("PerevalAdded", back_populates="images")


class PerevalArea(Base):
    __tablename__ = 'pereval_areas'

    id = Column(Integer, primary_key=True)
    id_parent = Column(Integer, ForeignKey('pereval_areas.id'))
    title = Column(Text)


class ActivityType(Base):
    __tablename__ = 'spr_activities_types'

    id = Column(Integer, primary_key=True)
    title = Column(Text)


# Определяем класс для работы с базой данных
class Database:
    def __init__(self):
        # Получаем переменные окружения из .env файла
        db_host = os.getenv('FSTR_DB_HOST')
        db_port = os.getenv('FSTR_DB_PORT')
        db_login = os.getenv('FSTR_DB_LOGIN')
        db_pass = os.getenv('FSTR_DB_PASS')

        # Создаем строку подключения к базе данных
        self.engine = create_engine(f'postgresql://{db_login}:{db_pass}@{db_host}:{db_port}/pereval')

        # Создаем таблицы в базе данных
        Base.metadata.create_all(self.engine)

        # Создаем сессию для работы с базой данных
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, email, phone, full_name):
        session = self.Session()
        new_user = User(email=email, phone=phone, full_name=full_name)
        session.add(new_user)
        session.commit()
        return new_user.id

    def add_coord(self, latitude, longitude, height):
        session = self.Session()
        new_coord = Coord(latitude=latitude, longitude=longitude, height=height)
        session.add(new_coord)
        session.commit()
        return new_coord.id

    def add_pereval(self, user_id, date_added, beauty_title, title, other_titles, connect, add_time, coord_id,
                    level_winter, level_summer, level_autumn, level_spring):
        session = self.Session()
        new_pereval = PerevalAdded(
            user_id=user_id,
            date_added=date_added,
            beauty_title=beauty_title,
            title=title,
            other_titles=other_titles,
            connect=connect,
            add_time=add_time,
            coord_id=coord_id,
            level_winter=level_winter,
            level_summer=level_summer,
            level_autumn=level_autumn,
            level_spring=level_spring
        )
        session.add(new_pereval)
        session.commit()
        return new_pereval.id

    def add_image(self, pereval_id, img_data, title):
        session = self.Session()
        new_image = PerevalImage(pereval_id=pereval_id, img=img_data, title=title)
        session.add(new_image)
        session.commit()
        return new_image.id

    def add_area(self, id_parent, title):
        session = self.Session()
        new_area = PerevalArea(id_parent=id_parent, title=title)
        session.add(new_area)
        session.commit()
        return new_area.id

    def add_activity_type(self, title):
        session = self.Session()
        new_activity_type = ActivityType(title=title)
        session.add(new_activity_type)
        session.commit()
        return new_activity_type.id


# Пример использования класса
if __name__ == "__main__":
    # Создаем объект базы данных
    db = Database()

    # Добавляем пользователя
    user_id = db.add_user('user@email.tld', '79031234567', 'Тест Тестович')

    # Добавляем координаты
    coord_id = db.add_coord(45.3842, 7.1525, 1200)

    # Добавляем перевал
    pereval_id = db.add_pereval(
        user_id=user_id,
        date_added='2022-02-21 14:14:00.720184',
        beauty_title='пер. ',
        title='Пхия',
        other_titles='Триев',
        connect='',
        add_time='2021-09-22 13:18:13',
        coord_id=coord_id,
        level_winter='',
        level_summer='1А',
        level_autumn='1А',
        level_spring=''
    )

    # Добавляем изображение (замените '...' на фактические данные изображения в base64)
    # img_data = decode('...', 'base64') # Пример декодирования изображения
    # image_id = db.add_image(pereval_id=pereval_id, img_data=img_data, title='Седловина')

    # Добавляем область
    area_id = db.add_area(id_parent=None, title='Планета Земля')

    # Добавляем тип активности
    activity_type_id = db.add_activity_type(title='пешком')

    print(f"Пользователь добавлен с ID: {user_id}")
    print(f"Координаты добавлены с ID: {coord_id}")
    print(f"Перевал добавлен с ID: {pereval_id}")
    print(f"Область добавлена с ID: {area_id}")
    print(f"Тип активности добавлен с ID: {activity_type_id}")




