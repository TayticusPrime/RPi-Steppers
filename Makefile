# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++11 -Wall

# Source and output files
SRC = main.cpp
OUT = output/main

# Default target: compile and run
all: $(OUT)

# Compile the program
$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(OUT)

# Run the program
run: $(OUT)
	./$(OUT)

# Clean up generated files
clean:
	rm -f $(OUT)
