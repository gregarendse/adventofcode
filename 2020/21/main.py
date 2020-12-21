import re
from typing import List, Dict, Set


def part_one(lines: List[str]) -> int:
    all_ingredients, all_allergens, ingredient_allergen_map = process(lines)

    count: int = 0
    allergens: Set[str] = set()

    for allergen in ingredient_allergen_map.values():
        allergens |= allergen

    safe_ingredients: Set[str] = set(all_ingredients) - allergens

    for ingredient in all_ingredients:
        if ingredient in safe_ingredients:
            count += 1

    return count


def process(lines: List[str]) -> [List[str], Set[str]]:
    all_ingredients: List[str] = []
    all_allergens: List[str] = []
    ingredient_allergen_map: Dict[str, Set[str]] = dict()

    pattern = re.compile('(?P<ingredients>.*)\s+\(contains\s+(?P<allergens>.*)\)')

    for line in lines:
        match = pattern.match(line)
        ingredients: List[str] = match.groupdict()['ingredients'].split()
        all_ingredients.extend(ingredients)

        allergens: List[str] = match.groupdict()['allergens'].replace(',', '').split()
        all_allergens.extend(allergens)

        for allergen in allergens:
            existing_ingredients: Set[str] = ingredient_allergen_map.get(allergen)

            if existing_ingredients is not None:
                ingredient_allergen_map[allergen] = set(ingredients) & existing_ingredients
            else:
                ingredient_allergen_map[allergen] = set(ingredients)

    return all_ingredients, all_allergens, ingredient_allergen_map


def part_two(lines: List[str]) -> str:
    all_ingredients, all_allergens, ingredient_allergen_map = process(lines)
    lens = [len(item) for item in ingredient_allergen_map.values()]

    while max(lens) > 1:
        for allergen in ingredient_allergen_map.keys():

            if len(ingredient_allergen_map[allergen]) == 1:
                continue

            for other in ingredient_allergen_map.keys():
                if len(ingredient_allergen_map[allergen]) == 1:
                    break
                if allergen == other:
                    continue
                if len(ingredient_allergen_map[other]) == 1:
                    ingredient_allergen_map[allergen] -= ingredient_allergen_map[other]

        lens = [len(item) for item in ingredient_allergen_map.values()]

    allergens: List[str] = list(set(all_allergens))
    allergens.sort()

    canonical_list: List[str] = []
    for key in allergens:
        canonical_list.append(list(ingredient_allergen_map.get(key))[0])

    return ",".join(canonical_list)


with open('input.txt', 'r') as file:
    lines: List[str] = file.readlines()
    print(part_one(lines))
    print(part_two(lines))
