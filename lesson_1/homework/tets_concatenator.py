import os
# import pytest
# import doctest
import unittest
from concatenator import Concatenator


class TestConcatenator(unittest.TestCase):

    def test_concatenator_path(self):
        self.assertEqual(
            Concatenator('test_data/file1.zip').path, 'test_data/file1'
        )

    def test_concatenator_file_list(self):
        test_list = [
            '00YxJtCq', '0Bfd4ZT9', '0D0xLDnk', '0EhW1kqt', '0EUEcFZK',
            '0fRkvCjC', '0jvzCvlc', '0MD2caDF', '0MWjfPlL', '0W7IYJnZ',
            '0Y9ceEkn', '0Yt7ORri', '1bTqA7N6', '1Ih7dQps', '1MNW5I3h',
            '1USusw3J', '1VniyghJ', '223H65wl', '29tJ9Sww', '2gTp74zC',
            '2kgbh5Dg', '2L0KUBew', '2mRGTpXj', '2R1dxrCq', '2Seixb7R',
            '2ZaMOhnl', '3BDP9x7Y', '3Cn6nyTR', '3d5wStYw', '3fi9bU5I',
            '3fO5QHkv', '3XZ3pugn', '43NsVYXG', '49mUbQlq', '4AVhr91u',
            '4dawZCja', '4IhV5lwE', '4K92FKuZ', '4NBnBSWX', '4nP87Omj',
            '4oUUt1uX', '4TfHPdNZ', '4xjdByGL', '5BmZ5WkK', '5OfHh5Bj',
            '5QsMvfEU', '5r9IfpaB', '5uNt1KxQ', '5W145Q6k', '69SMTiFx',
            '6bpaPc1y', '6ECyFtXo', '6GDNAEQD', '6Hpku3Qc', '6jlxIE5S',
            '6LB9s4Vc', '6ORNqmhR', '6sP8djY1', '6uZletmj', '6V0gMXaX',
            '6wlMLX6R', '72gyYv5J', '72xt62lj', '78P4d0zS', '7clMMGoX',
            '7DMj70VV', '7KWE8Yrb', '7llHBWPb', '7osf141S', '7XeGguiI',
            '8a7bwoof', '8GGr6HUF', '8gSBVXrq', '8jW39frF', '8NuAoD9a',
            '96rKwPvk', '9AaaoHMK', '9B6vLf4f', '9bzYAmG3', '9ePwzRdZ',
            '9fB5Gg91', '9ih5WgbE', '9knHBHW9', '9MhNieaW', '9ndv3uGV',
            '9tSnZESv', '9YWY8djS', 'a0OMlF3j', 'aC4klkqV', 'adzgkHOW',
            'AhTPp2xW', 'AkfQuUld', 'AMIIDTVG', 'anBiW54D', 'AoeCuWyN',
            'aPQmS93x', 'apW8vUJm', 'aqHemXKn', 'aVipogbi', 'aVW64Knc',
            'AwVEhREV', 'B6p484um', 'B78LXxeI', 'bbkFHQig', 'BErM8aqa',
            'bevJor26', 'BFgPEui8', 'Bi7kJy5w', 'bjMiiH3K', 'bKNpSU5B',
            'Bq3XQRV7', 'BYjDOosq', 'c0wK6r9U', 'C7YyiyNY', 'C8Fp2Tao',
            'CaDwI6dW', 'ccWcTQIV', 'cm0dH5KH', 'cn6TvwxJ', 'cnssuDAq',
            'Co5aZ2Zn', 'COJSv03F', 'CoxTiP77', 'cRQCnrg5', 'CRW8Vxyd',
            'CYrjxlLs', 'd2CBvhlH', 'd44EdQYf', 'D7XL0GcO', 'daXcXCix',
            'Db0Q6fAE', 'DbFQfREd', 'dD3a94hL', 'dFgm919d', 'DMFLbKe3',
            'dNPJ22p6', 'dOzCEijK', 'DqimimoK', 'Dr2ixLP4', 'dUGEmpaB',
            'dwKwREvJ', 'DXZafx2R', 'dY16TYcJ', 'E3xpvRIu', 'eNhZ7axT',
            'eOsMXVQn', 'EOUO5yPx', 'EQoqc3at', 'EW0VjDeO', 'EWSePDRn',
            'EXzvJPl3', 'fF0UPvQA', 'FMX0hwqZ', 'FN6VgFdy', 'fOWwD5YC',
            'fPIW7XyT', 'G2qKpWcC', 'Gf627j3z', 'gzTvJeib', 'H4WjsKrP',
            'HBWY9NpN', 'hcHhaTp1', 'HcS72lJo', 'hKAt8urh', 'HKLQSO7d',
            'HsGfgwEy', 'hTv9cEHY', 'HwVRoXyi', 'hwymkuly', 'HxxGQUxO',
            'hy4f2McS', 'i9DdXan2', 'iABfXt7m', 'IIeNesZo', 'IjLOgdrv',
            'iJnkrd18', 'IK9u5wge', 'IsxsPYUw', 'ITDgsQ70', 'ixvVnwWS',
            'Izi0RsmB', 'j5hF0vw6', 'J5oP1FVZ', 'JWRVOgTK', 'k18OQ8fQ',
            'k9TPSznN', 'KF99aOSZ', 'kIBH2Gko', 'KisWjDRC', 'KITIg8L5',
            'KwhXUg6h', 'KyJuOjV8', 'l426Uh7T', 'L7coJ82v', 'lB0k8Ioy',
            'M6UZwHAJ', 'mF0EX0EX', 'MG9WO0r0', 'mgrm8kHi', 'MM65e7Xp',
            'moOZc0l1', 'MYttSUn3', 'NaYvqoUE', 'Ng7jqpNp', 'nhkNLR7R',
            'nIL5sbWU', 'nKY1TGqd', 'nndtHNqA', 'oC5r3jcL', 'ocltruSW',
            'oElmgnps', 'ohnVEcu4', 'oKngojFi', 'puDDWxO8', 'QdeoVPtb',
            'QMCa5uDh', 'QtZkulB7', 'RA3XFYCW', 'RBexzkfG', 'rFa15S4j',
            'rg2Hb6FJ', 'rMLF0MOQ', 'rR2WOVEi', 'StsptBaq', 'sVF18dDz',
            'T31xVVvd', 'tDEZsvIi', 'to9VfY5I', 'TqVN72C7', 'UcfFuFNU',
            'ueCJbip7', 'ufyq5y8A', 'UPo2DN6p', 'UPZdAcj7', 'V0DEtdSh',
            'wEpy8Oe5', 'zbctfoRK', 'zKiyscvS', 'zN8ziYX3'
        ]
        self.assertEqual(
            Concatenator('test_data/file1.zip').file_list,
            [os.path.join('test_data/file1', file) for file in test_list]
        )

    def test_concatenator_key_file(self):
        self.assertEqual(
            Concatenator('test_data/file1.zip').key_file,
            'test_data/file1\\parts.md5'
        )
        self.assertEqual(
            Concatenator('test_data/file1.zip', key_file='parts.md5').key_file,
            'test_data/file1\\parts.md5'
        )
        with self.assertRaises(FileNotFoundError):
            Concatenator('test_data/file1.zip', key_file='parts')

    def test_concatenator_container(self):
        with self.assertRaises(ValueError):
            Concatenator('test_data/test.jpg', key_file='parts')


if __name__ == '__main__':
    unittest.main()
