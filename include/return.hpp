#ifndef PULSE_RETURN_HPP
#define PULSE_RETURN_HPP

#include <stdexcept>

class Return : public std::runtime_error
{
  public:
    Return() : runtime_error("Return sentinel") {}
};

#endif 
