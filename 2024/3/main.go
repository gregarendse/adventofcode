package main

import "fmt"

func main() {
	input := "2024/3/input.txt"
	partOne, err := PartOne(input)
	if err != nil {
		panic(err)
	}
	fmt.Println(partOne)

	partTwo, err := PartTwo(input)
	if err != nil {
		panic(err)
	}
	fmt.Println(partTwo)
}