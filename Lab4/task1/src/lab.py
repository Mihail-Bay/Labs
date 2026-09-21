from datetime import date
from pathlib import Path
from sqlalchemy import (
    create_engine, Column, Integer, String, Date, ForeignKey,
    CheckConstraint, event,
)
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    bookings = relationship("Booking", back_populates="user")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, nullable=False, default=0)
    bookings = relationship("Booking", back_populates="book")
    __table_args__ = (CheckConstraint("copies_available >= 0"),)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    booking_date = Column(Date, nullable=False, default=date.today)
    user = relationship("User", back_populates="bookings")
    book = relationship("Book", back_populates="bookings")


def create_database(url):
    engine = create_engine(url)

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, record):
        # SQLite требует явно включить проверку внешних ключей.
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    return engine


def save(session):
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise


def add_user(session, name, email):
    if not name.strip() or not email.strip():
        raise ValueError("Имя и email не должны быть пустыми")
    user = User(name=name, email=email)
    session.add(user)
    save(session)
    return user


def add_book(session, title, author, copies):
    if not title.strip() or not author.strip() or copies < 0:
        raise ValueError("Неверные данные книги")
    book = Book(title=title, author=author, copies_available=copies)
    session.add(book)
    save(session)
    return book


def create_booking(session, user_id, book_id):
    user = session.get(User, user_id)
    book = session.get(Book, book_id)
    if user is None or book is None:
        raise ValueError("Пользователь или книга не найдены")
    if book.copies_available == 0:
        raise ValueError("Нет свободных экземпляров")
    booking = Booking(user_id=user_id, book_id=book_id)
    book.copies_available -= 1
    session.add(booking)
    save(session)
    return booking


def delete_booking(session, booking_id):
    booking = session.get(Booking, booking_id)
    if booking is None:
        raise ValueError("Бронирование не найдено")
    booking.book.copies_available += 1
    session.delete(booking)
    save(session)


def main():
    folder = Path(__file__).resolve().parent.parent
    lines = (folder / "txt/input.txt").read_text(
        encoding="utf-8").splitlines()
    name, email = lines[0].split(";")
    title, author, copies = lines[1].split(";")
    db = folder / "txt/library.db"
    engine = create_database("sqlite:///" + db.as_posix())
    try:
        with Session(engine) as session:
            user = session.query(User).filter_by(email=email).first()
            if user is None:
                user = add_user(session, name, email)
            book = add_book(session, title, author, int(copies))
            print("До бронирования:", book.copies_available)
            booking = create_booking(session, user.id, book.id)
            print("Бронь:", booking.id, booking.booking_date)
            print("После бронирования:", book.copies_available)
            delete_booking(session, booking.id)
            print("После удаления:", book.copies_available)
            for item in session.query(Book).all():
                print(item.id, item.title, item.copies_available)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
