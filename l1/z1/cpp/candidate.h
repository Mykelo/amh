#ifndef CANDIDATE_H
#define CANDIDATE_H

class Candidate {
    public:
    double* gen(double min, double max, int size);
    virtual double* tweak(double* point, int size) {}
    virtual double* analyze(double* point, int size) {}
};

#endif