#include "candidate.h"
#include <stdlib.h>
#include <time.h>  

using namespace std;

double* Candidate::gen(double min, double max, int size) {
    srand(time(NULL));
    double point[size];
    const int RANGE = 1000000;

    for (int i = 0; i < size; i++) {
        double x = (rand() % RANGE) * (max - min) / RANGE + min;
        point[i] = x;
    }
    return point;
}