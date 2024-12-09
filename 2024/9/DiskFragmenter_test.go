package main

import "testing"

func TestPartOne(t *testing.T) {
	testCases := []struct {
		expected int
		input    string
	}{
		{
			expected: 1928,
			input:    "sample.txt",
		},
		{
			expected: 6334655979668,
			input:    "input.txt",
		},
	}

	for i, testCase := range testCases {
		result, err := PartOne(testCase.input)
		if err != nil {
			t.Errorf("case %d: unexpected error: %s", i, err)
		}

		if result != testCase.expected {
			t.Errorf("case %d: expected %d, got %d", i, testCase.expected, result)
		}
	}
}

func TestPartTwo(t *testing.T) {
	testCases := []struct {
		expected int
		input    string
	}{
		{
			expected: 2858,
			input:    "sample.txt",
		},
		{
			expected: 6349492251099,
			input:    "input.txt",
		},
	}

	for i, testCase := range testCases {
		result, err := PartTwo(testCase.input)
		if err != nil {
			t.Errorf("case %d: unexpected error: %s", i, err)
		}

		if result != testCase.expected {
			t.Errorf("case %d: expected %d, got %d", i, testCase.expected, result)
		}
	}
}
