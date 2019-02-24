#include "expr.hpp"

using namespace token;

class Stmt {};

template <typename T>
class Visitor;

class Block : public Stmt {
public:
  vector<Stmt> statements;

  Block(vector<Stmt> statements) {
    this->statements = statements;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitBlockStmt(this);
  }
};

class Expression : public Stmt {
public:
  Expr expression;

  Expression(Expr expression) {
    this->expression = expression;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitExpressionStmt();
  }
};

class If : public Stmt {
public:
  Expr condition;
  Stmt thenBranch, elseBranch;

  If(Expr condition, Stmt thenBranch, Stmt elseBranch) {
    this->condition = condition;
    this->thenBranch = thenBranch;
    this->elseBranch = elseBranch;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    return visitor->visitIfStmt();
  }
};

class Print : public Stmt {
public:
  Expr expression;

  Print(Expr expression) {
    this->expression = expression;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    visitor->visitPrintStmt();
  }
};

class Var : public Stmt {
public:
  Token name;
  Expr initializer;

  Var(Token name, Expr initializer) {
    this->name = name;
    this->initializer = initializer;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    visitor->visitVarStmt();
  }
};

class While : public Stmt {
public:
  Expr condition;
  Stmt body;

  While(Expr condition, Stmt body) {
    this->condition = condition;
    this->body = body;
  }

  template <typename T>
  T accept(Visitor<T> visitor) {
    visitor.visitWhileStmt();
  }
};

namespace stmtVisit {
  template <typename T>
  class Visitor {
    virtual T visitBlockStmt(Block stmt);
    virtual T visitExpressionStmt(Expression stmt);
    virtual T visitIfStmt(If stmt);
    virtual T visitPrintStmt(Print stmt);
    virtual T visitVarStmt(Var stmt);
    virtual T visitWhileStmt(While stmt);
  };
}
