# Variables
CXX = g++
CXXFLAGS = -Wall -O2 -fopenmp
SRC_DIR = CLustering
DATA_DIR = data
SRC = $(SRC_DIR)/main.cpp $(SRC_DIR)/Cluster.cpp $(SRC_DIR)/Utils.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = percolation

# Default target
all: $(TARGET)

# Link object files to create executable
$(TARGET): $(OBJ)
	@echo "Linking object files to create executable..."
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile .cpp files to .o files
$(SRC_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "Compiling $<..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up object files and executable
clean:
	@echo "Removing object files and executable..."
	rm -f $(OBJ) $(TARGET)

# Remove all .exe files in the SRC_DIR directory
clean_exe:
	@echo "Removing all .exe files in $(SRC_DIR)/ and current directory..."
	rm -f $(SRC_DIR)/*.exe ./*.exe

# Remove all .txt files in both SRC_DIR and DATA_DIR directories
clean_txt:
	@echo "Removing all .txt files in $(SRC_DIR)/ and $(DATA_DIR)/..."
	rm -f $(SRC_DIR)/*.txt $(DATA_DIR)/*.txt

# Full cleanup (object files, executables, text files)
clean_all:
	@echo "Performing full cleanup, keeping only .cpp and .h files..."
	rm -rf $(OBJ) $(TARGET) $(SRC_DIR)/*.o $(SRC_DIR)/*.exe $(SRC_DIR)/*.txt $(DATA_DIR)/*.txt ./*.exe

# Debugging build
debug: CXXFLAGS += -g -DDEBUG

debug: clean $(TARGET)
