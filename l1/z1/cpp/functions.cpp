#include "functions.h"
#include <math.h>

double HappyCat::compute(double* point, int size) {
    double norm = 0;
    double sum = 0;
    for (int i = 0; i < size; i++) {
        norm += point[i] * point[i];
        sum += point[i];
    }
    norm = sqrt(norm);

    return pow(pow(norm * norm - 4, 2.0), 0.125) + 0.25 * (0.5 * norm * norm + sum) + 0.5;
}

double Griewank::compute(double* point, int size) {
    double sum = 0;
    double product = 1;
    for (int i = 0; i < size; i++) {
        sum += point[i] * point[i] / 4000;
        product *= cos(point[i] / sqrt(i + 1));
    }

    return 1 + sum - product;
}