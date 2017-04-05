class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs[name] = ['List from metaclass', 1, 2, 3]
        return super().__new__(cls, name, bases, attrs)


class Journal(metaclass=MyMeta):
    pass


class BlackPirate(Journal):
    pass


if __name__ == '__main__':
    j = Journal()
    b = BlackPirate()
    print(j.Journal)
    print(b.BlackPirate)
