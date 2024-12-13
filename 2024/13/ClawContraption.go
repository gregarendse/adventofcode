package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func PartOne(input string) (int, error) {
	clawMachines, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	total := 0

	for _, machine := range clawMachines {
		a, b, err := machine.Solve()
		if err != nil {
			continue
		}

		if a >= 0 && a <= 100 && b >= 0 && b <= 100 {
			cost := (3 * a) + b
			total += cost
		}
	}

	return total, nil

}

func PartTwo(input string) (int, error) {
	clawMachines, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	total := 0

	for _, machine := range clawMachines {
		machine.PrizePosition.y += 10000000000000
		machine.PrizePosition.x += 10000000000000

		a, b, err := machine.Solve()
		if err != nil {
			continue
		}

		cost := (3 * a) + b
		total += cost
	}

	return total, nil
}

func parseFile(input string) ([]*ClawMachine, error) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, err
	}

	file = bytes.TrimSpace(file)

	machines := strings.Split(string(file), "\n\n")
	var clawMachines []*ClawMachine

	for _, machine := range machines {
		parts := strings.Split(machine, "\n")
		clawMachine := ClawMachine{}
		for _, part := range parts {
			split := strings.Split(part, ":")
			switch split[0] {
			case "Button A":
				position, err := parse(split)
				if err != nil {
					return nil, err
				}
				clawMachine.A = position
			case "Button B":
				position, err := parse(split)
				if err != nil {
					return nil, err
				}
				clawMachine.B = position
			case "Prize":
				position, err := parse(split)
				if err != nil {
					return nil, err
				}
				clawMachine.PrizePosition = position
			default:
				return nil, fmt.Errorf("unknown prefix %s", split[0])
			}
		}
		clawMachines = append(clawMachines, &clawMachine)

	}

	return clawMachines, nil
}

func parse(split []string) (*Position, error) {
	values := strings.Split(split[1], ",")
	position := &Position{}
	for _, v := range values {
		v = strings.TrimSpace(v)
		atoi, err := strconv.Atoi(v[2:])
		if err != nil {
			fmt.Printf("Failed to parse split: %v, %v\n", v[2:], err)
			return nil, err
		}

		switch v[0] {
		case 'X':
			position.x = atoi
		case 'Y':
			position.y = atoi
		default:
			fmt.Printf("Unknown identifier: %v\n", v[0])
			return nil, fmt.Errorf("unknown identifier %v", v[0])
		}
	}
	return position, nil
}

type Position struct {
	x, y int
}

type ClawMachine struct {
	PrizePosition *Position
	A             *Position
	B             *Position
}

func (c *ClawMachine) CalculateButtonB() (int, error) {
	//N * A.x + M * B.x = X
	//N * A.y + M * B.y = Y
	Y := c.PrizePosition.y
	X := c.PrizePosition.x
	Ax := c.A.x
	Ay := c.A.y
	Bx := c.B.x
	By := c.B.y

	//M = (Y * A.x - X * A.y) / (B.y * A.x - B.x * A.y)
	if (Y*Ax-X*Ay)%(By*Ax-Bx*Ay) != 0 {
		return 0, fmt.Errorf("not reachable")
	}
	return (Y*Ax - X*Ay) / (By*Ax - Bx*Ay), nil
}
func (c *ClawMachine) CalculateButtonA() (int, error) {
	//N * A.x + M * B.x = X
	//N * A.y + M * B.y = Y
	Y := c.PrizePosition.y
	X := c.PrizePosition.x
	Ax := c.A.x
	Ay := c.A.y
	Bx := c.B.x
	By := c.B.y

	//N = (Y * Bx - X * By) / ( Ay * Bx - Ax * By )
	if (Y*Bx-X*By)%(Ay*Bx-Ax*By) != 0 {
		return 0, fmt.Errorf("not reachable")
	}
	return (Y*Bx - X*By) / (Ay*Bx - Ax*By), nil
}

func (c *ClawMachine) Solve() (int, int, error) {

	buttonAPresses, err := c.CalculateButtonA()
	if err != nil {
		return 0, 0, nil
	}
	buttonBPresses, err := c.CalculateButtonB()
	if err != nil {
		return 0, 0, nil
	}

	return buttonAPresses, buttonBPresses, nil
}

func (c *ClawMachine) String() string {
	return fmt.Sprintf("(%v, %v, %v)", c.A, c.B, c.PrizePosition)
}
