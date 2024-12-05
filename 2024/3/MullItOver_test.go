package main

import "testing"

func TestHistorianHysteria(t *testing.T) {

	expected := 161

	partOne, err := PartOne("sample.txt")

	if err != nil {
		t.Error(err)
	}

	if partOne != expected {
		t.Errorf("Expected %d, got %d", expected, partOne)
	}
}

func TestPartTwo(t *testing.T) {

	expected := 48

	partTwo, err := PartTwo("sample_2.txt")

	if err != nil {
		t.Error(err)
	}

	if partTwo != expected {
		t.Errorf("Expected %v, got %v", expected, partTwo)
	}
}
