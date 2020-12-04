#!/usr/bin/env python3
from typing import List, Dict, Set


class Passport(object):
    valid_hair_characters: Set[str] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
    valid_eye_colors: Set[str] = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    numbers: Set[str] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    def __init__(self, byr, iyr, eyr, hgt, hcl, ecl, pid, cid):
        self.byr = byr
        self.iyr = iyr
        self.eyr = eyr
        self.hgt = hgt
        self.hcl = hcl
        self.ecl = ecl
        self.pid = pid
        self.cid = cid

    def __is_byr_valid__(self) -> bool:
        len_check = len(self.byr) == 4
        range_check = 1920 <= int(self.byr) <= 2002
        return len_check and range_check

    def __is_iyr_valid__(self) -> bool:
        len_check = len(self.iyr) == 4
        range_check = 2010 <= int(self.iyr) <= 2020
        return len_check and range_check

    def __is_eyr_valid__(self) -> bool:
        len_check = len(self.eyr) == 4
        range_check = 2020 <= int(self.eyr) <= 2030
        return len_check and range_check

    def __is_hgt_valid__(self) -> bool:
        s = str(self.hgt)
        if s.endswith('cm'):
            return 150 <= int(s.replace('cm', '')) <= 193
        elif s.endswith('in'):
            return 59 <= int(s.replace('in', '')) <= 76
        else:
            return False

    def __is_hcl_valid__(self) -> bool:
        s = str(self.hcl)
        if s.startswith('#') and len(self.hcl) == 7:
            hair_characters = set([i for i in s.replace('#', '')])
            return len(hair_characters - self.valid_hair_characters) == 0
        else:
            return False

    def __is_ecl_valid__(self) -> bool:
        check = self.ecl in self.valid_eye_colors
        return check

    def __is_pid_valid__(self) -> bool:
        len_check = len(self.pid) == 9
        pid_set = set([i for i in str(self.pid)])
        check = len(pid_set - self.numbers) == 0
        return len_check and check

    def is_valid(self) -> bool:
        return self.is_present() \
               and self.__is_byr_valid__() \
               and self.__is_iyr_valid__() \
               and self.__is_eyr_valid__() \
               and self.__is_hgt_valid__() \
               and self.__is_hcl_valid__() \
               and self.__is_ecl_valid__() \
               and self.__is_pid_valid__()

    def is_present(self) -> bool:
        return self.byr is not None \
               and self.iyr is not None \
               and self.eyr is not None \
               and self.hgt is not None \
               and self.hcl is not None \
               and self.ecl is not None \
               and self.pid is not None

    def __str__(self):
        return "byr: {byr}, iyr: {iyr}, eyr: {eyr}, hgt: {hgt}, hcl: {hcl}, ecl: {ecl}, pid: {pid}, cid: {cid}" \
            .format(byr=self.byr, iyr=self.iyr, eyr=self.eyr, hgt=self.hgt, hcl=self.hcl, ecl=self.ecl, pid=self.pid,
                    cid=self.cid)


passports: List[Passport] = []
count: int = 0

with open('input.txt', 'r') as file:
    lines = file.read().splitlines()
    lines.append('')

    kvs: Dict[str, str] = {}
    for line in lines:

        if len(line) > 0:
            parts = line.split()

            for part in parts:
                split = part.split(':')
                kvs[str(split[0])] = str(split[1])
        else:
            passport: Passport = Passport(
                byr=kvs.get('byr'),
                iyr=kvs.get('iyr'),
                eyr=kvs.get('eyr'),
                hgt=kvs.get('hgt'),
                hcl=kvs.get('hcl'),
                ecl=kvs.get('ecl'),
                pid=kvs.get('pid'),
                cid=kvs.get('cid')
            )

            passports.append(passport)

            kvs = {}

            if passport.is_valid():
                count = count + 1

print(count)
