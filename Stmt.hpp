  interface Visitor<R> {
    R visitBlockSTMT(Block STMT);
    R visitExpressionSTMT(Expression STMT);
    R visitIfSTMT(If STMT);
    R visitPrintSTMT(Print STMT);
    R visitVarSTMT(Var STMT);
    R visitExpr condition, Stmt bodySTMT(Expr condition, Stmt body STMT);
  }
  static class Block extends Stmt {
    Block(vector<stmt> statements) {
      this.statements = statements;
    }

    <R> R accept(Visitor<R> visitor) {
      return visitor.visitBlockStmt(this);
    }

    final vector<stmt> statements;
  }
  static class Expression extends Stmt {
    Expression(Expr expression) {
      this.expression = expression;
    }

    <R> R accept(Visitor<R> visitor) {
      return visitor.visitExpressionStmt(this);
    }

    final Expr expression;
  }
  static class If extends Stmt {
    If(Expr condition, Stmt thenBranch, Stmt elseBranch) {
      this.condition = condition;
      this.thenBranch = thenBranch;
      this.elseBranch = elseBranch;
    }

    <R> R accept(Visitor<R> visitor) {
      return visitor.visitIfStmt(this);
    }

    final Expr condition;
    final Stmt thenBranch;
    final Stmt elseBranch;
  }
  static class Print extends Stmt {
    Print(Expr expression) {
      this.expression = expression;
    }

    <R> R accept(Visitor<R> visitor) {
      return visitor.visitPrintStmt(this);
    }

    final Expr expression;
  }
  static class Var extends Stmt {
    Var(Token name, Expr initializer) {
      this.name = name;
      this.initializer = initializer;
    }

    <R> R accept(Visitor<R> visitor) {
      return visitor.visitVarStmt(this);
    }

    final Token name;
    final Expr initializer;
  }
  static class Expr condition, Stmt body extends Stmt {
    Expr condition, Stmt body() {
    }

    <R> R accept(Visitor<R> visitor) {
      return visitor.visitExpr condition, Stmt bodyStmt(this);
    }

  }
package com.siddhartha.lox;

import java.util.List;

abstract class Stmt {

  abstract <R> R accept(Visitor<R> visitor);
}
