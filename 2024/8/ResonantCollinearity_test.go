package main

import "testing"

func TestPartOne(t *testing.T) {
	testCases := []struct {
		expected int
		input    string
	}{
		{
			expected: 14,
			input:    "sample.txt",
		},
		{
			expected: 265,
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
			expected: 9,
			input:    "sample_2.txt",
		},
		{
			expected: 34,
			input:    "sample.txt",
		},
		{
			expected: 962,
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
