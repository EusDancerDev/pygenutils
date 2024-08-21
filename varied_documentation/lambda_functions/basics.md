# Lambda Function Basics

Here's the explanation about the usage of 'lambda' functions, including how to handle multiple arguments.

### Lambda Functions in Python

A `lambda` function in Python is a small anonymous function defined with the `lambda` keyword. It can take any number of arguments, but can only have one expression. The syntax is:

```python
lambda arguments: expression
```

#### Basic Example

Here's a simple example where a `lambda` function takes one argument and returns its square:

```python
square = lambda x: x ** 2
print(square(5))  # Output: 25
```

#### Multiple Arguments

`lambda` functions can take multiple arguments. Here’s an example where the `lambda` function takes two arguments and returns their sum:

```python
add = lambda x, y: x + y
print(add(3, 4))  # Output: 7
```

---

### Common Use Cases

#### Using with `map()`

The `map()` function applies a given function to all items in an input list. For instance, squaring each number in a list:

```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # Output: [1, 4, 9, 16, 25]
```

#### Using with `filter()`

The `filter()` function constructs an iterator from elements of an iterable for which a function returns true. For example, filtering out even numbers:

```python
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # Output: [2, 4]
```

#### Using with `sorted()`

The `sorted()` function returns a new sorted list from the elements of any iterable. You can use a `lambda` function to define a custom sorting key. For example, sorting a list of tuples by the second element:

```python
tuples = [(1, 'one'), (2, 'two'), (3, 'three')]
sorted_tuples = sorted(tuples, key=lambda x: x[1])
print(sorted_tuples)  # Output: [(1, 'one'), (3, 'three'), (2, 'two')]
```

---

### Using `lambda` with Multiple Arguments

`lambda` functions can handle multiple arguments just like regular functions. Here's a more detailed look at how to use `lambda` functions with multiple arguments in various contexts:

#### Basic Syntax

The basic syntax for a `lambda` function with multiple arguments is:

```python
lambda arg1, arg2, ..., argN: expression
```

#### Examples

1. **Sum of Two Numbers**

   A `lambda` function that takes two arguments and returns their sum:

   ```python
   add = lambda x, y: x + y
   print(add(3, 4))  # Output: 7
   ```

2. **Product of Three Numbers**

   A `lambda` function that takes three arguments and returns their product:

   ```python
   multiply = lambda x, y, z: x * y * z
   print(multiply(2, 3, 4))  # Output: 24
   ```

3. **String Concatenation**

   A `lambda` function that takes two string arguments and concatenates them:

   ```python
   concatenate = lambda s1, s2: s1 + " " + s2
   print(concatenate("Hello", "World"))  # Output: "Hello World"
   ```

#### Using with Functions that Accept Functions as Arguments

`lambda` functions with multiple arguments are particularly useful when working with higher-order functions like `map()`, `filter()`, and `sorted()`, which accept other functions as arguments.

1. **Using `map()` with Multiple Arguments**

   The `map()` function can accept multiple sequences (iterables), and the function provided must take as many arguments as there are sequences. For instance, summing corresponding elements from two lists:

   ```python
   list1 = [1, 2, 3]
   list2 = [4, 5, 6]
   summed = list(map(lambda x, y: x + y, list1, list2))
   print(summed)  # Output: [5, 7, 9]
   ```

2. **Using `sorted()` with a Complex Key**

   Sorting a list of tuples based on the sum of their elements:

   ```python
   tuples = [(1, 2), (3, 1), (2, 4)]
   sorted_tuples = sorted(tuples, key=lambda x: x[0] + x[1])
   print(sorted_tuples)  # Output: [(1, 2), (3, 1), (2, 4)]
   ```

3. **Custom Sorting with `sorted()`**

   Sorting a list of dictionaries by multiple keys using a `lambda` function:

   ```python
   people = [{'name': 'John', 'age': 25}, {'name': 'Jane', 'age': 30}, {'name': 'Dave', 'age': 25}]
   sorted_people = sorted(people, key=lambda person: (person['age'], person['name']))
   print(sorted_people)  
   # Output: [{'name': 'Dave', 'age': 25}, {'name': 'John', 'age': 25}, {'name': 'Jane', 'age': 30}]
   ```

### Practical Examples

1. **Filtering Based on Multiple Conditions**

   Using `filter()` to get items from a list of tuples where the first element is greater than 2 and the second element is less than 5:

   ```python
   data = [(1, 2), (3, 4), (5, 6), (7, 8)]
   filtered_data = list(filter(lambda x: x[0] > 2 and x[1] < 5, data))
   print(filtered_data)  # Output: [(3, 4)]
   ```

2. **Using with `reduce()`**

   Combining elements of a list into a single value based on a binary operation, such as finding the maximum product of pairs in a list:

   ```python
   from functools import reduce
   data = [(1, 2), (3, 4), (5, 6)]
   max_product = reduce(lambda x, y: x if x[0] * x[1] > y[0] * y[1] else y, data)
   print(max_product)  # Output: (5, 6)
   ```

---

### Limitations

While `lambda` functions are syntactically convenient, they are limited to a single expression. They are often used for simple operations and are not a substitute for regular functions that may need more complex logic or multiple expressions.

## Summary

- `lambda` functions provide a concise way to create small, anonymous functions.
- They are commonly used with functions like `map()`, `filter()`, and `sorted()`.
- `lambda` functions can take multiple arguments but are limited to a single expression.

By understanding and using `lambda` functions appropriately, you can write more concise and readable code for specific use cases.

## Conclusion

Using `lambda` functions with multiple arguments can greatly enhance the flexibility and readability of your code, especially when working with functions that operate on sequences or collections. They allow you to write concise, inline functions that are useful for simple operations and can be passed as arguments to higher-order functions.
