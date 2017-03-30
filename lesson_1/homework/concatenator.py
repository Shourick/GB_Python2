import os
import sys
import io
import zipfile
import hashlib
import magic
import doctest

from collections import OrderedDict

__author___ = 'Наумов Александр Сергеевич'


class Concatenator:
    '''Class to concatenate chunks of file in single one
    also it is possible to slice single file into chunks
    
    >>> cnt = Concatenator('test_data/file1.zip')
    >>> cnt.path
    'test_data/file1'
    >>> cnt.key_file
    'test_data/file1\\\\parts.md5'

    '''

    def __init__(self, container, key_file='parts.md5'):

        if os.path.exists(container) and \
           'zip' in MyMagic().from_file(container).lower():

            container = self.unzip_container(container)

        elif os.path.isdir(container):
            pass

        else:
            print('Wrong format for container!')
            raise ValueError(
                'Wrong format for container {}!\n '
                'Zip archive or directory expected!'.format(container)
            )
        self.path = container
        self.key_file = os.path.join(self.path, key_file)
        with open(self.key_file) as f:
            self.hash_list = f.read().splitlines()
        self._file_list = [
            os.path.join(container, file)
            for file in os.listdir(container)
            if self.get_md5(os.path.join(container, file))
            in self.hash_list
        ]

    @property
    def file_list(self):
        '''Return a chunks list
        
        :return: List of chunks as list of files
        '''
        return self._file_list
    
    @file_list.setter
    def file_list(self, container):
        '''Reinitiates the instance with new chunks
        
        :param container: The location of chunks
        :return: None
        '''
        self.__init__(container)

    def unzip_container(self, zip_file):
        _extract_path = os.path.dirname(zip_file)
        self.unzip(zip_file, _extract_path)
        return '.'.join(zip_file.split('.')[:-1])

    @staticmethod
    def unzip(file_name, path_to_extract=None):
        '''Decompresses zip archive
        
        :param file_name: The name of the zip archive
        :param path_to_extract: Path to extract archived files to
        :return: None
        '''
        with zipfile.ZipFile(file_name, 'r') as zf:
            zf.extractall(path_to_extract)

    @staticmethod
    def get_md5(file_name, chunk_size=io.DEFAULT_BUFFER_SIZE):
        '''Gets the md5 hex digest for the a file
        
        :param file_name: The file name
        :param chunk_size: Size of a chunk, is used to reduce 
               memory usage on a big file
        :return: The hex digest of the file 
        '''
        hash_object = hashlib.md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hash_object.update(chunk)
        return hash_object.hexdigest()

    @staticmethod
    def slice_file(file_name, chunk_size):
        '''Slices a file into chunks
        
        :param file_name: The file name of the chuncked file
        :param chunk_size: Size of the chunk
        :return: Number of chunks
        '''
        _dir = os.path.dirname(file_name)
        _count = 0
        with open(file_name, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hash_object = hashlib.md5()
                hash_object.update(chunk)
                hash_value = hash_object.hexdigest()
                f_name = '.'.join(
                    (
                        hash_value[:8],
                        hash_value[8:12]
                    )
                )
                with open(os.path.join(_dir, f_name), 'wb') as f_i:
                    f_i.write(chunk)
                    _count += 1
        return _count

    def dict_md5(self, file_list=None):
        '''Creates a dictionary {<hex digest1>: <file_name1>, ...} 
           for all files in the list
        
        :param file_list: The list of files
        :return: Dictionary as is described above
        '''
        if file_list is None:
            file_list = self._file_list
        return dict(
            (self.get_md5(file), file)
            for file in file_list if os.path.isfile(file)
        )

    def write_list_md5(self, path=None, file_name=None):
        '''Writes list of the files hex digests into a file
        
        :param path: Path to the files
        :param file_name: The output file name
        :return: Number of the files 
        '''
        if path is None:
            path = self.path
        _md5_list = self.dict_md5(os.listdir(path)).keys()
        if file_name is None:
            file_name = self.key_file
        with open(file_name, 'w') as f:
            f.write(_md5_list)
        return len(_md5_list)

    def concatenate(self, output_file):
        '''Concatenates chunks into a single file
        
        :param output_file: File name without extension to concatenate into
        :return: The type and size of the output file
        '''
        with open(self.key_file) as f:
            hash_list = f.read().splitlines()
            hash_files = (
                OrderedDict(
                    sorted(
                        self.dict_md5().items(),
                        key=lambda t: hash_list.index(t[0])
                    )
                )
            )
        _file_name = '.'.join((self.path, '_cnt_'))
        with open(_file_name, 'wb') as f_out:
            for file in hash_files.values():
                with open(file, 'rb') as f_in:
                    f_out.write(f_in.read())

        _file_type = MyMagic(mime=True).from_file(_file_name)
        output_file = '.'.join((output_file, _file_type.split('/')[1]))
        if os.path.exists(output_file):
            os.remove(output_file)
        os.renames(_file_name, output_file)

        return _file_type, \
               os.path.getsize(output_file)


# Пришлось доработать базовый класс magic.Magic,
# чтобы он мог найти нужные файлы
class MyMagic(magic.Magic):

    @staticmethod
    def get_magic():
        _path = ''
        for path in sys.path:
            if os.path.exists(os.path.join(path, 'magic.mgc')):
                _path = path
                break
        return os.path.join(_path, 'magic.mgc')

    def __init__(self, *args, **kwargs):
        super().__init__(magic_file=self.get_magic(), *args, **kwargs)


if __name__ == '__main__':
    doctest.testmod()
