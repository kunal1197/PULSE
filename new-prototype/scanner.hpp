#include <string>
#include <vector>
#include <map>

#include <boost/any.hpp>

#include "token.hpp"

using namespace std;


class Scanner {
public:
  string source;
  vector<Token> tokens;

  int start;
  int current;
  int line;

  map<string, TokenType> keywords;

  void map_init() {
    keywords["and"] = AND;
    keywords["class"] = CLASS;
    keywords["else"] = ELSE;
    keywords["false"] = FALSE;
    keywords["for"] = FOR;
    keywords["fun"] = FUN;
    keywords["if"] = IF;
    keywords["nil"] = NIL;
    keywords["or"] = OR;
    keywords["print"] = PRINT;
    keywords["return"] = RETURN;
    keywords["super"] = SUPER;
    keywords["this"]= THIS;
    keywords["true"] = TRUE;
    keywords["var"] = VAR;
    keywords["while"] = WHILE;
  }

  Scanner(string source) {
    map_init();
    this->source = source;
    start = 0;
    current = 0;
    line = 1;
  }

  vector<Token> scanTokens() {
    while(!isAtEnd()) {
      start = current;
      scanToken();
    }

    tokens.push_back(Token(EOFF, "", NULL, line));
    return tokens;
  }

  void scanToken() {
    char c = advance();
    switch(c) {
      case '(': addToken(LEFT_PAREN); break;
      case ')': addToken(RIGHT_PAREN); break;
      case '{': addToken(LEFT_BRACE); break;
      case '}': addToken(RIGHT_BRACE); break;
      case ',': addToken(COMMA); break;
      case '.': addToken(DOT); break;
      case '-': addToken(MINUS); break;
      case '+': addToken(PLUS); break;
      case ';': addToken(SEMICOLON); break;
      case '*': addToken(STAR); break;
      case '%': addToken(MODULO); break;
      case '!': addToken(match('=') ? BANG_EQUAL : BANG); break;
      case '=': addToken(match('=') ? EQUAL_EQUAL : EQUAL); break;
      case '<': addToken(match('=') ? LESS_EQUAL : LESS); break;
      case '>': addToken(match('=') ? GREATER_EQUAL : GREATER); break;
      case '/':
          if(match('/')) {
            while(peek() != '\n' && !isAtEnd()) advance();
          } else if(match('*')) {
            while(peek() != '*' && !isAtEnd()) {
              if(peek() == '\n') {
                line++;
              }
              advance();
            }
            advance();
            if(peek() == '/') advance();
            else
              Lox.error(line, "Improperly closed multi-comment statement.");
          } else {
            addToken(SLASH);
          }
          break;
      case ' ':
      case '\r':
      case '\t':
          break;
      case '\n':
          line++;
          break;
      case '"': string(); break;
      default:
          if(isDigit(c)) {
            number();
          } else if(isAlpha(c)) {
            identifier();
          } else {
            Lox.error(line, "Unexpected character.");
          }
          break;
    }
  }

  void identifier() {
    while(isAlphaNumeric(peek())) advance();

    string text = source.substr(start, current);

    TokenType type;

    if(keywords.find(text) == keywords.end()) {
      type = IDENTIFIER;
    } else {
      type = keywords.find(text)->second;
    }

    addToken(type);
  }

  void number() {
    while(isDigit(peek())) advance();

    if(peek() == '.' && isDigit(peekNext())) {
      advance();

      while(isDigit(peek())) advance();
    }

    addToken(NUMBER, stod(source.substr(start, current)));
  }

  void String() {
    while(peek() != '"' && !isAtEnd()) {
      if(peek() == '\n') line++;
      advance();
    }

    if(isAtEnd()) {
      Lox.error(line, "Unterminated string.");
      return;
    }

    advance();

    string value = source.substr(start+1, current-1);
    addToken(STRING, value);
  }

  bool match(char expected) {
    if(isAtEnd()) return false;
    if(source[current] != expected) return false;

    current++;
    return true;
  }

  char peek() {
    if(isAtEnd()) return '\0';
    return source[current];
  }

  char peekNext() {
    if(current + 1 >= source.length()) return '\0';
    return source[current+1];
  }

  bool isAlpha(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
  }

  bool isAlphaNumeric(char c) {
    return isAlpha(c) || isDigit(c);
  }

  bool isDigit(char c) {
    return c >= '0' && c <= '9';
  }

  bool isAtEnd() {
    return current >= source.length();
  }

  char advance() {
    current++;
    return source[current-1];
  }

  void addToken(TokenType type) {
    addToken(type, NULL);
  }

  void addToken(TokenType type, boost::any literal) {
    string text = source.substr(start, current);
    tokens.push_back(Token(type, text, literal, line));
  }
};
