package main

import (
	"log"
	"os"
	"strings"
)

func PartOne(s string) (int, error) {
	input, err := parseFile(s)
	if err != nil {
		log.Fatalf("parseFile() failed: %v", err)
		return 0, err
	}

	antiNodes := make(map[Position]struct{})

	for _, positions := range input.antenna {

		for _, first := range positions {
			for _, second := range positions {
				if first == second {
					continue
				}

				antiNode := first.AntiNode(second)

				if antiNode.WithinMap(input.mapSize) {
					antiNodes[antiNode] = struct{}{}
				}

			}
		}
	}

	return len(antiNodes), nil
}

func PartTwo(s string) (int, error) {
	input, err := parseFile(s)
	if err != nil {
		log.Fatalf("parseFile() failed: %v", err)
		return 0, err
	}

	antiNodes := make(map[Position]struct{})

	for _, positions := range input.antenna {

		for _, originalFirst := range positions {
			for _, originalSecond := range positions {
				if originalFirst == originalSecond {
					continue
				}

				first := originalFirst
				second := originalSecond
				antiNodes[first] = struct{}{}

				for {
					antiNode := first.AntiNode(second)

					if !antiNode.WithinMap(input.mapSize) {
						break
					}

					second = first
					first = antiNode

					antiNodes[antiNode] = struct{}{}
				}

			}
		}
	}

	return len(antiNodes), nil
}

func parseFile(input string) (*Input, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
		return nil, err
	}

	fileStr := strings.TrimSpace(string(file))

	lines := strings.Split(fileStr, "\n")
	antenna := make(map[string][]Position)
	mapSize := Size{}

	mapSize.height = len(lines)
	for y, line := range lines {
		mapSize.width = len(line)
		for x, c := range line {
			v := string(c)
			if v != "." && v != "#" {
				antenna[v] = append(antenna[v], Position{x, y})
			}
		}
	}

	return &Input{
		antenna: antenna,
		mapSize: mapSize,
	}, nil
}

type Input struct {
	antenna map[string][]Position
	mapSize Size
}

type Position struct {
	x, y int
}

func (p Position) AntiNode(position Position) Position {
	return Position{
		x: 2*p.x - position.x,
		y: 2*p.y - position.y,
	}
}

func (p Position) WithinMap(mapSize Size) bool {
	return p.x >= 0 && p.x < mapSize.width &&
		p.y >= 0 && p.y < mapSize.height
}

type Size struct {
	width, height int
}
