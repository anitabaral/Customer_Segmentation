# Customer segmentation using RFM analysis

Recency, Frequency, and Monetary customer segmentation model, that aids to personalized marketing, 
increased engagement and relevant offers to the right group of customers.

### ☤ Features
----------
- Segments customers on the basis of geography and behavior.
- Customers segmented geographically are further segmented using RFM analysis.
- RFM segmentation provides 7 segments of customers, **Champions**, **Loyalists**, **Potential Loyalists**, **Promising**,
**Can't loose**, **At risk**, **Lost customers**
- Count and average frequency, monetary and recency of each segment is presented.
- Provides list of all or top 10 customers belonging to a certain segment.

### ⏳ Installation and use
- **Operating system**: macOS / OS X · Linux · Windows
- **Python version**: Python 3.9 
- **Package managers**: [pip] [pipenv]

#### pipenv
Before you install dependencies, make sure that
your `pip`is up to date.
- Installing pipenv
```bash
pip install --user pipenv
```
#### Getting the dataset: (https://archive.ics.uci.edu/ml/datasets/online+retail)

#### Quickstart
```bash
git clone https://github.com/anitabaral/Major_Project/new/dev
cd Major_Project

pipenv shell
pipenv run pip freeze > requirements.txt
pipenv install -r requirements.txt

streamlit run app.py

```
### ⭐️ Working architecture of the project
![working model](https://user-images.githubusercontent.com/29528102/131431236-55d99443-1eeb-44e8-9860-c06175cf0d79.jpg)


