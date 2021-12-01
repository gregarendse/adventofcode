import re
from typing import Dict, List, Optional, Pattern


class Rule(object):
    rules: List[str] = []
    value: Optional[str] = None

    def apply(self, string):
        """
        3: "a" "b" | "b" "a"

        :param string:
        :return:
        """
        parts: List[str] = "".join(self.rules).split('|')

        valid: bool = False
        for part in parts:
            valid |= part in string
        return valid


def define_rule(rule_id: int, rules: List[str], rule_map: Dict[int, List[str]]) -> List[str]:
    new_rule: List[str] = []
    for rule in rules:
        try:
            _rule_id: int = int(rule)

            new_rule.append("(")
            new_rule.extend(define_rule(_rule_id, rule_map[_rule_id], rule_map))
            new_rule.append(")")
        except:
            new_rule.append(str(rule))

    return new_rule


with open('input.txt', 'r') as file:
    read = file.read()
    [rules, values] = read.split('\n\n')

    rule_map: Dict[int, List[str]] = dict()

    for line in rules.splitlines():
        [rule_id, rules] = line.split(':')
        rule_map[int(rule_id)] = rules.replace('"', '').split()

    rule_zero: List[str] = define_rule(0, rule_map[0], rule_map)

    print("".join(rule_zero))
    pattern: Pattern[str] = re.compile("^" + "".join(rule_zero) + "$")

    match_count: int = 0
    for value in values.splitlines():
        if pattern.match(value) is not None:
            print(value)
            match_count += 1

    print(match_count)
