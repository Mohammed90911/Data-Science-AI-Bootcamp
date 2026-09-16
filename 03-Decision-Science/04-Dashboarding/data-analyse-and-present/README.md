# Analyze and Present

## 🎯 Objectives

You know the Olist data through and through by now.

It's time to analyze the data for your management, and present your results!

For this challenge, **focus on creating two, three good visuals in a notebook**. Once you have those, you can either present them by showing your notebook, or by copy-pasting the charts into a presentation tool of your choice.

If you want to and have enough time, you can also create a basic dashboard using Dash in the next challenge. That said, remember the focus of the challenge is to create an insightful chart first. Making a dashboard is a nice extra, but optional.

🏁 Stop your analyses 2 hours before presentation time so you have time to create your presentation (or dashboard). Once you have a basic presentation (or your dashboard running), you can still go back to add more visuals!

Remember to work together with your buddy and split the work.

## ⚙️ Setup

🚀 For this challenge you can use both:
- The `Order`, `Seller`, `Product` and `Review` classes from the `olist` module
- The original tables available in `Olist().get_data()`

In the previous units, we built the first classes for our Linear and Logistic Regression models. They are feature tables, but might not have all data you'd want to use in a dashboard. For example, to visualize evolutions over time, you'd have to go back to the original tables to find the purchase date, delivery date, ...

⚠️ Make sure you have the latest versions of `seller.py` and `product.py` in your `olist` module. To do so:

1. Go back to the Logistic Regression unit, and download the Recap solution.
1. Unzip the file, and inside you will find the `seller_updated.py` and `product_updated.py` files. Open those files in VS Code.
1. In your terminal navigate to the `olist` folder, and open it using VS Code:
   ```bash
   cd ~/code/<user.github_nickname>/03-Decision-Science/olist
   code .
   ```
1. Copy-paste the contents of:
   - The solution's `seller_updated.py` into your `olist/seller.py` and `olist/seller_updated.py` files.
   - The solution's `product_updated.py` into your `olist/product.py` and `olist/product_updated.py` files.

## 👥 Choose a target audience

Team up with your buddy and decide:

> Who will you present to? The CEO? CFO? Head of Marketing? Sales? Investors?

Pick an audience, and think about what you want to present. If you're in doubt, scroll down to the _Need inspiration?_ section..

## 📊 Analyse the data

Open the `analysis.ipynb` notebook to get started with your analysis.

We already provided the code to import the different Olist classes from the previous units to prepare the data. Those are a good place to get started. If you need additional information you can also go back to the original `Olist().get_data()`. You'll need those if you want to plot evolutions over time. Don't make it too complicated though: today is all about presenting analysis through visualizations. So resist the urge to create even more classes. 🤓

### Need help getting the data?

Besides the different classes we made in the previous unit (`Order`, `Seller`, `Product`, `Review`), we also give you some other functions you can use.

Head over to the `bi_data.py` in this challenge folder. It contains a couple of functions to create ready-made tables for BI (Business Intelligence). Check the module docstring to see what are the main functions, and the function docstrings to see how they work.

You can use these functions to create the data for your analysis. Have a look at the code, and make sure you understand what it's doing!

Don't hesitate to change the file to adapt the functions' behaviour to your needs, or to add new functions.

### Creating your first visualizations

Now it's time to choose 📊 the right visualization 📈 for the point you want to bring across.

In a notebook, build a couple of visualizations **using Plotly** - split the work with your buddy! Remember to keep your notebook nice and tidy! It should be runnable from top to bottom at all times...

Make sure to create your visuals using **Plotly**! That will allow you to easily transfer them to a Plotly Dash dashboard in a second phase.

Once you have two or three visualizations, move on to the next part! You can come back to this point once you have a first version of your dashboard running.

Don't forget to **regularly commit and push** the work you made!

### Need inspiration?

Here are a couple of ideas you could implement. Don't try to do all of them today, that's impossible. Just pick a few you're interested in.

> **Legend:**<br>
>
> 🔎 Have a look at this source to find the code that generates a table that is (as good as) ready to plot.<br>
>
> 🛠️ Most of the work has been done, but you'll need to make a couple of modications to get it working.<br>
>
> 🤯 This will keep you busy for a while...

- Analyse **sales** across different dimensions:
  - Evolution over time (🔎 `bi_data.py`)
  - By seller (🔎 `olist.seller`)
  - By product category (🔎 `olist.product`)
  - By geography (customer / seller) (🔎 `bi_data.py`)
- Analyse **customer satisfaction** (NPS = Net Promoter Score = % promoters - % detractors, or CSAT = Customer Satisfaction = Average review score):
  - Correlation with other variables (price, delivery time, wait time) (🔎 `olist.order`)
  - By seller (location) (🔎 `olist.seller`)
  - By product (category) (🔎 `olist.product`)
  - By customer (location)  (🛠️ `olist.order` joined with `Olist().get_data()['customers']`)
  - Evolution over time (🛠️ `olist.order` joined with `bi_data.orders_cleaned()`)
- Analyse Olist's **profitability** (see the next point for details):
  - Evolution over time of fee on sales (🛠️ `bi_data`: adapt `sales_by_period()`)
  - Distribution across sellers (🛠️ start from `olist.seller`)
  - Distribution across product categories  (🛠️ start from `olist.product`)
  - By customer and/or seller location (🛠️ `bi_data`: adapt `sales_by_..._state()`)
- Analyse how estimated **reputation costs** impact profitability: which sellers or products have the worst impact? (🤯 adapt `olist.seller` or `olist.product`)

Don't hesitate to go back into some of the challenges of the previous units and dive into their **solutions** for inspiration. For example in:
- CEO Request
- Metric Design
- NPS Recap in Statistical Inference
- Delivery Time Recap in Linear Regression

Expand the section below **if (and only if)** you want to dive into profitability (and have the time for it.) You can also first head over the next challenge on dashboarding, and then come back here.

<details>
  <summary markdown='span'><strong>Expand</strong> to dive into Olist's profitability.</summary>

### [Optional] Olist's profitability?

#### Revenues

- **Sales fees:** Olist takes a **10% cut** on the product price (excl. freight) of each order delivered
- **Subscription fees:** Olist charges **80 BRL by month** per seller

#### Costs
- _Estimated_ **reputation costs** of orders with bad reviews (<= 3 stars)

  💡 In the long term, bad customer experience has business implications: low repeat rate, immediate customer support cost, refunds or unfavorable word of mouth communication. We make an assumption about the monetary cost for each bad review:
  ```python
  # review_score:   cost (BRL)
  {
    '1 star':        100,
    '2 stars':        50,
    '3 stars':        40,
    '4 stars':         0,
    '5 stars':         0,
  }
  ```

</details>

## 🎥 Show time! Present your analysis

You have 5 minutes per buddy pair (Q&A included) to present your results.

The TAs will play the role of the CEO, CFO, Marketing Director, investor, ...

You can present:
- Straight from your **notebook**.
- Use your favourite **presentation app** and copy paste your relevant charts in there.
- Make a dashboard using **Plotly Dash** (head over to the next challenge for that).

🏁 Stop your analyses 2 hours before presentation time so you have time to create your presentation (or dashboard). Once you have a basic presentation (or your dashboard running), you can still go back to add more visuals!

## Wrapping it up

There are no tests for this challenge, but do not forget to commit and push your code!
