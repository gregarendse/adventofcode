package main

import "fmt"

func main() {
	input := "2024/10/input.txt"
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
