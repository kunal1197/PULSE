#include <iostream>

#include "pulse.hpp"
#include "ast_printer.hpp"
#include "token.hpp"
#include "expr.hpp"


int main(int argc, char **argv)
{
    if (argc > 2)
    {
        std::cout << "Usage: pulse [source file]" << std::endl;
        exit(0);
    }

    Pulse interpreter;

    if (argc == 2)
    {
        interpreter.run_file(argv[1]);
    }
    else
    {
        interpreter.run_prompt();
    }

    return 0;
}
