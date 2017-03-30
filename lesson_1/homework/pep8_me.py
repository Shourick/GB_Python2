import random
import string
import os


def create_file(namef, dir_, size):
    if not size.isdigit():
        if size.endswith('KB'):
            s1 = size.split('KB')
            size1 = int(s1[0])*1024
            token = ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.ascii_lowercase +
                    string.digits
                ) for _ in range(size1)
            )
        # if -> elif
        elif size.endswith('MB'):
            s1 = size.split('MB')
            size1 = int(s1[0]) * 1048567
            token = ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.ascii_lowercase +
                    string.digits
                ) for _ in range(size1)
            )
        # if -> elif
        elif size.endswith('GB'):
            s1 = size.split('GB')
            size1 = int(s1[0]) * 1073741824
            token = ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.ascii_lowercase +
                    string.digits
                ) for _ in range(size1)
            )
        # Добавлено для исключения ошибки UnboundLocalError
        else:
            token = 'Unknown size unit!'
    else:
        token = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.ascii_lowercase +
                string.digits
            ) for _ in range(int(size))
        )

    # file = open(dir_ + namef, "w")
    # file.write(token)
    with open(os.path.join(dir_, namef), "w") as file:
        file.write(token)


# create_file("/test1.txt", "E:", '10KB')
# create_file("/test2.txt", "E:", '1024')
# create_file("/test11.txt", "E:", '2MB')
# create_file("/test21.txt", "E:", '1B')

# Я бы написал так, но может так непринято?
create_file("test1.txt", "E:/", '10KB')
create_file("test2.txt", "E:/", '1024')
create_file("test11.txt", "E:/", '2MB')
create_file("test21.txt", "E:/", '1B')
