# **Assertion in Python**

## Overview

* Assertions in Python are statements that assert or enforce certain conditions to be true in the code.
* They are primarily used for debugging purposes to check that certain conditions hold true at specific points in the code.
  When an assertion fails, it raises an AssertionError exception, indicating that something unexpected has occurred.

Here's a simple example:

```python
def divide(x, y):
    assert y != 0, "Cannot divide by zero!"
    return x / y

print(divide(10, 2))  # Output: 5.0
print(divide(10, 0))  # AssertionError: Cannot divide by zero!
```

In this example, the `assert` statement checks if the denominator `y` is not zero before performing the division.
If `y` is zero, it raises an AssertionError with the specified error message.

## Assertion in production environments
* Assertions are commonly used to check conditions or errors that should never occur in a well-tested and properly functioning program.
  That is to say, no error handling is desired when using assertion, this is used to enforce certain conditions 
  that are expected to be true at specific points in the code,
  
* They're particularly useful during development and debugging to catch potential issues early on
  during the development, as a debugging aid.<br>
  However, they can be disabled in a production environment to improve performance, as they incur a slight overhead.

* If the condition specified in an assertion fails, it indicates a bug or an unexpected situation in the code.
  Therefore, assertions are primarily used for debugging and ensuring that the code behaves as intended during development.

* Unlike error handling with try-except blocks, where you anticipate and handle specific errors that might occur during runtime,
  assertions are meant to be disabled in production code.
  This is because they impose a performance overhead, and failing assertions in a production environment
  could indicate a serious issue that needs immediate attention and fixing, rather than just handling the error gracefully.
  
* While it might be necessary in some cases for specific error logging or recovery procedures, in general,
  assertion errors should not occur if the code is working properly.

### Try-except blocks

* You can indeed use a try-except structure to achieve similar error handling as an assertion,
  but there are some differences in how they are used and their intended purposes.

Here's the same example using a try-except structure:

```python
def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero!")
    return result

print(divide(10, 2))  # Output: 5.0
print(divide(10, 0))  # ValueError: Cannot divide by zero!
```

* In this version, instead of checking the condition with an assertion, we perform the division inside a try block.
  If a ZeroDivisionError occurs (i.e., when `y` is zero), the except block is executed, and a ValueError is raised with the specified error message.

### Mathematical conditional structures

* In the mathematical scope, assertions still serve as an alternative to the conditional structures.
  For example, `2 <= x <= 5` is equivalent to the conditional structure `if (x >= 2) and (x <= 5)`, 
  but in a more compact and elegant form, closer to natural language.

* To that, a try-except blocks can be incorporated to catch the AssertionError and respond accordingly.

Here's an example:

```python
try:
    assert 2 <= x <= 5, "x should be between 2 and 5"
except AssertionError as e:
    print("Assertion error:", e)
    # Handle the assertion error here, if necessary
```

In this example, if the condition `2 <= x <= 5` fails, an AssertionError will be raised. 
The try-except block catches this error, and it can be handled it as needed within the except block.

## Summary

* While both approaches can be used to handle errors, they serve different purposes:

	1. Assertions (`assert`): Used to check conditions that should always be true during development. <br>
							  They're primarily for debugging and ensuring that your code is behaving as expected.<br>
							  They're typically disabled in production code for performance reasons.

	2. Try-except: Used for general error handling, allowing you to catch and respond to specific exceptions that might occur during runtime.<br>
				   It's more versatile than assertions and is suitable for handling a wider range of errors, including those that can occur during normal program execution.

* Technically, try-except structures can be used to handle errors in Python code.
  However, it's important to understand that assertions are primarily used for debugging purposes, 
  checking conditions that should never occur if the code is working correctly,
  and encountering an assertion error typically indicates a serious issue with the code
  that needs to be addressed rather than gracefully handled.
  
* This provides clearer intent and easier debugging during development.
