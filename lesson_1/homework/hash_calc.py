import csv
import hashlib

__author___ = 'Наумов Александр Сергеевич'


def get_hash(source_str, hash_type):
    hash_object = hashlib.__get_builtin_constructor(hash_type)()
    hash_object.update(source_str.encode('utf-8'))
    return hash_object.hexdigest()


with open('need_hashes.csv', encoding='utf-8') as f:
    data_list = [
        [data[0], data[1], get_hash(data[0], data[1])]
        for data in csv.reader(f.read().splitlines(), delimiter=';')
    ]
with open('need_hashes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(data_list)
