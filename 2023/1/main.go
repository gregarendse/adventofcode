package main

import (
	"fmt"
	"os"
	"strings"
)

func part_one(content string) int {
	var total int = 0

	for _, v := range strings.Split(string(content), "\n") {

		var numbers []int

		for _, c := range v {
			num := 0
			if '0' <= c && c <= '9' {
				num = int(c - '0')
				numbers = append(numbers, num)
			}

		}

		total += (numbers[0] * 10) + numbers[len(numbers)-1]

	}

	return total
}

func part_two(content string) int {
	var total int = 0

	for _, line := range strings.Split(string(content), "\n") {
		var numbers []int

		for i := 0; i < len(line); i++ {
			for j := i + 1; j < len(line); j++ {
				part := line[i:j]
				num := 0

				switch part {
				case "one", "1":
					num = 1
				case "two", "2":
					num = 2
				case "three", "3":
					num = 3
				case "four", "4":
					num = 4
				case "five", "5":
					num = 5
				case "six", "6":
					num = 6
				case "seven", "7":
					num = 7
				case "eight", "8":
					num = 8
				case "nine", "9":
					num = 9
				}

				if num != 0 {
					numbers = append(numbers, num)
				}
			}
		}
		fmt.Printf("%s: %d\n", string(line), (numbers[0]*10)+numbers[len(numbers)-1])

		total += (numbers[0] * 10) + numbers[len(numbers)-1]
	}

	return total
}

func main() {
	content, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}

	fmt.Println(part_one(string(content))) //	55130
	fmt.Println(part_two(string(content))) //	54985
}
