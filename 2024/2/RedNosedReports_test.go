package main

import "testing"

func TestHistorianHysteria(t *testing.T) {

	expected := 2

	partOne, err := PartOne("sample.txt")

	if err != nil {
		t.Error(err)
	}

	if partOne != expected {
		t.Errorf("Expected %d, got %d", expected, partOne)
	}
}

func TestPartTwo(t *testing.T) {

	expected := 4

	partTwo, err := PartTwo("sample.txt")

	if err != nil {
		t.Error(err)
	}

	if partTwo != expected {
		t.Errorf("Expected %v, got %v", expected, partTwo)
	}
}
