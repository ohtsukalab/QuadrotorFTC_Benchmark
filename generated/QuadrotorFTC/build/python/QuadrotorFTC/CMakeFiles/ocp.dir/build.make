# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\CMake\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\CMake\bin\cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build"

# Include any dependencies generated for this target.
include python/QuadrotorFTC/CMakeFiles/ocp.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include python/QuadrotorFTC/CMakeFiles/ocp.dir/compiler_depend.make

# Include the progress variables for this target.
include python/QuadrotorFTC/CMakeFiles/ocp.dir/progress.make

# Include the compile flags for this target's objects.
include python/QuadrotorFTC/CMakeFiles/ocp.dir/flags.make

python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj: python/QuadrotorFTC/CMakeFiles/ocp.dir/flags.make
python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj: python/QuadrotorFTC/CMakeFiles/ocp.dir/includes_CXX.rsp
python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj: C:/Users/ohtsu/OneDrive\ -\ Kyoto\ Univ/ToCheck/BenchmarkBook/Test/QuadrotorFTC_Benchmark/generated/QuadrotorFTC/python/QuadrotorFTC/ocp.cpp
python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj: python/QuadrotorFTC/CMakeFiles/ocp.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\QUADRO~1 && C:\mingw64\bin\c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj -MF CMakeFiles\ocp.dir\ocp.cpp.obj.d -o CMakeFiles\ocp.dir\ocp.cpp.obj -c "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\QuadrotorFTC\ocp.cpp"

python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ocp.dir/ocp.cpp.i"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\QUADRO~1 && C:\mingw64\bin\c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\QuadrotorFTC\ocp.cpp" > CMakeFiles\ocp.dir\ocp.cpp.i

python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ocp.dir/ocp.cpp.s"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\QUADRO~1 && C:\mingw64\bin\c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\QuadrotorFTC\ocp.cpp" -o CMakeFiles\ocp.dir\ocp.cpp.s

# Object files for target ocp
ocp_OBJECTS = \
"CMakeFiles/ocp.dir/ocp.cpp.obj"

# External object files for target ocp
ocp_EXTERNAL_OBJECTS =

python/QuadrotorFTC/ocp.cp38-win_amd64.pyd: python/QuadrotorFTC/CMakeFiles/ocp.dir/ocp.cpp.obj
python/QuadrotorFTC/ocp.cp38-win_amd64.pyd: python/QuadrotorFTC/CMakeFiles/ocp.dir/build.make
python/QuadrotorFTC/ocp.cp38-win_amd64.pyd: C:/Users/ohtsu/AppData/Roaming/jupyterlab-desktop/jlab_server/libs/python38.lib
python/QuadrotorFTC/ocp.cp38-win_amd64.pyd: python/QuadrotorFTC/CMakeFiles/ocp.dir/linkLibs.rsp
python/QuadrotorFTC/ocp.cp38-win_amd64.pyd: python/QuadrotorFTC/CMakeFiles/ocp.dir/objects1
python/QuadrotorFTC/ocp.cp38-win_amd64.pyd: python/QuadrotorFTC/CMakeFiles/ocp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library ocp.cp38-win_amd64.pyd"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\QUADRO~1 && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\ocp.dir\link.txt --verbose=$(VERBOSE)
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\QUADRO~1 && C:\mingw64\bin\strip.exe "C:/Users/ohtsu/OneDrive - Kyoto Univ/ToCheck/BenchmarkBook/Test/QuadrotorFTC_Benchmark/generated/QuadrotorFTC/build/python/QuadrotorFTC/ocp.cp38-win_amd64.pyd"

# Rule to build all files generated by this target.
python/QuadrotorFTC/CMakeFiles/ocp.dir/build: python/QuadrotorFTC/ocp.cp38-win_amd64.pyd
.PHONY : python/QuadrotorFTC/CMakeFiles/ocp.dir/build

python/QuadrotorFTC/CMakeFiles/ocp.dir/clean:
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\QUADRO~1 && $(CMAKE_COMMAND) -P CMakeFiles\ocp.dir\cmake_clean.cmake
.PHONY : python/QuadrotorFTC/CMakeFiles/ocp.dir/clean

python/QuadrotorFTC/CMakeFiles/ocp.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\QuadrotorFTC" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\python\QuadrotorFTC" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\python\QuadrotorFTC\CMakeFiles\ocp.dir\DependInfo.cmake" --color=$(COLOR)
.PHONY : python/QuadrotorFTC/CMakeFiles/ocp.dir/depend

