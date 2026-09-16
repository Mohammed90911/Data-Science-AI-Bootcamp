In this exercise, we will cover the most useful built-in data structures.
Before diving into the code, take some time to read the following:

- [Lists](https://docs.python.org/3/tutorial/introduction.html#lists), called _array_ in other languages
- [More on lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Tuples](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries), called _hash_ or _hashmap_ in other languages
- [Looping Techniques](https://docs.python.org/3/tutorial/datastructures.html#looping-techniques) with the `for` keyword

All done? Let's code!

## Exercise

### Currencies

Let's build a currency converter in the `currencies.py` file. In this exercise, we will manipulate lists, dictionaries and tuples.

1. Create a new constant dictionary called `RATES` at the top of `currencies.py`. Keys will be 6-letter strings like `"USDEUR"`, `"GBPEUR"`, `"CHFEUR"`, and the values will be their rate stored as a simple Python [`float` number](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex). You can find this information on [Google](https://www.google.com/search?q=USDEUR)
2. Implement the `convert(amount, currency)` function. The first parameter is a **tuple** of two elements: a float and a currency (e.g. `(100, "USD")`). The second parameter is a `String`, the currency you want to convert the amount into.
3. You should _round_ the results to the nearest whole number.
4. When called with an unknown rate (e.g. `"RMBEUR"`), the `convert` function should return `None`.


<br><br>
💡 **Try out your code (before running `make`) by running only the function you just wrote**

One simple way to do this is by calling your function and printing out the result. For example, below are the steps you could take to test the `convert` function in this challenge.

1. **Add the following line to the bottom of your `.py` file:**

    ```python
    # Test converting 100 Euros into US dollars
    print(convert((100, "EUR"), "USD"))
    ```

2. **Run the file in your terminal:**

    ```bash
    python currencies.py
    ```

3. **Check the output in the terminal:**
    - Is anything being printed out?
    - Is it the correct data type?
    - Does the answer printed in your terminal match your expectations?
    - Is there an **error**? Do you understand the error? If you do, debug and try again. If you don't, open a ticket!

This allows you to easily see if your function works and what it does before spending lots of time waiting for more complicated tests to run. Only run your `make` when you know your code works without basic errors!

Remember, coding is an iterative process, so your code will rarely perform as you expect it to the first time. Testing early and often helps you meet basic requirements before testing all possible errors, thus reducing overall debugging time!

Run the tests with:

```bash
make
```

You may notice some tests failing. Update your rates with the following values as results have been hard-coded in the tests:

- `USDEUR`: `0.85`
- `GBPEUR`: `1.13`
- `CHFEUR`: `0.86`
- `EURGBP`: `0.885`
