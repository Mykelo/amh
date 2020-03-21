#include <random>
#include "gaussianSteepestAscent.h"
#include "function.h"

using namespace std;

GaussianSteepestAscent::GaussianSteepestAscent(double variance) {
    this->distribution = new normal_distribution<double>(0, variance);
}

double* GaussianSteepestAscent::tweak(double* point, int size) {
    std::uniform_real_distribution<double> distribution(0.0, 1.0);
    double newPoint[size];
    double p = 1.0;
    for (int i = 0; i < size; i++) {

    }
}

double* GaussianSteepestAscent::analyze(double* point, int size, Function* f) {

}