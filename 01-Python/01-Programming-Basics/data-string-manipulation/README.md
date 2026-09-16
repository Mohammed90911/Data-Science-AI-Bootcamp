The `String` class is one of the most used classes in Python and programming languages in general. A lot of built-in methods already exist to make life easier. Your goal in these exercises will be to:

- Learn to look for the right method, using the Python documentation
- Get familiar with using the Python interpreter to experiment with new methods and make them yours

The [IPython](https://ipython.org/) [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop), as the kernel for Jupyter, can be run with:

```bash
ipython
```

1. It **reads** the expression written by the user, which can be any valid Python expression like `"Hello"`, `2+2`, `"hello".upper()` ...
2. It **evaluates** the result of this expression.
3. It **prints** out the result.
4. It **loops** back to step 1, waiting for a new user input.

**Experiment with the following lines** in the IPython interpreter:

```python
# Python 3.7.1 (default, Dec 14 2018, 13:28:58)
# Type 'copyright', 'credits' or 'license' for more information
# IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: 1 + 1

In [2]: help(str.lower) # Quit help by hitting `Q` on the keyboard

In [3]: "A string object".lower()

In [4]: quit
```

In Python, everything (a string, an integer, a floating number, a list...) is an object. We can call methods on these objects. Such methods are called **instance methods** since they can only be called on instances of the class. The object on which we call the method is called the **receiver**.

You can read more about the difference between a function and a method [here](https://www.tutorialspoint.com/difference-between-method-and-function-in-python)

## Exercise

Open `string_methods.py` and implement all the functions.

Find the right Python methods of the [String class](https://docs.python.org/3/library/stdtypes.html#string-methods) to plug in and make the tests pass.

Code is all about being inventive and knowing how and where to look for the info you need! Often, the most difficult step is to ask Google the right question. To find the methods you'll need for this challenge, use:

- Google and [Stack Overflow](http://stackoverflow.com/)
- [The python doc](https://docs.python.org/3) if you have a rough idea of the method you are looking for.

When you think you've found the method you're looking for, and you think you know how to use it, use the Python interpreter to test this method on something! Experimenting on the Python interpreter is a crucial step for beginners.

💡 Everytime you implement a function in the file, passing more tests as you go by running `make`, please commit & push your progress!

```bash
git add string_methods.py
git commit -m "Progress on string_methods: XXX tests passing"
git push origin master
```

## Not passing the tests?

It's easy to get lost in the output of the `make` command. If your code doesn't pass the test, and you don't immediately see why, it's better to run the code directly and see what your function does.

Imagine your `add_comma()` function doesn't work. You can run `python string_methods.py`, but you will see that nothing happens.

<details>
  <summary markdown='span'>💡 Why is that? (Click to see the answer.)</summary>

  In the `.py` file, we defined functions, but we never used them.
</details>

<details>
  <summary markdown='span'>💡 How can we then use them?</summary>

  1. In your `.py` file, add a new line after the function definition.
  1. Add some code that uses your function, e.g. `add_comma("John Peter Jude")`.
  1. Make sure that this line is indented all the way to left! Otherwise the Python interpreter will think it's part of your function definition.
  1. Save the file and run:
     ```bash
     python string_methods.py
     ```
  1. Once you're done coding the function and it passes the tests, remove the line you just wrote. Otherwise it will clutter up your test output.
</details>

Have fun!
