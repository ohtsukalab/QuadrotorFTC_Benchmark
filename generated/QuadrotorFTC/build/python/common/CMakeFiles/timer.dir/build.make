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
include python/common/CMakeFiles/timer.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include python/common/CMakeFiles/timer.dir/compiler_depend.make

# Include the progress variables for this target.
include python/common/CMakeFiles/timer.dir/progress.make

# Include the compile flags for this target's objects.
include python/common/CMakeFiles/timer.dir/flags.make

python/common/CMakeFiles/timer.dir/timer.cpp.obj: python/common/CMakeFiles/timer.dir/flags.make
python/common/CMakeFiles/timer.dir/timer.cpp.obj: python/common/CMakeFiles/timer.dir/includes_CXX.rsp
python/common/CMakeFiles/timer.dir/timer.cpp.obj: C:/Users/ohtsu/OneDrive\ -\ Kyoto\ Univ/ToCheck/BenchmarkBook/Test/QuadrotorFTC_Benchmark/generated/QuadrotorFTC/python/common/timer.cpp
python/common/CMakeFiles/timer.dir/timer.cpp.obj: python/common/CMakeFiles/timer.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object python/common/CMakeFiles/timer.dir/timer.cpp.obj"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\common && C:\mingw64\bin\c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT python/common/CMakeFiles/timer.dir/timer.cpp.obj -MF CMakeFiles\timer.dir\timer.cpp.obj.d -o CMakeFiles\timer.dir\timer.cpp.obj -c "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\common\timer.cpp"

python/common/CMakeFiles/timer.dir/timer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/timer.dir/timer.cpp.i"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\common && C:\mingw64\bin\c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\common\timer.cpp" > CMakeFiles\timer.dir\timer.cpp.i

python/common/CMakeFiles/timer.dir/timer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/timer.dir/timer.cpp.s"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\common && C:\mingw64\bin\c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\common\timer.cpp" -o CMakeFiles\timer.dir\timer.cpp.s

# Object files for target timer
timer_OBJECTS = \
"CMakeFiles/timer.dir/timer.cpp.obj"

# External object files for target timer
timer_EXTERNAL_OBJECTS =

python/common/timer.cp38-win_amd64.pyd: python/common/CMakeFiles/timer.dir/timer.cpp.obj
python/common/timer.cp38-win_amd64.pyd: python/common/CMakeFiles/timer.dir/build.make
python/common/timer.cp38-win_amd64.pyd: C:/Users/ohtsu/AppData/Roaming/jupyterlab-desktop/jlab_server/libs/python38.lib
python/common/timer.cp38-win_amd64.pyd: python/common/CMakeFiles/timer.dir/linkLibs.rsp
python/common/timer.cp38-win_amd64.pyd: python/common/CMakeFiles/timer.dir/objects1
python/common/timer.cp38-win_amd64.pyd: python/common/CMakeFiles/timer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library timer.cp38-win_amd64.pyd"
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\common && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\timer.dir\link.txt --verbose=$(VERBOSE)
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\common && C:\mingw64\bin\strip.exe "C:/Users/ohtsu/OneDrive - Kyoto Univ/ToCheck/BenchmarkBook/Test/QuadrotorFTC_Benchmark/generated/QuadrotorFTC/build/python/common/timer.cp38-win_amd64.pyd"

# Rule to build all files generated by this target.
python/common/CMakeFiles/timer.dir/build: python/common/timer.cp38-win_amd64.pyd
.PHONY : python/common/CMakeFiles/timer.dir/build

python/common/CMakeFiles/timer.dir/clean:
	cd /d C:\Users\ohtsu\ONEDRI~1\ToCheck\BENCHM~1\Test\QUADRO~1\GENERA~1\QUADRO~1\build\python\common && $(CMAKE_COMMAND) -P CMakeFiles\timer.dir\cmake_clean.cmake
.PHONY : python/common/CMakeFiles/timer.dir/clean

python/common/CMakeFiles/timer.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\python\common" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\python\common" "C:\Users\ohtsu\OneDrive - Kyoto Univ\ToCheck\BenchmarkBook\Test\QuadrotorFTC_Benchmark\generated\QuadrotorFTC\build\python\common\CMakeFiles\timer.dir\DependInfo.cmake" --color=$(COLOR)
.PHONY : python/common/CMakeFiles/timer.dir/depend
