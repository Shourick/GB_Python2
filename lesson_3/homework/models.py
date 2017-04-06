import os
import sqlite3
import json
import datetime
from peewee import *

BASE_DIR = os.path.dirname(__file__)
DB_FILE_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
DATA_BASE = SqliteDatabase(DB_FILE_NAME)


class MyModel(Model):
    class Meta:
        database = DATA_BASE


class Company(MyModel):
    name = CharField(max_length=64)
    address = CharField(max_length=255, null=True)
    commission = FloatField(default=0.01)


class TimeUnits(MyModel):
    name = CharField(max_length=16)


class Term(MyModel):
    name = CharField(max_length=16)
    time_units = ForeignKeyField(TimeUnits)
    amount = IntegerField()


class Deal(MyModel):
    company = ForeignKeyField(Company, related_name='balance')
    date_of_payment = DateField()
    term = ForeignKeyField(Term)
    amount = FloatField()
    description = TextField(null=True)


class Terminal(MyModel):
    configuration = TextField(null=True)
    name = CharField(max_length=32)
    public_key = TextField(null=True)


class Transaction(MyModel):
    company = ForeignKeyField(Company)
    terminal = ForeignKeyField(Terminal)
    amount = FloatField()
    date_time = DateTimeField(default=datetime.datetime.now())


class PaymentType(MyModel):
    name = CharField(max_length=32)
    description = CharField(max_length=255)


class Payment(MyModel):
    company = ForeignKeyField(Company)
    payment_type = ForeignKeyField(PaymentType)
    date_time = DateTimeField(default=datetime.datetime.now())
    deal = ForeignKeyField(Deal)
    amount = FloatField()


class DbWorks:
    _model_list = (
        TimeUnits, Term, Deal, Company, Terminal, Transaction, PaymentType,
        Payment
    )

    def __init__(self, model_list=None):
        if model_list:
            self._model_list = model_list
        self.db_file_name = DB_FILE_NAME
        if not os.path.exists(self.db_file_name):
            _conn = sqlite3.connect(self.db_file_name)
            _conn.close()
        self.data_base = SqliteDatabase(self.db_file_name)
        for model in self._model_list:
            if not model.table_exists():
                model.create_table()

    def re_init(self, model_list=None):
        """Drops the table in the list and creates them again

        :param model_list: The list of the table classes in the database
        :return: 
        """
        if os.path.exists(DB_FILE_NAME):
            _answer = input(
                '\n'.join(
                    (
                        'This operation will destroy your database!',
                        'All data will be lost!',
                        'Are you sure? <Yes, destroy it/N>: '
                    )
                )
            )
            if _answer == 'Yes, destroy it':
                if model_list:
                    self._model_list = model_list
                for model in self._model_list:
                    if model.table_exists():
                        self.data_base.drop_table(model)
        self.__init__(model_list)

    @staticmethod
    def select_transaction(
            terminal_id=None,
            start_date=datetime.datetime(1971, 12, 25),
            end_date=datetime.datetime.now()
    ):
        if terminal_id:
            return Transaction.select('*').where(
                Transaction.terminal == terminal_id,
                Transaction.date_time <= end_date,
                Transaction.date_time >= start_date
            ).execute()
        return Transaction.select().where(
            Transaction.date_time <= end_date,
            Transaction.date_time >= start_date
        ).execute()

    @staticmethod
    def balance(
            model,
            company=None,
            start_date=datetime.datetime(1971, 12, 25),
            end_date=datetime.datetime.now()
    ):
        if company:
            return list(
                model.select(
                    Company.name, fn.SUM(model.amount)
                ).join(Company).group_by(model.company).where(
                    model.company == company,
                    model.date_time <= end_date,
                    model.date_time >= start_date
                ).dicts()
            )
        return list(
            model.select(
                Company.name, fn.SUM(model.amount)
            ).join(Company).group_by(model.company).where(
                model.date_time <= end_date, model.date_time >= start_date
            ).dicts()
        )

    def company_balance(
            self,
            company=None,
            start_date=datetime.datetime(1971, 12, 25),
            end_date=datetime.datetime.now()
    ):
        transaction_balance = self.balance(
            Transaction, company, start_date, end_date
        )
        payment_balance = self.balance(
            Payment, company, start_date, end_date
        )
        for transaction in transaction_balance:
            company = transaction['name']
            for payment in payment_balance:
                if payment['name'] == company:
                    payment['amount'] += transaction['amount']
                    transaction = None
            if transaction:
                payment_balance.append(transaction)
        return payment_balance

    def insert_replace(self, row_list, model):
        """Inserts or replaces row in the table

        :param row_list: The list of the rows
        :param model: The class of a table in the database
        """
        _chunk_size = self.max_variable_number // len(row_list[0])
        _print_timer = len(row_list) // _chunk_size // 40 + 1
        _n = len(row_list) // (_chunk_size * _print_timer) - 1
        print('\n{}<{}>'.format(' ' * 17, '-' * _n))
        print('Load data to DB:', end=' ')
        with self.data_base.atomic():
            for i in range(0, len(row_list), _chunk_size):
                model.insert_many(
                    row_list[i:i + _chunk_size]
                ).upsert().execute()
                if i % (_chunk_size * _print_timer) == 0:
                    print('.', end='', flush=True)

    @classmethod
    def max_sql_variables(cls):
        """Get the maximum number of arguments allowed in a _query by 
        the current sqlite3 implementation. 
        """
        _db = sqlite3.connect(':memory:')
        _cur = _db.cursor()
        _cur.execute('CREATE TABLE t (test)')
        _low, _high = 0, 10000
        while (_high - 1) > _low:
            _guess = (_high + _low) // 2
            _query = 'INSERT INTO t VALUES ' + ','.join(['(?)' for _ in
                                                         range(_guess)])
            args = [str(i) for i in range(_guess)]
            try:
                _cur.execute(_query, args)
            except sqlite3.OperationalError as e:
                if "too many SQL variables" in str(e):
                    _high = _guess
                else:
                    raise
            else:
                _low = _guess
        _cur.close()
        _db.close()
        cls.max_variable_number = _low


DbWorks.max_sql_variables()