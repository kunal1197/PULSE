#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

#include "resolver.hpp"
#include "ast_deleter.hpp"
#include "expr.hpp"
#include "interpreter.hpp"
#include "pulse.hpp"
#include "parser.hpp"
#include "stmt.hpp"
#include "scanner.hpp"
#include "token.hpp"
#include "runtime_err.hpp"

bool Pulse::had_error = false;
bool Pulse::had_runtime_error = false;

void Pulse::run_file(const char *path)
{
    std::string pathCheck(path);
    if(pathCheck.substr(pathCheck.find_last_of(".") + 1) == "pul") {
      const std::ifstream file(path);
      std::stringstream src_buffer;

      src_buffer << file.rdbuf();

      run(src_buffer.str());

      if (had_error)
          exit(65); // data format error
      if (had_runtime_error)
          exit(70);
    } else {
      had_error = true;
      error(0, "Incorrect file extension. Expecting .pul file!");
    }

}

void Pulse::run_prompt()
{
    std::string curr_line;

    while (true)
    {
        std::cout<<"Pulse> ";
        had_error = false; // reset error status
        getline(std::cin, curr_line);

        if(curr_line == "exit();") {
          break;
        }

        std::cout << "Pulse out:- ";
        run(curr_line);
        std::cout << std::endl;
    }
}

void Pulse::run(const std::string &source)
{
    Scanner scanner(source);
    const std::vector<Token> tokens = scanner.scan_tokens();

    Parser parser(tokens);
    std::vector<Stmt *> statements = parser.parse();

    // Stop if there was a parsing error.
    if (had_error)
        return;

    Interpreter interpreter;

    Resolver resolver(&interpreter);
    resolver.resolve(statements);

    // Stop if there was a resolution error.
    if (had_error)
        return;

    interpreter.interpret(statements);

    AstDeleter deleter;
    deleter.recursive_delete(statements);
}

void Pulse::error(int line, const std::string &message)
{
    report(line, "", message);
}

void Pulse::error(Token token, const std::string &message)
{
    if (token.type == END_OF_FILE)
    {
        report(token.line, " at end", message);
    }
    else
    {
        report(token.line, " at '" + token.lexeme + "'", message);
    }
}

void Pulse::runtime_error(RuntimeErr err)
{
    std::cout << "[line " << err.token.line << "] "
              << err.what()
              << std::endl;

    had_runtime_error = true;
}

// Private

void Pulse::report(int line,
                 const std::string &occurrence,
                 const std::string &message)
{
    std::cout << "[line " << line << "] Error: "
              << occurrence << " : " << message
              << std::endl;

    had_error = true;
}
