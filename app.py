import os
import pickle
from random import randint
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.orm as so
from alchemical import Alchemical, Model
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

encryption_key = os.environ['ENCRYPTION_KEY']
db = Alchemical('sqlite:///db.sqlite')


class Encrypted(sa.TypeDecorator):
    impl = sa.Text
    cache_ok = True

    def __init__(self, encryption_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryption_key = encryption_key
        self.fernet = Fernet(encryption_key.encode())

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = self.fernet.encrypt(pickle.dumps(value)).decode()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = pickle.loads(self.fernet.decrypt(value.encode()))
        return value


class User(Model):
    __tablename__ = 'users'
    id: so.Mapped[UUID] = so.mapped_column(primary_key=True, default=uuid4)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    credit_card: so.Mapped[dict[str, str]] = so.mapped_column(Encrypted(encryption_key))


def main():
    # create the database tables
    db.create_all()

    # add a user
    with db.begin() as session:
        name = input('Enter name: ')
        fake_credit_card = {
            'number': f'4111 1111 1111 {randint(1000, 9999)}',
            'expiry': f'{randint(1, 12)}/{randint(21, 30)}',
            'cvv': f'{randint(100, 999)}',
        }
        user = User(name=name, credit_card=fake_credit_card)
        session.add(user)

    # retrieve all users
    with db.Session() as session:
        for user in session.scalars(User.select()):
            print(f'\nName: {user.name}')
            print(f'Credit Card: {user.credit_card['number']}')
            print(f'Expiration: {user.credit_card['expiry']}')


if __name__ == '__main__':
    main()
