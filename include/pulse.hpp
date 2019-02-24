#ifndef PULSE_SRC_PULSE_H_
#define PULSE_SRC_PULSE_H_

#include <string>

#include "token.hpp"
#include "interpreter.hpp"
#include "runtime_err.hpp"

class Pulse
{
  public:
    static void run_file(const char *path);

    static void run_prompt();

    static void run(const std::string &source);

    static void error(int line, const std::string &message);

    static void error(Token token, const std::string &message);

    static void runtime_error(RuntimeErr err);

  private:
    static bool had_error;

    static bool had_runtime_error;

    static void report(int line, const std::string &occurrence, const std::string &message);
};

#endif
