package main

import (
	"bytes"
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Direction int

const (
	UP Direction = iota
	RIGHT
	DOWN
	LEFT
)

func (d Direction) Next() Direction {
	switch d {
	case UP:
		return RIGHT
	case RIGHT:
		return DOWN
	case DOWN:
		return LEFT
	case LEFT:
		return UP
	default:
		panic("Invalid direction: " + strconv.Itoa(int(d)))
	}
}

type Guard struct {
	x         int
	y         int
	direction Direction
	Route     []Point
}

func (g *Guard) Copy() *Guard {
	newGuard := &Guard{
		x:         g.x,
		y:         g.y,
		direction: UP,
		Route: []Point{{
			x: g.x,
			y: g.y,
		}},
	}

	return newGuard
}

type Lab struct {
	Obstacle map[Point]string
	Size     struct {
		x int
		y int
	}
}

func (l *Lab) Copy() *Lab {
	newLab := &Lab{
		Obstacle: make(map[Point]string),
		Size:     l.Size,
	}

	for point, s := range l.Obstacle {
		newLab.Obstacle[point] = s
	}

	return newLab
}

func (g *Guard) move(lab *Lab) (int, bool, error) {

	var positionNext Point
	switch g.direction {
	case UP:
		positionNext = Point{
			x: g.x,
			y: g.y - 1,
		}
		break
	case RIGHT:
		positionNext = Point{
			x: g.x + 1,
			y: g.y,
		}
		break
	case DOWN:
		positionNext = Point{
			x: g.x,
			y: g.y + 1,
		}
		break
	case LEFT:
		positionNext = Point{
			x: g.x - 1,
			y: g.y,
		}
		break
	default:
		return len(g.Route), false, fmt.Errorf("invalid direction")
	}

	if lab.Obstacle[positionNext] == "#" {
		g.direction = g.direction.Next()
		return len(g.Route), true, nil
	}

	//	Check if guard leaves lab
	if positionNext.x < 0 || positionNext.y < 0 ||
		positionNext.x >= lab.Size.x || positionNext.y >= lab.Size.y {
		return len(g.Route), false, nil
	}

	g.x = positionNext.x
	g.y = positionNext.y
	g.Route = append(g.Route, Point{x: g.x, y: g.y})

	return len(g.Route), true, nil
}

func PartOne(input string) (int, error) {

	lab, guard, err := parseFile(input)

	if err != nil {
		return 0, err
	}

	distinctPoints, _, err := guard.findDistinctPoints(lab)
	if err != nil {
		return 0, err
	}
	return len(distinctPoints), nil
}

type State struct {
	x, y int
	d    Direction
}

func (g *Guard) findDistinctPoints(lab *Lab) (map[Point]bool, bool, error) {

	distinctState := map[State]bool{}
	distinctPoints := map[Point]bool{}

	for {
		movements := len(g.Route)

		distinctPoints[Point{
			x: g.x,
			y: g.y,
		}] = true

		_, ok, err := g.move(lab)
		if err != nil {
			return distinctPoints, false, err
		}
		if !ok {
			return distinctPoints, true, nil
		}

		currentPosition := State{
			x: g.x,
			y: g.y,
			d: g.direction,
		}
		state := distinctState[currentPosition]

		if movements == len(g.Route) {
			continue
		}

		if state == false {
			distinctState[currentPosition] = true
			continue
		}

		if state == true {
			return distinctPoints, false, nil
		}

		if len(g.Route)/len(distinctState) > 2 {
			return distinctPoints, false, errors.New("guard might be looping")
		}
	}
}

func PartTwo(input string) (int, error) {

	originalLab, originalGuard, err := parseFile(input)

	if err != nil {
		return 0, err
	}

	guard := originalGuard.Copy()
	lab := originalLab.Copy()

	distinctPoints, _, err := guard.findDistinctPoints(lab)
	if err != nil {
		return 0, err
	}

	guardLoopCount := 0

	if originalGuard.x == guard.Route[0].x && originalGuard.y == guard.Route[0].y {

	} else {
		return 0, errors.New("first position is not starting position")
	}

	delete(distinctPoints, Point{
		x: originalGuard.x,
		y: originalGuard.y,
	})

	tasks := make(chan Point, len(distinctPoints))
	results := make(chan bool, len(distinctPoints))

	for i := 0; i < 4; i++ {
		go worker(tasks, results, originalLab, originalGuard)
	}

	for point := range distinctPoints {
		tasks <- point
	}

	close(tasks)

	for i := 0; i < len(distinctPoints); i++ {
		result := <-results
		if !result {
			guardLoopCount++
		}
	}

	return guardLoopCount, nil
}

func worker(tasks <-chan Point, results chan<- bool, lab *Lab, originalGuard *Guard) {
	for task := range tasks {
		updatedLab := lab.Copy()
		newGuard := originalGuard.Copy()

		updatedLab.Obstacle[task] = "#"

		_, ok, err := newGuard.findDistinctPoints(updatedLab)

		if err != nil {
			log.Printf("error: %v\n", err)
			continue
		}

		results <- ok
	}
}

type Point struct {
	x int
	y int
}

func parseFile(input string) (*Lab, *Guard, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, nil, err
	}

	file = bytes.TrimSpace(file)

	lines := strings.Split(string(file), "\n")

	labMap := make([][]string, len(lines))

	lab := Lab{Obstacle: make(map[Point]string)}
	var guard Guard

	for i, line := range lines {

		row := make([]string, len(line))

		for j, c := range line {
			row[j] = string(c)

			switch string(c) {
			case "#":
				point := Point{j, i}
				lab.Obstacle[point] = string(c)
				break
			case "^":
				guard = Guard{
					x:         j,
					y:         i,
					direction: UP,
					Route: []Point{{
						x: j,
						y: i,
					}},
				}
				break
			}
		}

		labMap[i] = row
	}

	lab.Size.y = len(lines)
	lab.Size.x = len(lines[0])

	return &lab, &guard, nil
}
