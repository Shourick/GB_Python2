__author__ = 'Наумов Александр Сергеевич'
from concatenator import Concatenator

cnt = Concatenator('files/file1.zip')
cnt.concatenate('files/file1')
cnt.file_list = 'files/file2.zip'
cnt.concatenate('files/file2')

