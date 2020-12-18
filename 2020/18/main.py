from typing import List, Optional


def evaluate(a: int, operator: str, b: int) -> int:
    if operator == '+':
        return a + b
    elif operator == '*':
        return a * b
    elif operator is None:
        return b


def calculate(input: List[str]) -> int:
    result: int = 0
    operator: Optional[str] = None

    for item in input:
        if item in ['*', '+']:
            operator = item
        else:
            result = evaluate(result, operator, int(item))

    return result


def calculate_with_precedence(__input: List[str]) -> int:
    for operator in ['+', '*']:
        while operator in __input:
            index: int = __input.index(operator)
            result = evaluate(int(__input[index - 1]), operator, int(__input[index + 1]))
            new_input = __input[:index - 1]
            new_input.append(str(result))
            new_input.extend(__input[index + 2:])
            __input = new_input

    return int(__input[0])


def part_one(lines: List[str]) -> int:
    line_results: List[int] = []
    for line in lines:

        end: int = line.find(')')
        close_bracket: int = end
        while end != -1:

            open_bracket = find_opening_bracket(end, line)

            result: int = calculate(line[open_bracket + 1:close_bracket].split())
            line = line[:open_bracket] + str(result) + line[close_bracket + 1:]

            end: int = line.find(')')
            if end != -1:
                close_bracket = end

        line_result: int = calculate(line.split())
        line_results.append(line_result)

    return sum(line_results)


def find_opening_bracket(end, line) -> int:
    start: int = line.find('(', 0, end)
    open_bracket: int = start
    while start != -1:
        start = line.find('(', start + 1, end)
        if start != -1:
            open_bracket = start
    return open_bracket


def part_two(lines: List[str]) -> int:
    line_results: List[int] = []
    for line in lines:

        end: int = line.find(')')
        close_bracket: int = end
        while end != -1:

            open_bracket = find_opening_bracket(end, line)

            result: int = calculate_with_precedence(line[open_bracket + 1:close_bracket].split())
            line = line[:open_bracket] + str(result) + line[close_bracket + 1:]

            end: int = line.find(')')
            if end != -1:
                close_bracket = end

        line_result: int = calculate_with_precedence(line.split())
        line_results.append(line_result)

    return sum(line_results)


with open('input.txt', 'r') as file:
    lines: List[str] = file.readlines()
    print(part_one(lines))
    print(part_two(lines))
