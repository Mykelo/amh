#include "function.h"

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

class HappyCat : Function {
    double compute(double* point, int size);
};

class Griewank : Function {
    double compute(double* point, int size);
};

#endif