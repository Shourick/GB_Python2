import os
import sqlite3
import json
import datetime
from peewee import *

BASE_DIR = os.path.dirname(__file__)
DB_FILE_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
DATA_BASE = SqliteDatabase(DB_FILE_NAME)
START_DATE = datetime.datetime(1971, 12, 25)
END_DATE = datetime.datetime.now()
SERVICE_OPERATIONS = [
    {'id': 0, 'name': 'power on'},
    {'id': 1, 'name': 'reboot'},
    {'id': 2, 'name': 'power off'},
    {'id': 3, 'name': 'sensor activated'},
    {'id': 4, 'name': 'blocked, encashment is required'},
]
TRANSACTION_TYPES = [
    {'id': 0, 'transaction_type': 'service transaction'},
    {'id': 1, 'transaction_type': 'payment transaction'},
    {'id': 2, 'transaction_type': 'encashment transaction'},
]


class MyModel(Model):
    class Meta:
        database = DATA_BASE


class Company(MyModel):
    name = CharField(max_length=64)
    address = CharField(max_length=255, null=True)
    commission = FloatField(default=0.01)


class Employee(MyModel):
    name = CharField(max_length=32)
    middle_name = CharField(max_length=32)
    surname = CharField(max_length=32)


class TimeUnits(MyModel):
    name = CharField(max_length=16)


class Term(MyModel):
    name = CharField(max_length=16)
    time_units = ForeignKeyField(TimeUnits)
    amount = IntegerField()


class Deal(MyModel):
    company = ForeignKeyField(Company, related_name='deal')
    date_of_payment = DateField()
    term = ForeignKeyField(Term)
    amount = FloatField()
    description = TextField(null=True)


class Terminal(MyModel):
    ip = CharField(primary_key=True, max_length=7)
    configuration = TextField(null=True)
    name = CharField(max_length=32, null=True)
    public_key = TextField(null=True)


class TransactionType(MyModel):
    id = PrimaryKeyField()
    transaction_type = CharField(max_length=32)


class Service(MyModel):
    id = PrimaryKeyField()
    name = CharField(max_length=32)


class Transaction(MyModel):
    terminal = ForeignKeyField(Terminal, related_name='transactions')
    transaction_id = IntegerField()
    transaction_type = ForeignKeyField(TransactionType)
    date_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = ((('terminal', 'transaction_id'), True),)


class ServiceTransaction(MyModel):
    transaction = ForeignKeyField(
        Transaction, primary_key=True, related_name='services'
    )
    service = ForeignKeyField(Service)


class PaymentTransaction(MyModel):
    transaction = ForeignKeyField(
        Transaction, primary_key=True, related_name='payments'
    )
    company = ForeignKeyField(Company)
    amount = FloatField()


class EncashmentTransaction(MyModel):
    transaction = ForeignKeyField(
        Transaction, primary_key=True, related_name='encashments'
    )
    employee = ForeignKeyField(Employee)
    amount = FloatField()


class PaymentType(MyModel):
    name = CharField(max_length=32)
    description = CharField(max_length=255)


class Payment(MyModel):
    company = ForeignKeyField(Company, related_name='payments')
    payment_type = ForeignKeyField(PaymentType)
    date_time = DateTimeField(default=datetime.datetime.now())
    deal = ForeignKeyField(Deal, related_name='payments')
    amount = FloatField()


