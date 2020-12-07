from typing import List, Set

count: int = 0
everyone_count: int = 0

with open('input.txt', 'r') as file:
    read = file.read()

    for group in read.strip().split('\n\n'):
        answers: List = []
        for person in group.split('\n'):
            person_answers: Set[str] = set()
            for answer in person.replace('\n', ''):
                person_answers.add(answer)

            answers.append(person_answers)

        group_answers: Set[str] = answers[0]
        for answer in answers:
            group_answers = group_answers & answer
        everyone_count = everyone_count + len(group_answers)

    for line in read.split('\n\n'):
        answers = set()
        for c in line.replace('\n', ''):
            answers.add(c)
        count = count + len(answers)

print(count)
print(everyone_count)
