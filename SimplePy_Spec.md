# SimplePy Language Specification

## Overview

SimplePy is a minimal subset of Python designed for educational purposes. It supports basic programming constructs necessary to implement simple algorithms.

## Data Types

*   `integer`:  Whole numbers (e.g., -2, 0, 10).

## Variables

*   Variables are declared implicitly upon assignment.
*   Variable names must start with a letter and can be followed by letters or numbers.

## Operators

*   **Arithmetic:** `+` (addition), `-` (subtraction), `*` (multiplication), `/` (integer division), `%` (modulo).
*   **Comparison:**  `==` (equal to), `!=` (not equal to), `>` (greater than), `<` (less than), `>=` (greater than or equal to), `<=` (less than or equal to).
*   **Assignment:** `=`

## Control Flow

*   **Conditional:**
    ```python
    if condition:
        # statements
    else:
        # statements
    ```

*   **Looping:**
    ```python
    while condition:
        # statements
    ```

## Input/Output

*   `print(expression)`: Outputs the value of the expression.
*   `input()`: Reads an integer from standard input. Assign value from input to some integer variable: `x = input()`.

## Comments

*   Single-line comments start with `#`.

## Example

(Example code will be added later)

## Limitations

*   No functions, lists, strings, or other complex data types.
*   No recursion.
*   Limited error handling in the interpreter.
