package main

import "testing"

func TestPartOne(t *testing.T) {
	testCases := []struct {
		expected int
		input    string
	}{
		{
			expected: 143,
			input:    "sample.txt",
		},
		{
			expected: 5639,
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
			expected: 123,
			input:    "sample.txt",
		},
		{
			expected: 5273,
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
