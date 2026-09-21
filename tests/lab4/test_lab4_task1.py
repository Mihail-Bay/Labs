import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab4" / "task1" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab4_task1", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.engine = lab.create_database("sqlite:///:memory:")
        self.session = Session(self.engine)
        self.addCleanup(self.engine.dispose)
        self.addCleanup(self.session.close)

    def test_full_booking_cycle(self):
        user = lab.add_user(self.session, "Михаил", "m@example.com")
        book = lab.add_book(self.session, "Книга", "Автор", 2)
        booking = lab.create_booking(self.session, user.id, book.id)
        self.assertEqual(book.copies_available, 1)
        self.assertEqual(booking.booking_date, date.today())
        self.assertEqual(booking.user.name, "Михаил")
        self.assertEqual(booking.book.title, "Книга")
        booking_id = booking.id
        lab.delete_booking(self.session, booking_id)
        self.assertEqual(book.copies_available, 2)
        self.assertIsNone(self.session.get(lab.Booking, booking_id))

    def test_unique_email_and_rollback(self):
        lab.add_user(self.session, "Первый", "same@example.com")
        with self.assertRaises(IntegrityError):
            lab.add_user(self.session, "Второй", "same@example.com")
        self.assertEqual(self.session.query(lab.User).count(), 1)
        user = lab.add_user(self.session, "Третий", "new@example.com")
        self.assertIsNotNone(user.id)

    def test_missing_user_book_and_booking(self):
        user = lab.add_user(self.session, "Михаил", "m@example.com")
        book = lab.add_book(self.session, "Книга", "Автор", 1)
        for user_id, book_id in [(999, book.id), (user.id, 999)]:
            with self.subTest(user=user_id, book=book_id):
                with self.assertRaises(ValueError):
                    lab.create_booking(self.session, user_id, book_id)
        with self.assertRaises(ValueError):
            lab.delete_booking(self.session, 999)
        self.assertEqual(book.copies_available, 1)

    def test_no_copies_and_invalid_data(self):
        user = lab.add_user(self.session, "Михаил", "m@example.com")
        book = lab.add_book(self.session, "Книга", "Автор", 0)
        with self.assertRaises(ValueError):
            lab.create_booking(self.session, user.id, book.id)
        self.assertEqual(self.session.query(lab.Booking).count(), 0)
        with self.assertRaises(ValueError):
            lab.add_book(self.session, "Книга", "Автор", -1)
        with self.assertRaises(ValueError):
            lab.add_user(self.session, "", "empty@example.com")


if __name__ == "__main__":
    unittest.main()
