package main

import (
	"bytes"
	"errors"
	"log"
	"os"
	"strconv"
	"strings"
)

func PartOne(input string) (int, error) {

	lines, err := parseFile(input)

	if err != nil {
		return 0, err
	}

	result := 0

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		for j := 0; j < len(line); j++ {

			if mul, index, err := multiply(line[j:]); err == nil {
				result += mul
				j += index
			}

		}

	}
	return result, nil
}

func PartTwo(input string) (int, error) {

	lines, err := parseFile(input)

	if err != nil {
		return 0, err
	}

	result := 0
	enabled := true

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		for j := 0; j < len(line); j++ {

			if _, index, err := parseInstruction(line[j:], "do()"); err == nil {
				enabled = true
				j += index
			}

			if _, index, err := parseInstruction(line[j:], "don't()"); err == nil {
				enabled = false
				j += index
			}

			if enabled {
				if mul, index, err := multiply(line[j:]); err == nil {
					result += mul
					j += index
				}
			}

		}

	}
	return result, nil
}

func parseInstruction(line string, instruction string) (int, int, error) {

	if len(line) < len(instruction) {
		return 0, 0, errors.New("line too short")
	}

	if line[:len(instruction)] != instruction {
		return 0, 0, errors.New("instruction does not match")
	}

	return 1, len(instruction), nil
}

func multiply(line string) (int, int, error) {
	instruction := "mul("
	index := 0

	if len(line) < len(instruction) {
		return 0, 0, errors.New("mul line too short")
	}

	if line[:len(instruction)] != instruction {
		return 0, 0, errors.New("mul line does not match")
	}
	index += len(instruction)

	//	Find Left
	left, position, err := extractNumber(line[index:], ",")
	if err != nil {
		return 0, 0, err
	}
	index += position

	// Move past the ,
	index += 1

	//	Find right
	right, position, err := extractNumber(line[index:], ")")
	if err != nil {
		return 0, 0, err
	}
	index += position

	return left * right, index, nil

}

func parseFile(input string) ([]string, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, err
	}

	file = bytes.TrimSpace(file)

	lines := strings.Split(string(file), "\n")

	return lines, nil
}

func extractNumber(line string, delim string) (int, int, error) {

	for k := 1; k < 4; k++ {
		if string(line[k]) == delim {
			value, err := strconv.Atoi(line[:k])
			if err != nil {
				log.Fatalf("failed to parse number: %v", err)
				return 0, 0, err
			}
			return value, k, nil
		}
	}

	return 0, 0, errors.New(delim + " not found")
}
