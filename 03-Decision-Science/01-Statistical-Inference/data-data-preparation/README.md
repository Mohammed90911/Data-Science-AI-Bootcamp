## Data Preparation

In this exercise, you will perform an **Exploratory Data Analysis** (EDA).

### Data Schema

✏️ Before you start, make sure you understand Olist's data schema.

High level view:

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/lectures/olist_data_schema.png' width='800'>

Detailed ERD (Entity Relationship Diagram) with all tables, columns, and relationships:

<img src="https://wagon-public-datasets.s3.amazonaws.com/04-Decision-Science/01-Project-Setup/olist_schema_v2.png" width=1000>

We have also written a detailed description of the data schema for you in the previous challenge's `data` folder.

Use the command below to open this `README`:
```bash
code -a ~/code/<user.github_nickname>/{{ local_path_to("03-Decision-Science/01-Statistical-Inference/01-Context-and-Setup") }}/data/README.md
```

Right-click on the tab and choose "Open Preview" to see the Markdown format nicely rendered.

### Data Loader

We'll load the csv data in a Python class and pandas DataFrame, which will come in handy throughout the week.

✏️ Open `data_preparation.ipynb` and follow the instructions.
