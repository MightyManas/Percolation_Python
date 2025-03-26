# Variables
CXX = g++
CXXFLAGS = -Wall -O2
SRC = main.cpp Cluster.cpp Utils.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = percolation

# Default target
all: $(TARGET)

# Link object files to create executable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile .cpp files to .o files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up object files and executable
clean:
	@echo "Removing object files and executable..."
	rm -f $(OBJ) $(TARGET)

# Remove only .exe files
clean_exe:
	@echo "Removing all .exe files..."
	find . -name "*.exe" -delete

# Remove only .txt files
clean_txt:
	@echo "Removing all .txt files..."
	find . -name "*.txt" -delete

# Remove everything (object files, executable, .exe and .txt files)
clean_all:
	@echo "Performing full cleanup: object files, executable, .exe, and .txt files..."
	rm -rf $(OBJ) $(TARGET) ./*.exe ./*.txt
	
