#ifndef FUNCTION_H
#define FUNCTION_H

class Function {
    public:
    virtual float compute(float* point, int size) = 0;
};

#endif