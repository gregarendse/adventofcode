package main

import (
	"testing"
)

func TestPartOne(t *testing.T) {
	testCases := []struct {
		expected int
		input    string
	}{
		{
			expected: 480,
			input:    "sample.txt",
		},
		{
			expected: 26810,
			input:    "input.txt",
		},
	}

	for i, testCase := range testCases {
		t.Logf("Case #%d: %v", i+1, testCase.input)
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
			expected: 875318608908,
			input:    "sample.txt",
		},
		{
			expected: 108713182988244,
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
