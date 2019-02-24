#include <string>
#include <sstream>

#include <boost/any.hpp>

#include "tokentype.hpp"

using namespace std;

using namespace tokentype;

namespace token {
  class Token {
  public:
    TokenType type;
    string lexeme;
    boost::any literal;
    int line;

    Token() {}

    Token(TokenType type, std::string lexeme, boost::any literal, int line) {
      this->type = type;
      this->lexeme = lexeme;
      this->literal = literal;
      this->line = line;
    }

    template <typename T>
    std::string to_string(const T& object) {
      std::ostringstream ss;
      ss << object;
      return ss.str();
    }
  };
}
