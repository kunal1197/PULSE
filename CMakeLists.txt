cmake_minimum_required(VERSION 3.10)
project(pulsepp)

set(CMAKE_CXX_STANDARD 11)

include_directories(include)

add_executable(pulsepp
        include/expr.hpp
        include/pulse.hpp
        include/scanner.hpp
        include/token.hpp
        src/cli.cpp
        src/pulse.cpp
        src/scanner.cpp
        src/token.cpp
        include/visitor.hpp
        src/parser.cpp
        include/parser.hpp
        src/interpreter.cpp
        include/interpreter.hpp
        src/ast_printer.cpp
        include/ast_printer.hpp
        include/interpreter_result.hpp
        src/interpreter_result.cpp
        include/visitable_types.hpp
        include/environment.hpp
        include/return.hpp
        src/resolver.cpp
        include/resolver.hpp
        include/runtime_err.hpp
        include/ast_deleter.hpp
        src/ast_deleter.cpp)