class DbWorks:
    _model_list = (
        TimeUnits, Term, Deal, Company, Terminal, Transaction, PaymentType,
        Payment, ServiceTransaction, Service, PaymentTransaction,
        EncashmentTransaction, Employee, TransactionType
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
        self.insert_replace(TRANSACTION_TYPES, TransactionType)
        self.insert_replace(SERVICE_OPERATIONS, Service)

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
            terminal_ip=None, start_date=START_DATE, end_date=END_DATE
    ):
        '''Makes the report about transaction for the specified terminal 
        within the term if the terminal is not specified,
         then makes the report for all terminals 

        :param terminal_ip: IP of a terminal
        :param start_date: Start date of the term
        :param end_date: End date of the term
        :return: Query from the Transaction table
        '''
        if terminal_ip:
            return list(Transaction.select().where(
                Transaction.terminal == terminal_ip,
                Transaction.date_time <= end_date,
                Transaction.date_time >= start_date
            ).dicts())
        return list(Transaction.select().where(
            Transaction.date_time <= end_date,
            Transaction.date_time >= start_date
        ).dicts())

    @staticmethod
    def select_last_transaction(terminal_ip):
        '''Returns the last transaction ID for the specified terminal 

        :param terminal_ip: IP of a terminal
        :return: The last transaction ID
        '''
        try:
            return Transaction.select().where(
                Transaction.terminal == terminal_ip)\
                .order_by(Transaction.transaction_id).get().transaction_id
        except Transaction.DoesNotExist:
            Terminal(
                ip=terminal_ip, name=' '.join(('Terminal', terminal_ip))
            ).save(True)
            return 0

    @staticmethod
    def save_transaction(transaction):
        _transaction = Transaction(
            terminal=transaction.client_ip,
            transaction_id=transaction.id,
            transaction_type=transaction.operation,
            date_time=transaction.date_time
        )
        _transaction.save()
        _id = _transaction.id
        if transaction.operation == 0:
            _transaction = ServiceTransaction(
                transaction=_id, service=transaction.reference_id
            )
        elif transaction.operation == 1:
            try:
                Company.get(Company.id == transaction.reference_id)
            except Company.DoesNotExist:
                Company(
                    id=transaction.reference_id,
                    name=' '.join(('Company', str(transaction.reference_id))),
                    commission = 0.01
                ).save(True)
            _transaction = PaymentTransaction(
                transaction=_id,
                company=transaction.reference_id,
                amount=transaction.amount
            )
        elif transaction.operation == 2:
            try:
                Employee.get(Employee.id == transaction.reference_id)
            except Employee.DoesNotExist:
                Employee(
                    id=transaction.reference_id,
                    name=' '.join(('Employee', str(transaction.reference_id))),
                    middle_name=' ',
                    surname=' '
                ).save(True)
            _transaction = EncashmentTransaction(
                transaction=_id,
                employee=transaction.reference_id,
                amount=transaction.amount
            )
        else:
            raise ValueError(
                'Wrong transaction type {}'.format(transaction.operation)
            )
        _transaction.save(True)

    @staticmethod
    def balance(
            model, ref_model, model_id=None,
            start_date=START_DATE, end_date=END_DATE
    ):
        '''Calculates the operational balance for the specified model 
        within the term. If the model_id is not specified, then calculates 
        the balance for all models
        
        :param model: The reference table of balanced items  
        :param ref_model: The table name where operational data are stored
        :param model_id: Id of the balanced item
        :param start_date: Start date of the term
        :param end_date: End date of the term
        :return: The list of the dictionary like this:
        [
            {'name': <company name_1>, 'amount': <amount_1>},
            ...
            {'name': <company name_n>, 'amount': <amount_n>}
        ]
        '''
        if model_id:
            return list(
                model.select(model.name).annotate(
                    ref_model, fn.SUM(ref_model.amount)).where(
                    model.id == model_id,
                    ref_model.date_time <= end_date,
                    ref_model.date_time >= start_date
                ).dicts()
            )
        return list(
                model.select(model.name).annotate(
                    ref_model, fn.SUM(ref_model.amount)).where(
                    ref_model.date_time <= end_date,
                    ref_model.date_time >= start_date
                ).dicts()
            )

    def total_balance(
            self, model=Company, model_id=None,
            start_date=START_DATE, end_date=END_DATE
    ):
        transaction_balance = self.balance(
            model, Transaction, model_id, start_date, end_date
        )
        payment_balance = self.balance(
            model, Payment, model_id, start_date, end_date
        )
        for transaction in transaction_balance:
            company = transaction['name']
            for payment in payment_balance:
                if payment['name'] == company:
                    payment['amount'] += transaction['amount']
                    transaction = None
            if transaction:
                payment_balance.append(transaction)
        return dict((item['name'], item['amount']) for item in payment_balance)

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
        """Gets the maximum number of arguments allowed in a _query by 
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
if __name__ == '__main__':
    db = DbWorks()
    # Выбрать платёжные транкции для указанного терминала (id)
    # за указанный период (от моего рождения до текущего момента)
    print(db.select_transaction(terminal_ip='1.10'))
    # За указанный период (datetime) по данным платёжных транзакций
    # сформировать выборку какая сумма должна быть перечислена каждой
    # фирме-партнёру (можно не учитывать тех партнёров,
    # для которых нет платежей).
    print(db.total_balance())
    # По данным платёжных транзакций сформировать выборку с указанием,
    # какая сумма прошла через каждый терминал за указанный период.
    print(db.balance(model=Terminal, ref_model=Transaction))
    #  *Дополнительно.* По каждому терминалу сформировать отчет,
    # где отражаются временные периоды в течение дня (0-6, 6-12, 12-18, 18-24)
    # и количество транзакций в каждый временной период.
    time_step = 6
    for i in range(0, 24, time_step):
        print('Period {} - {}'.format(i, i + time_step))
        print(
            list(
                Terminal.select(Terminal.name).annotate(
                    Transaction, fn.Count(Transaction.id).alias('count')
                ).where(
                    Transaction.date_time.hour >= i,
                    Transaction.date_time.hour < (i + time_step)
                ).dicts()
            )
        )
