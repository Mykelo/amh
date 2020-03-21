#include <random>
#include "candidate.h"
#include "function.h"

#ifndef GAUSSIAN_STEEPEST_ASCENT_H
#define GAUSSIAN_STEEPEST_ASCENT_H

class GaussianSteepestAscent : Candidate {
    private:
    std::default_random_engine generator;
    std::normal_distribution<double>* distribution;

    public:
    GaussianSteepestAscent(double variance);
    virtual double* tweak(double* point, int size) {}
    virtual double* analyze(double* point, int size, Function* f) {}
};

#endif