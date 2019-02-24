#include <boost/any.hpp>

#include "token.hpp"

using namespace token;

class Expr {};

template <typename T>
class Visitor;

class Assign : public Expr {
public:
  Token name;
  Expr value;

  Assign(Token name, Expr value) {
    this->name = name;
    this->value = value;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitAssignExpr();
  }
};

class Binary : public Expr {
public:
  Expr left, right;
  Token op;

  Binary(Expr left, Token op, Expr right) {
    this->left = left;
    this->op = op;
    this->right = right;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitBinaryExpr();
  }
};

class Grouping : public Expr {
public:
  Expr expression;

  Grouping(Expr expression) {
    this->expression = expression;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitGroupingExpr();
  }
};

class Literal : public Expr {
public:
  boost::any expression;

  Literal(boost::any expression) {
    this->expression = expression;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitLiteralExpr();
  }
};

class Logical : public Expr {
public:
  Expr left, right;
  Token op;

  Logical(Expr left, Token op, Expr right) {
    this->left = left;
    this->op = op;
    this->right = right;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitLogicalExpr();
  }
};

class Unary : public Expr {
public:
  Token op;
  Expr right;

  Unary(Token op, Expr right) {
    this->op = op;
    this->right = right;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitUnaryExpr();
  }
};

class Variable : public Expr {
public:
  Token name;

  Variable(Token name) {
    this->name = name;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitVariableExpr();
  }
};

namespace exprVisit {
  template <typename T>
  class Visitor {
  public:
    virtual T visitAssignExpr(Assign expr);
    virtual T visitBinaryExpr(Binary expr);
    virtual T visitGroupingExpr(Grouping expr);
    virtual T visitLiteralExpr(Literal expr);
    virtual T visitLogicalExpr(Logical expr);
    virtual T visitUnaryExpr(Unary expr);
    virtual T visitVariableExpr(Variable expr);
  };
}
