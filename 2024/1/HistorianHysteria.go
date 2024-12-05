package main

import (
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

func PartOne(input string) (int, error) {

	lefts, rights, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	slices.Sort(lefts)
	slices.Sort(rights)

	diffs := make([]int, len(lefts))
	sum := 0

	for i := 0; i < len(lefts); i++ {
		l_int := lefts[i]
		r_int := rights[i]

		var diff int
		if l_int >= r_int {
			diff = l_int - r_int
		} else {
			diff = r_int - l_int
		}

		diffs = append(diffs, diff)
		sum += diff
	}

	return sum, nil
}

func PartTwo(input string) (int, error) {

	lefts, rights, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	left_nums := map[int]int{}
	right_nums := map[int]int{}

	for i := 0; i < len(lefts); i++ {
		left_nums[lefts[i]] += 1
		right_nums[rights[i]] += 1
	}

	sum := 0

	for i := 0; i < len(lefts); i++ {
		sum += lefts[i] * right_nums[lefts[i]]
	}

	return sum, nil
}

func parseFile(input string) ([]int, []int, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, nil, err
	}

	lines := strings.Split(string(file), "\n")

	lefts := make([]int, len(lines))
	rights := make([]int, len(lines))

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		split := strings.Fields(line)

		if len(split) != 2 {
			log.Printf("malformed input: %q, %v", line, split)
			return nil, nil, err
		}

		l, r := split[0], split[1]

		l_int, err := strconv.Atoi(l)
		if err != nil {
			log.Printf("Failed to convert to int: %q", l)
			return nil, nil, err
		}

		r_int, err := strconv.Atoi(r)
		if err != nil {
			log.Printf("Failed to convert to int: %q", r)
			return nil, nil, err
		}

		lefts = append(lefts, l_int)
		rights = append(rights, r_int)
	}
	return lefts, rights, nil
}
