#include "token.hpp"

using namespace std;

class RuntimeError {
public:
   Token token;
   RuntimeError(Token token, string message) {
      throw runtime_error(message);
      this->token = token;
  }
};