#include <map>

#include <boost/any.hpp>

#include "runtimeerror.hpp"

class Environment {
public:
  Environment *enclosing;
  map<string, boost::any> values;

  Environment() {
    enclosing = NULL;
  }

  Environment(Environment &enclosing) {
    this->enclosing = &enclosing;
  }

  boost::any get(Token name) {
    if(values.find(name.lexeme) != values.end()) {
      return values.find(name.lexeme)->second;
    }

    if(enclosing != NULL) return enclosing->get(name);

    throw RuntimeError(name, "Undefined variable '" + name.lexeme + "'.");
  }

  void assign(Token name, boost::any value) {
    if(values.find(name.lexeme) != values.end()) {
      values[name.lexeme] = value;
      return;
    }

    if(enclosing != NULL) {
      enclosing->assign(name, value);
      return;
    }

    throw RuntimeError(name, "Undefined variable '" + name.lexeme + "'.");
  }

  void define(string name, boost::any value) {
    values[name] = value;
  }
};
