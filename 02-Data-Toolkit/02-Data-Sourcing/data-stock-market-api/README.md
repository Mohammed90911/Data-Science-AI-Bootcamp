# Stock Market API

In this exercise, we are going to play around with the stock market API [Massive](https://massive.com/).

🎯 The goal here is:
- to get comfortable reading API documentation,
- to extract information from an API, and
- load it into a dataframe to manipulate and visualise the data easily.

## Intro

A common way of collecting data is through APIs. Those can be [public APIs](https://github.com/public-apis/public-apis) with authentication or not, free or paid, internal APIs at your company, etc.

When it comes to APIs, there are two **data formats** that will be sent back to you when performing an API call:

- [XML](https://en.wikipedia.org/wiki/XML) (long-established)
- [JSON](https://en.wikipedia.org/wiki/JSON) (currently very widespread)

ℹ️ Most modern APIs are send back JSON. In this challenge, we are going to use such an API.

## Reading the documentation

When presented with a new API to use, your first reflex should be to go straight to the documentation, and figure out the following:

1. Does it serve JSON?
1. Does this API require authentication? (Do I need to sign up to get an API key? Do I need to pay?)
1. What is the base URI?
1. Which endpoints can I call? What data does it return?

👯‍♂️ Buddy time! 👉  Let's find the API documentation page of **massive.com**. Read the documentation, and try answering those questions. When you are comfortable with what this API is about, you can start working on the challenge.

<details><summary markdown='span'>Solution to find the documentation
</summary>
Documentation pages are often hidden in the footer or in some menu.
<br>
Typing <i>'the_website_name API documentation'</i> in the google search bar is a quick way to find it too.
<br>
<strong>Solution</strong>: <a href="https://massive.com/docs">https://massive.com/docs</a>
</details>

## Apple stock the last 90 days

### API setup

The endpoints of the API that we want to use are protected **behind a paywall**.

Fortunately, we can get a lot of the API functionality for free. You just have to register on the website, and you will receive **5 API calls per minute for free**. That should be enough for us.

👉 **Create an account** now. After going through the easy process, you can click in the top right corner of the website on `Dashboard` to find your personal API key.

Whenever you make an API call, you will have to provide this API key in your request as a key-value pair.

For example, to get a certain day's stock prices:
```
https://api.massive.com/v1/open-close/AAPL/2025-02-03?adjusted=true&apiKey=YOUR_API_KEY
```

### Using the API

👉 Now let's find in the Massive API documentation the **URL** for historical Apple stock prices.

When you find the URL, copy and paste it in a new tab and look at the data you get from the API.

> If you are on Chrome, you should install the [JSONView](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc) extension for a neater look. In the end, JSON is just text that needs to be **parsed**, that's what the extension will do.

It should be a JSON looking like this:
<details><summary markdown='span'>Show example
</summary>

```js
{
  "ticker": "AAPL",
  "queryCount": 24,
  "resultsCount": 24,
  "adjusted": true,
  "results": [
    {
      "v": 7.0790813e+07,
      "vw": 131.6292,
      "o": 130.465,
      "c": 130.15,
      "h": 133.41,
      "l": 129.89,
      "t": 1673240400000,
      "n": 645365
    },
    {
      "v": 6.3896155e+07,
      "vw": 129.822,
      "o": 130.26,
      "c": 130.73,
      "h": 131.2636,
      "l": 128.12,
      "t": 1673326800000,
      "n": 554940
    },
    {
      "v": 6.9458949e+07,
      "vw": 132.3081,
      "o": 131.25,
      "c": 133.49,
      "h": 133.51,
      "l": 130.46,
      "t": 1673413200000,
      "n": 561278
    },
    {
      "v": 7.1379648e+07,
      "vw": 133.171,
      "o": 133.88,
      "c": 133.41,
      "h": 134.26,
      "l": 131.44,
      "t": 1673499600000,
      "n": 635331
    },
    // [...]
  ],
  "status": "OK",
  "request_id": "edd1a3b1104cde7bba8fbe0ccaa645df",
  "count": 24
}
```


</details>

❗️ Take your time before reading the solution, finding what we want in an API documentation can usually take **10 to 15 minutes of reading**.

<details><summary markdown='span'>Solution
</summary>
You can find the information here in the documentation:
<a href="https://massive.com/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to">https://massive.com/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to</a>
<br>
The URL is:
<pre>
https://api.massive.com/v2/aggs/ticker/AAPL/range/1/day/2025-01-02/2025-02-03?adjusted=true&sort=asc&apiKey=YOUR_API_KEY
</pre>
</details>

👉 Read the API documentation to understand:
- the request format (the various parts of the url), and
- what the keys in the response stand for.

🔍 What would you need to change to get the last 90 days' prices?

### Making test calls to the API

Before building something fancy, we need to first make sure that we can run an API call successfully. This is a sanity check to make sure we don't start coding too much before realizing that the API we intended to use is not a good fit. And to make sure that we understood all the parameters correctly.

So how can we make our first call? Using the browser...

The browser _is_ an HTTP client! If there is no complex request `Header` to set and the verb to use is `GET`, then it's just as easy as typing the URL in the address bar.

## Using API data in Pandas

### Setup

For this exercise we will work in a Notebook.

```sh
jupyter notebook
```

👉 Go ahead and **create** a new Jupyter Notebook named `stocks.ipynb` in the `~/code/<user.github_nickname>/{{local_path_to("02-Data-Toolkit/02-Data-Sourcing/01-Stock-Market-API")}}` folder.

👉 Start with the usual imports in the first cell:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
```

We will reuse the **API URL** for the **historical Apple stock prices** here.<br>
To make a **call** to the API you can use the following code:

```python
import requests

url = "YOUR_API_URL"    # Replace by the URL you found before
api_data = requests.get(url).json()
```

👉 Why are we chaining a `.json()` after `.get()`? Does it still work without that call? You can `print()` intermediate steps to convince yourself. (💡 [Doc](https://requests.readthedocs.io/en/master/user/quickstart/#json-response-content))

👉 Change the API request URL so that you get the Apple stock prices for the past 90 days. Your end date needs to be yesterday's date, otherwise it won't work. (For now you can hard-code the from and to dates. We'll change that in the optional part.)

If the code breaks while you're playing with the parameters, try commenting out the `.json()` part and inspect the result of the `.get()` requests by `print()`ing it out.

### Convert the request data into a DataFrame

👉 You can now **create a dataframe** `apple_df` from this data. Investigate the format of the JSON in your browser to see which data you need to extract.

<details><summary markdown='span'>Solution
</summary>
<code>apple_df = pd.DataFrame(api_data['results'])</code>
</details>

With this dataframe we can **plot** the evolution of the stock price.
But before doing that, we need to do a couple of things:
- Convert the column containing the timestamp into a datetime object and save it in a `date` column.
- Set the `date` column as the index
- Rename the columns to something more userfriendly than `c`, `o`, `h`, `l`, ...

### Converting the date to a datetime object

👉 First check the API documentation to:
- Find out which column in your dataframe represents the time?
- The time seems to be represented by a number. What does this number represent?

<details><summary markdown='span'>Solution
</summary>
The time is in the column <code>t</code> in our dataframe.

The number is a so-called **Unix time** in milliseconds. This is a very common format in programming. It is the number of milliseconds since 1-1-1970. You will also encounter the same but in number of seconds.
</details>


👉 To convert this into a date, you can use `Pandas.to_datetime()`:

- **pd.to_datetime()** documentation: [http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime](http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime)
- Which argument do you need to convert from Unix time?
- How do you tell Pandas that it is the number of milliseconds?

<details><summary markdown='span'>Solution
</summary>
<code>apple_df['date'] = pd.to_datetime(apple_df['t'], origin='unix', unit='ms')</code>
</details>

### Set the date column as the index

👉 To do this you can use the DataFrame method **set_index**

- documentation: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html)


<details><summary markdown='span'>Solution
</summary>
<code>apple_df = apple_df.set_index('date')</code>
</details>


### Rename the columns

Which DataFrame method would you need to rename the columns? Hint: don't search too far...

<details><summary markdown='span'>Solution
</summary>
<strong>pd.DataFrame.rename()</strong> documentation: <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html">https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html</a>
</details>

💡 The safest way to rename columns is to use a dictionary with the old column names as the keys and the new column names as the values.

👉 Rename the columns like this:
```
  'o': 'open'
  'c': 'close'
  'h': 'high'
  'l': 'low'
```

<details><summary markdown='span'>Solution
</summary>
```python
mapping = {
    'o': 'open',
    'c': 'close',
    'h': 'high',
    'l': 'low',
    'n': 'number',
    'v': 'volume',
    'vw': 'avg_price'
}
apple_df = apple_df.rename(columns=mapping)
```
</details>


### Now we can plot 🎉

👉 First let's plot only the values in the **`close`** column

<details><summary markdown='span'>Solution
</summary>
<code>apple_df['close'].plot()</code>
</details>

Now we can make a plot with the values in the **`open`, `close`, `high`, and `low`** columns

<details><summary markdown='span'>Solution
</summary>
<code>apple_df[['open', 'close', 'high', 'low']].plot()</code>
</details>

💡 Our plot is really hard to read. We can improve its readability with the `figsize` argument of the `plot()` method.
- documentation: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html)

<details><summary markdown='span'>Solution
</summary>
<code>apple_df[['open', 'close', 'high', 'low']].plot(figsize=(12,4))</code>
</details>

### Test your code!

Add the following cell to your notebook and run it:

```python
from nbresult import ChallengeResult

result = ChallengeResult('apple',
    index_name=apple_df.index.name,
    index_type=apple_df.index.dtype,
    columns=apple_df.columns
)
result.write()
print(result.check())
```

You can `commit` and `push` your code :rocket:


## Back to the API

Let's find out what other kinds of data we can get from this API 🕵️‍♂️

### What is the URL to find:

1. Amazon's historical stock prices?
2. Meta's (Facebook) market cap?
3. Apple's quarterly gross revenues for the last 4 quarters?
4. The most recent news item about Tesla?

Hint: Sometimes you will need a URL that will give you a larger response, containing the data we are actually looking for.

<details><summary markdown='span'>All Solutions
</summary>
<ol>
    <li><code>https://api.massive.com/v2/aggs/ticker/AMZN/range/1/day/2025-01-02/2025-02-03?apiKey=YOUR_API_KEY</code></li>
    <li><code>https://api.massive.com/v3/reference/tickers/META?apiKey=YOUR_API_KEY</code></li>
    <li><code>https://api.massive.com/vX/reference/financials?ticker=AAPL&timeframe=quarterly&limit=4&apiKey=YOUR_API_KEY</code></li>
    <li><code>https://api.massive.com/v2/reference/news?ticker=TSLA&limit=1&apiKey=YOUR_API_KEY</code></li>
</ol>
</details>

❗️  Don't forget to **push your code to GitHub**

## (Optional) Plotting  _multiple_  line charts

We'd like to **compare** the evolution of the GAFA stocks (Google, Apple, Meta, Amazon) by plotting them on the _same_ chart.

👉 Reuse the code from above to build a dataframe with one column per stock and keeping the dates as the index.

💡 To make your life easier, first refactor your code into a `create_stock_df_of_company(company_code)` function to get the information for one company.

Then use it for all companies, concatenate all the data, and pivot.

💡 Maybe you can use some normalization technique at `t = 0` to better compare the relative performance of each stock!

## (Optional) Make the dates flexible

So far we have hard coded the start and end date of our data.

👉 Refactor your `create_stock_df_of_company(company_code)` to always take the last 90 days of data.
