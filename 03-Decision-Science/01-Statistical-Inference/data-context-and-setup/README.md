## Objectives of the module

We will analyze a dataset provided by an e-commerce marketplace called **Olist** to answer the CEO's question:

> How could Olist increase its profit?

## About Olist 🇧🇷

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/best-practices/olist.png" width="500"/>

Olist is a leading e-commerce service that connects merchants to main marketplaces in Brazil. They provide a wide range of offers including inventory management, dealing with reviews and customer contacts to logistic services.

Olist charges sellers a monthly fee. This fee is progressive with the volume of orders.

Here are the seller and customer workflows:

**Seller:**

- Seller joins Olist
- Seller uploads products catalogue
- Seller gets notified when a product is sold
- Seller hands over an item to the logistic carrier

👉 Note that multiple sellers can be involved in one customer order!

**Customer:**

- Browses products on the marketplace
- Purchases products from Olist.store
- Gets an expected date for delivery
- Receives the order
- Leaves a review about the order

👉 A review can be left as soon as the order is sent, meaning that a customer can leave a review for an order he did not receive yet!

## Dataset

The dataset consists of ~100k orders from 2016 and 2018 that were made on the Olist store, available as CSV files on Le Wagon S3 bucket (❗️the datasets available on Kaggle may be slightly different).

💾 Let's store our `data` folder *outside* of this challenge folder so that it can be accessed by all other challenges throughout the whole Decision Science module. We don't want it to be tracked by `git` anyway!

``` bash
# Create the data folder
mkdir -p ~/.lewagon/olist/data/csv
```

✅ Download the 9 datasets compressed in the `olist.zip` file, unzip it and store them in your `~/.lewagon/olist/data/csv` folder:

```bash
curl https://wagon-public-datasets.s3.amazonaws.com/olist/olist.zip > ~/.lewagon/olist/data/olist.zip
unzip -d ~/.lewagon/olist/data/csv/ ~/.lewagon/olist/data/olist.zip
```

Check you have the 9 datasets on your machine:

```bash
ls ~/.lewagon/olist/data/csv
```

## Setup

### 1 - Project Structure

Let's create a folder for our `olist` package. We'll refactor all our data-processing logic into `.py` files inside the `olist` package.

We'll create that `olist` folder in the main folder for this module: `~/code/<user.github_nickname>/03-Decision-Science`. Let's `cd` into that folder:

```bash
cd ~/code/<user.github_nickname>/03-Decision-Science
```

We already have some "boilerplate" code for you in this challenge. Let's move it into our target `olist` folder:

```bash
mv ~/code/<user.github_nickname>/{{ local_path_to("03-Decision-Science/01-Statistical-Inference/01-Context-and-Setup") }}/olist .
```

This will be your project structure for the module:

```bash
.
├── 01-Statistical-Inference    # Your notebooks & analyses, unit-by-unit,
│   ├── data-context-and-setup  # challenge-by-challenge
│   ├── data-data-preparation
│   └── data-exploratory-analysis
├── 02-Linear-Regression
│   └── ...
├── 03-Logistic-Regression
│   └── ...
├── 04-Dashboarding
│   └── ...
└── olist                       # your data-processing logic
    ├── README.md               # documentation for our package
    ├── __init__.py             # turns the olist folder into a "package"
    ├── data.py
    ├── order.py
    ├── product.py
    ├── review.py
    ├── seller.py
    └── utils.py
```

Check your current setup by running this:

```bash
tree
```

Your tree structure should look like this at this stage:

```bash
.
├── 01-Statistical-Inference
│   └── data-context-and-setup
│       └── ... [several files and folders in here]
└── olist
    ├── README.md
    ├── __init__.py
    ├── data.py
    ├── order.py
    ├── product.py
    ├── review.py
    ├── seller.py
    └── utils.py
```

All individual challenge folders will be automatically tracked by `git`. That magic happens when you create the challenge with the instructions from Kitt. Our `olist` folder is outside the individual challenge folders and we have to set up the `git` tracking ourselves.

Move into the `olist` folder:
```bash
cd olist
```

Initiate the `git` tracking:

```bash
git init
```

Your folder is now tracked by `git` locally.

Stage the files we just created:
```bash
git add .
git status  # Good practice to check your status when you did a `git add .`
```

If your status looks like you expected, you can commit:
```bash
git commit -m "initial setup"
```

So far, we only worked locally. Time to push our code to GitHub. To do that we need a repo on GitHub and connect our local repo to it. Fortunately, the `gh` tool provides a convenient way to do that:

```bash
gh repo create data-olist --private --push --source=.
```

Let's check if the repo was correctly created. This command should open the repo on GitHub in your browser:

```bash
gh browse
```

Throughout this module we'll be making changes to the code inside `olist`. Remember to commit your changes in this folder!

### 2 - Edit the `PYTHONPATH`

Add `olist` path to your `PYTHONPATH`.

This will allow you to easily import modules defined in `olist` in your notebooks throughout the week.

Open your terminal and navigate to your home directory by running:

```bash
cd
```

Now you'll need to open your `.zshrc` file. As you might have noticed the file starts with a dot which means it's a hidden file. To be able to see this file in your terminal you'll need to run the command below, the flag `-a` will allow you to see hidden files. You'll see multiple files starting with a `.`. They are mostly configuration files.

```bash
ls -a
```

Next let's open the file using your text editor:

```bash
code .zshrc
```

Now in your terminal run:
```bash
cd ~/code/<user.github_nickname>/03-Decision-Science
echo "export PYTHONPATH=\"$(pwd):\$PYTHONPATH\""
```

👉 Copy the resulting output line from your terminal and paste it at the bottom of your `~/.zshrc` file. Don't forget to save the file and then restart all your terminal windows to take this change into account.


### 🔥 Check your setup

Go to your **challenge folder** and run an `ipython` session:

```bash
cd ~/code/<user.github_nickname>/{{ local_path_to("03-Decision-Science/01-Statistical-Inference/01-Context-and-Setup") }}
ipython
```

Then type the following to check that the setup phase from the previous exercise worked:

```python
from olist.data import Olist
Olist().ping()
# => pong
```

If you get something else than `pong`, raise a ticket to get help from a TA. You might have a problem with the `$PYTHONPATH`.

## Push your code on GitHub

From your `{{ local_path_to("03-Decision-Science/01-Statistical-Inference/01-Context-and-Setup") }}` directory, commit and push your code:

```bash
cd ~/code/<user.github_nickname>/{{ local_path_to("03-Decision-Science/01-Statistical-Inference/01-Context-and-Setup") }}
git add .
git commit -m 'kick off olist challenge'
git push origin master
```

Congratulations! You're all setup for `olist` 🚀
