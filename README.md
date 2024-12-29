# SimplePy Interpreter Project

## Overview

This project implements a simple interpreter for "SimplePy," a minimal subset of the Python programming language. The interpreter is designed to execute basic algorithms and demonstrate fundamental programming constructs.

## Team Members

- [Giorgi Babunashvili] -
- [Rezi Gurguchiani] - 


## Language Specification

See the `SimplePy_Spec.md` file for a detailed description of the SimplePy language.

## Project Structure

*   `interpreter.py`: The main interpreter code (lexer, parser, interpreter).
*   `algorithms/`: Contains implementations of algorithms in SimplePy (will be added in a later commit).
* `SimplePy_Spec.md`: SimplePy language specification.
* `CONTRIBUTORS.md`: lists each team member's contributions.

## How to Run

1. **Prerequisites:** Make sure you have Python 3 installed on your system (you'll need it to run the interpreter locally).
2. **Navigate to the Project on GitHub:** Go to your repository on GitHub using your web browser.
3. **Download the Code:**
    *   Click the green "Code" button.
    *   Select "Download ZIP".
    *   Extract the downloaded ZIP file to a folder on your computer.
4. **Open a Terminal or Command Prompt:** Open a terminal or command prompt on your local machine.
5. **Navigate to the Project Directory:** Use the `cd` command to navigate to the directory where you extracted the project files. For example:

    ```bash
    cd Downloads/SimplePy_Interpreter-main 
    ```

    (Adjust the path according to where you extracted the ZIP file).
6. **Run the Interpreter:** Execute the following command to run the interpreter with a specific algorithm file:

    ```bash
    python interpreter.py algorithms/<algorithm_file_name>.simpy
    ```

    *   Replace `<algorithm_file_name>.simpy` with the actual name of the algorithm file you want to run (e.g., `1.simpy`, `2.simpy`, etc.).

7. **Provide Input:** If the algorithm requires input, the interpreter will prompt you to enter the input value(s) in the terminal. Enter the required values and press Enter.

8. **View Output:** The interpreter will execute the SimplePy code and print the output to the terminal.


## Example 

Here's how to run the "Sum of First N Numbers" algorithm (`sum_of_n.simpy`):

1. Download the code from the repository as a ZIP file and extract it.
2. Open a terminal or command prompt and navigate to the project directory.
3. Execute the following command in your terminal:

    ```bash
    python interpreter.py algorithms/sum_of_n.simpy
    ```

4. The interpreter will prompt you to enter an integer value for `n`. Enter a number (e.g., `10`) and press Enter.

5. The interpreter will output the sum of the first `n` numbers (e.g., `55` if you entered `10`).


## Testing

The interpreter has been tested with a set of algorithms implemented in SimplePy. These algorithms are located in the `algorithms` directory. Each `.simpy` file represents a different algorithm.

**To test the interpreter:**

1. Download the code from the repository as a ZIP file and extract it.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run each of the algorithm files (`.simpy` files in the `algorithms` directory) using the following command:

    ```bash
    python interpreter.py algorithms/<algorithm_file_name>.simpy
    ```

    Replace `<algorithm_file_name>.simpy` with the name of the algorithm file.
4. Provide appropriate input values when prompted.
5. Verify that the output produced by the interpreter matches the expected output for each algorithm.

**Test Cases:**

Here's a table summarizing the test cases for each algorithm:

| Algorithm File            | Description                                  | Example Input(s)          | Expected Output           |
| :------------------------ | :------------------------------------------- | :------------------------ | :------------------------ |
| `sum_of_n.simpy`          | Sum of First N Numbers                     | 5                         | 15                        |
|                           |                                              | 10                        | 55                        |
|                           |                                              | 0                         | 0                         |
| `factorial.simpy`         | Factorial of N                            | 5                         | 120                       |
|                           |                                              | 3                         | 6                         |
|                           |                                              | 0                         | 1                         |
| `gcd.simpy`               | GCD of Two Numbers                         | 48, 18                    | 6                         |
|                           |                                              | 12, 8                     | 4                         |
|                           |                                              | 5, 7                      | 1                         |
| `reverse_number.simpy`    | Reverse a Number                          | 1234                      | 4321                      |
|                           |                                              | 98765                     | 56789                     |
|                           |                                              | 1000                      | 1                         |
| `prime_check.simpy`       | Check if a Number is Prime                 | 7                         | 1 (True)                  |
|                           |                                              | 12                        | 0 (False)                 |
|                           |                                              | 1                         | 0                         |
| `palindrome_check.simpy`  | Check if a Number is Palindrome            | 121                       | 1 (True)                  |
|                           |                                              | 123                       | 0 (False)                 |
|                           |                                              | 7                         | 1                         |
| `largest_digit.simpy`     | Find the Largest Digit in a Number         | 3829                      | 9                         |
|                           |                                              | 12345                     | 5                         |
|                           |                                              | 999                       | 9                         |
| `sum_of_digits.simpy`     | Sum of Digits                              | 123                       | 6                         |
|                           |                                              | 9876                      | 30                        |
|                           |                                              | 5                         | 5                         |
| `multiplication_table.simpy` | Multiplication Table                    | 7                         | 7, 14, 21, ..., 70       |
|                           |                                              | 3                         | 3, 6, 9, ..., 30          |
| `fibonacci.simpy`         | Nth Fibonacci Number                       | 10                        | 34                        |
|                           |                                              | 1                         | 0                         |
|                           |                                              | 2                         | 1                         |

**Note:**

*   The `multiplication_table.simpy` algorithm will print the multiplication table up to 10.
*   In SimplePy, the result of dividing an integer by another integer is always an integer.
*   In SimplePy, the boolean values are represented by integers: `1` represents `True`, and `0` represents `False`.
