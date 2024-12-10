package main

import (
	"bytes"
	"log"
	"os"
	"strconv"
	"strings"
)

func PartOne(input string) (int, error) {
	heightMap, trailHeads, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	score := 0

	for _, trailHead := range trailHeads {
		trails, err := pathFinder(trailHead, heightMap)
		if err != nil {
			return 0, err
		}

		score += len(trails)

	}

	return score, nil

}

func PartTwo(input string) (int, error) {
	heightMap, trailHeads, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	score := 0

	for _, trailHead := range trailHeads {
		trails, err := uniquePathFinder(trailHead, heightMap)
		if err != nil {
			return 0, err
		}

		score += len(trails)

	}

	return score, nil
}

func parseFile(input string) (
	heightMap [][]int,
	startingPoints []Point,
	err error,
) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, nil, err
	}

	file = bytes.TrimSpace(file)

	lines := strings.Split(string(file), "\n")

	heightMap = make([][]int, len(lines))
	startingPoints = []Point{}

	for y, line := range lines {
		heightMap[y] = make([]int, len(line))
		for x, c := range line {
			height, err := strconv.Atoi(string(c))
			if err != nil {
				log.Fatalf("failed to parse height: %v", err)
				return nil, nil, err
			}

			heightMap[y][x] = height

			if height == 0 {
				//	Starting point
				startingPoints = append(startingPoints, Point{x, y})
			}
		}
	}

	return heightMap, startingPoints, nil
}

func pathFinder(trailHead Point, heightMap [][]int) ([]Trail, error) {

	var trails []Trail

	queue := make([]Trail, 0)
	queue = append(queue, Trail{path: nil, position: trailHead})

	visited := map[Point]bool{}

	for {
		if len(queue) == 0 {
			break
		}

		trail := queue[0]
		visited[trail.position] = true
		queue = queue[1:]

		if trail.position.height(heightMap) == 9 {
			//	Path complete
			trails = append(trails, trail)
			continue
		}

		next := trail.position.next(heightMap)
		for _, point := range next {
			if visited[point] {
				continue
			}
			visited[point] = true

			t := Trail{
				path:     append(trail.path, trail.position),
				position: point,
			}
			queue = append(queue, t)
		}
	}

	return trails, nil
}

func uniquePathFinder(trailHead Point, heightMap [][]int) ([]Trail, error) {

	var trails []Trail

	queue := make([]Trail, 0)
	queue = append(queue, Trail{path: nil, position: trailHead, visited: map[Point]bool{}})

	for {
		if len(queue) == 0 {
			break
		}

		trail := queue[0]
		trail.visited[trail.position] = true
		queue = queue[1:]

		if trail.position.height(heightMap) == 9 {
			//	Path complete
			//log.Printf("Found trail: %v\n", trail)
			trails = append(trails, trail)
			continue
		}

		next := trail.position.next(heightMap)
		for _, point := range next {
			if trail.visited[point] {
				continue
			}
			trail.visited[point] = true

			t := trail.copy()
			t.path = append(trail.path, trail.position)
			t.position = point

			queue = append(queue, t)
		}
	}

	return trails, nil
}

type Point struct {
	x int
	y int
}

func (p *Point) height(heightMap [][]int) int {
	return heightMap[p.y][p.x]
}

func (p *Point) add(point Point) Point {
	return Point{p.x + point.x, p.y + point.y}
}

func (p *Point) next(heightMap [][]int) []Point {
	movements := []Point{
		{x: 0, y: 1},  //	Up
		{x: 1, y: 0},  //	Right
		{x: 0, y: -1}, //	Down
		{x: -1, y: 0}, //	Left
	}

	var nexts []Point

	for _, movement := range movements {
		possibleNext := p.add(movement)

		if possibleNext.y >= 0 && possibleNext.y < len(heightMap) &&
			possibleNext.x >= 0 && possibleNext.x < len(heightMap[possibleNext.y]) {

			if possibleNext.height(heightMap)-p.height(heightMap) == 1 {
				nexts = append(nexts, possibleNext)
			}
		}
	}

	return nexts
}

type Trail struct {
	path     []Point
	position Point
	visited  map[Point]bool
}

func (t *Trail) copy() Trail {
	visited := make(map[Point]bool, len(t.visited))
	for point, b := range t.visited {
		visited[point] = b
	}

	path := make([]Point, len(t.path))
	for i, point := range t.path {
		path[i] = point
	}

	return Trail{
		path:     path,
		position: t.position,
		visited:  visited,
	}
}
