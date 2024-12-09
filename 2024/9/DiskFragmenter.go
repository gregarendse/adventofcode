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

func PartOne(input string) (int, error) {
	_, files, spaces, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	originalFirstSpace := spaces[0]
	originalLastFile := files[len(files)-1]

	for space := originalFirstSpace; space != nil; space = space.next {

		for file := originalLastFile; file != nil; file = file.prev {

			if file.length == 0 {
				continue
			}

			if file.index <= space.index {
				continue
			}

			lengthMin := min(space.length, file.length)
			newBlock := &Block{
				id:     file.id,
				index:  space.index,
				length: lengthMin,
			}

			files = append(files, newBlock)

			space.length = space.length - lengthMin
			space.index += lengthMin
			file.length = file.length - lengthMin

			if space.length == 0 {
				break
			}

		}
	}

	checkSum := 0
	for _, file := range files {
		for i := file.index; i < file.index+file.length; i++ {
			check := file.id * i
			checkSum += check
		}
	}

	return checkSum, nil
}

func PartTwo(input string) (int, error) {
	_, files, spaces, err := parseFile(input)
	if err != nil {
		return 0, err
	}

	originalFirstSpace := spaces[0]
	originalLastFile := files[len(files)-1]

	for space := originalFirstSpace; space != nil; space = space.next {

		for file := originalLastFile; file != nil; file = file.prev {

			if file.length == 0 {
				continue
			}

			if file.index <= space.index {
				continue
			}

			if file.length > space.length {
				continue
			}

			lengthMin := min(space.length, file.length)
			file.index = space.index

			space.length = space.length - lengthMin
			space.index += lengthMin

			if space.length == 0 {
				break
			}

		}
	}

	//// sort...
	//for i := 0; i < len(files); i++ {
	//	for j := i; j < len(files); j++ {
	//		if files[i].index > files[j].index {
	//			files[i], files[j] = files[j], files[i]
	//		}
	//	}
	//}
	//
	////	print...
	//compact := ""
	//for _, file := range files {
	//	for i := 0; i < file.length; i++ {
	//		compact += strconv.Itoa(file.id)
	//	}
	//}
	//log.Println(compact)
	////	Actual:		0099811188827773336446555665
	////	Expected: 	0099811188827773336446555566

	checkSum := 0
	for _, file := range files {
		//log.Printf("%v\n", file)
		for i := file.index; i < file.index+file.length; i++ {
			check := file.id * i
			//log.Printf("%d * %d = %d\n", i, file.id, check)
			checkSum += check
		}
	}

	return checkSum, nil
}

func parseFile(input string) (
	blocks []*Block,
	files []*Block,
	freeSpace []*Block,
	err error,
) {
	file, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("failed to read input: %v", err)
		return nil, nil, nil, err
	}

	file = bytes.TrimSpace(file)

	lines := strings.Split(string(file), "\n")

	if len(lines) != 1 {
		return nil, nil, nil, errors.New("failed to parse input")
	}

	line := lines[0]

	blocks = make([]*Block, len(line))
	files = make([]*Block, (len(line)+1)/2)
	freeSpace = make([]*Block, (len(line)+1)/2)

	var filePrev *Block = nil
	var spacePrev *Block = nil

	index := 0

	for i, c := range line {
		length, err := strconv.Atoi(string(c))
		if err != nil {
			return nil, nil, nil, fmt.Errorf("failed to parse line %d: %v", i, err)
		}
		if length == 0 {
			// Ignore empty blocks
			continue
		}
		j := i / 2
		blocks[i] = &Block{
			id:     j,
			index:  index,
			length: length,
		}
		index += length
		if i%2 != 0 {
			freeSpace[j] = blocks[i]
			freeSpace[j].prev = spacePrev
			if spacePrev != nil {
				spacePrev.next = freeSpace[j]
			}
			spacePrev = freeSpace[j]
		} else {
			files[j] = blocks[i]
			files[j].prev = filePrev
			if filePrev != nil {
				filePrev.next = files[j]
			}
			filePrev = files[j]
		}

	}

	return blocks, files, freeSpace, nil
}

type Block struct {
	id     int
	index  int
	length int

	next *Block
	prev *Block
}
