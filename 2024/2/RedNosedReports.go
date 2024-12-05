package main

import (
	"bytes"
	"log"
	"os"
	"strconv"
	"strings"
)

func PartOne(input string) (int, error) {

	reports, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	safeCount := 0

	for _, report := range reports {

		isSafe := ParseReport(report)

		log.Printf("%v : %v", report, isSafe)

		if isSafe {
			safeCount++
		}

	}

	return safeCount, nil
}

func ParseReport(report []int) bool {

	//	At the start assume the list is both increasing and decreasing
	decreasing := true
	increasing := true

	for i := range report {
		if i == 0 {
			continue
		}

		if report[i-1] == report[i] {
			return false
		}

		if report[i-1] > report[i] {
			if !decreasing {
				return false
			}
			increasing = false
		}
		if report[i-1] < report[i] {
			if !increasing {
				return false
			}
			decreasing = false
		}

		if report[i-1]-report[i] > 3 || report[i]-report[i-1] > 3 {
			return false
		}

	}

	return true
}

func PartTwo(input string) (int, error) {

	reports, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	safeCount := 0

	for _, report := range reports {

		if ParseReport(report) {
			safeCount++
			continue
		}

		for i := range report {
			subReport := make([]int, 0)
			subReport = append(subReport, report[:i]...)
			subReport = append(subReport, report[i+1:]...)

			isSafe := ParseReport(subReport)

			if isSafe {
				safeCount++
				break
			}

		}
	}

	return safeCount, nil
}

func parseFile(input string) ([][]int, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, err
	}

	file = bytes.TrimSpace(file)

	lines := strings.Split(string(file), "\n")
	reports := make([][]int, len(lines))

	for i, line := range lines {
		if len(line) == 0 {
			continue
		}

		fields := strings.Fields(line)
		report := make([]int, len(fields))
		for j, s := range fields {
			report[j], _ = strconv.Atoi(s)
		}

		reports[i] = report

	}
	return reports, nil
}
