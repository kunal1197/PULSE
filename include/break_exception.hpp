#ifndef PULSE_BREAK_EXCEPTION_H
#define PULSE_BREAK_EXCEPTION_H

#include <exception>

class BreakException : public std::exception {
  virtual const char* what() const throw() {
    return "My exception";
  }
};

#endif
