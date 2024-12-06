package main

import (
	"bytes"
	"errors"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

func PartOne(input string) (int, error) {

	rules, lines, err := parseFile(input)

	if err != nil {
		return 0, err
	}

	middleValueSum := 0

	for _, line := range lines {

		correctOrder := appyRules(rules, line)

		if correctOrder {
			middleValue := line[len(line)/2]
			middleValueSum += middleValue
		}
	}

	return middleValueSum, nil
}

func appyRules(rules []Rule, line []int) bool {

	for _, rule := range rules {
		pass := rule.Apply(line)
		if !pass {
			return false
		}
	}

	return true
}

func PartTwo(input string) (int, error) {
	rules, lines, err := parseFile(input)

	if err != nil {
		return 0, err
	}

	middleValueSum := 0

	errorLines := make([][]int, 0)
	for _, line := range lines {
		if !appyRules(rules, line) {
			errorLines = append(errorLines, line)
		}
	}

	for _, line := range errorLines {

		for {
			retry := false

			for _, rule := range rules {
				apply := rule.Apply(line)
				if !apply {
					rule.Fix(line)
					retry = true
					break
				}
			}

			if !retry {
				break
			}
		}

		middleValueSum += line[len(line)/2]
	}

	return middleValueSum, nil
}

type Rule struct {
	left  int
	right int
}

func (r *Rule) Fix(line []int) {

	leftIndex := slices.Index(line, r.left)
	rightIndex := slices.Index(line, r.right)

	if leftIndex == -1 || rightIndex == -1 {
		return
	}

	line[leftIndex] = r.right
	line[rightIndex] = r.left
}

func (r *Rule) Apply(line []int) bool {

	leftIndex := slices.Index(line, r.left)
	rightIndex := slices.Index(line, r.right)

	if leftIndex == -1 || rightIndex == -1 {
		return true
	}

	if leftIndex < rightIndex {
		return true
	}

	return false
}

func parseFile(input string) ([]Rule, [][]int, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, nil, err
	}

	file = bytes.TrimSpace(file)

	parts := strings.Split(string(file), "\n\n")

	//	Rules...
	rawRules := strings.Split(parts[0], "\n")
	rules := make([]Rule, len(rawRules))
	for i, rawRule := range rawRules {
		splitRule := strings.Split(rawRule, "|")

		left, err := strconv.Atoi(splitRule[0])
		if err != nil {
			return nil, nil, errors.New("invalid left line: " + rawRule)
		}
		right, err := strconv.Atoi(splitRule[1])
		if err != nil {
			return nil, nil, errors.New("invalid right line: " + rawRule)
		}

		rules[i] = Rule{
			left:  left,
			right: right,
		}
	}

	//	Lines...
	rawLines := strings.Split(parts[1], "\n")
	lines := make([][]int, len(rawLines))
	for i, rawLine := range rawLines {
		split := strings.Split(rawLine, ",")
		line := make([]int, len(split))
		for j, s := range split {
			v, err := strconv.Atoi(s)
			if err != nil {
				return nil, nil, errors.New("invalid line: " + s)
			}
			line[j] = v
		}
		lines[i] = line
	}

	return rules, lines, nil
}
