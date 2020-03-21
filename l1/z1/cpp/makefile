FLAGS = -std=c++11

main: functions.o gaussianSteepestAscent.o
	clang++ $(FLAGS) -o main functions.o gaussianSteepestAscent.o -c main.cpp

functions.o: functions.cpp
	clang++ $(FLAGS) -o functions.o -c functions.cpp

gaussianSteepestAscent.o: gaussianSteepestAscent.cpp
	clang++ $(FLAGS) -o gaussianSteepestAscent.o -c gaussianSteepestAscent.cpp