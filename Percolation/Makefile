# Variables
CXX = g++
CXXFLAGS = -Wall -O2
SRC = CLustering/main.cpp CLustering/Cluster.cpp CLustering/Utils.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = percolation

# Default target
all: $(TARGET)

# Link object files to create executable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile .cpp files to .o files
CLustering/%.o: CLustering/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up object files and executable
clean:
	@echo "Removing object files and executable..."
	rm -f $(OBJ) $(TARGET)

# Remove all .exe files in the CLustering directory
clean_exe:
	@echo "Removing all .exe files in CLustering/..."
	rm -f CLustering/*.exe ./*.exe

# Remove all .txt files in both CLustering and data directories
clean_txt:
	@echo "Removing all .txt files in CLustering/ and data/..."
	rm -f CLustering/*.txt data/*.txt

# Full cleanup (object files, executables, text files)
clean_all:
	@echo "Performing full cleanup, keeping only .cpp and .h files..."
	rm -rf $(OBJ) $(TARGET) CLustering/*.o CLustering/*.exe CLustering/*.txt data/*.txt ./*.exe
