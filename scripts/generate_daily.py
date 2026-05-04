import os
import datetime
import nbformat as nbf

today = datetime.date.today()
today_str = str(today)
day = today.weekday()

TOPICS = [
    "eda",
    "sql_case_study",
    "data_cleaning",
    "visualization",
    "statistics",
    "feature_engineering",
    "time_series",
]

topic = TOPICS[day % len(TOPICS)]
filename = "notebooks/" + today_str + "_" + topic + ".ipynb"


def cells(topic_key):
    d = today_str
    return {
        "eda": [
            ("md", "# Exploratory Data Analysis\n*Auto-generated – " + d + "*"),
            ("code", """\
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
n = 500
df = pd.DataFrame({
    'age':        np.random.randint(18, 65, n),
    'salary':     np.random.normal(55000, 15000, n).round(2),
    'experience': np.random.randint(0, 40, n),
    'department': np.random.choice(['Engineering','Marketing','Sales','HR','Finance'], n),
    'score':      np.random.uniform(1, 10, n).round(1),
})
print(df.shape)
df.head()"""),
            ("code", "df.describe()"),
            ("code", """\
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df['salary'], bins=30, ax=axes[0], color='steelblue')
axes[0].set_title('Salary Distribution')
sns.boxplot(data=df, x='department', y='salary', ax=axes[1])
axes[1].set_title('Salary by Department')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('notebooks/eda_plot_""" + d + """.png', dpi=80, bbox_inches='tight')
plt.show()"""),
            ("code", "print(df.groupby('department')['salary'].agg(['mean','median','count']).round(2))"),
        ],
        "sql_case_study": [
            ("md", "# SQL Case Study\n*Auto-generated – " + d + "*"),
            ("code", """\
import pandas as pd
import numpy as np

np.random.seed(10)
orders = pd.DataFrame({
    'order_id':    range(1, 201),
    'customer_id': np.random.randint(1, 51, 200),
    'product':     np.random.choice(['Laptop','Phone','Tablet','Monitor','Keyboard'], 200),
    'amount':      np.random.uniform(50, 2000, 200).round(2),
    'date':        pd.date_range('2024-01-01', periods=200, freq='2D'),
})
orders.head()"""),
            ("md", "## Query 1 – Top 10 customers by revenue"),
            ("code", "orders.groupby('customer_id')['amount'].sum().sort_values(ascending=False).head(10)"),
            ("md", "## Query 2 – Monthly revenue trend"),
            ("code", """\
monthly = orders.resample('ME', on='date')['amount'].sum().reset_index()
monthly.columns = ['month', 'revenue']
monthly['month'] = monthly['month'].dt.strftime('%Y-%m')
print(monthly.to_string(index=False))"""),
            ("md", "## Query 3 – Best-selling product"),
            ("code", "orders.groupby('product')['amount'].agg(['sum','count']).sort_values('sum', ascending=False)"),
        ],
        "data_cleaning": [
            ("md", "# Data Cleaning & Preprocessing\n*Auto-generated – " + d + "*"),
            ("code", """\
import pandas as pd
import numpy as np

np.random.seed(7)
n = 300
df = pd.DataFrame({
    'name':   ['User_' + str(i) for i in range(n)],
    'age':    np.where(np.random.rand(n) < 0.1, np.nan,
                       np.random.randint(18, 70, n)).astype(float),
    'email':  ['user' + str(i) + '@example.com' if np.random.rand() > 0.05 else None
               for i in range(n)],
    'salary': np.where(np.random.rand(n) < 0.08, -999,
                       np.random.normal(50000, 12000, n)).round(2),
    'city':   np.random.choice(['Berlin','Munich','Hamburg','Frankfurt', None], n),
})
print('Missing values:')
print(df.isnull().sum())
df.head(10)"""),
            ("code", """\
df['salary'] = df['salary'].replace(-999, np.nan)
df['age'].fillna(df['age'].median(), inplace=True)
df['salary'].fillna(df['salary'].median(), inplace=True)
df.dropna(subset=['email'], inplace=True)
df['city'].fillna('Unknown', inplace=True)
print('After cleaning:')
print(df.isnull().sum())
print('Shape:', df.shape)"""),
            ("code", "df.describe()"),
        ],
        "visualization": [
            ("md", "# Data Visualization\n*Auto-generated – " + d + "*"),
            ("code", """\
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')
np.random.seed(3)
n = 400
df = pd.DataFrame({
    'x':        np.random.randn(n),
    'y':        np.random.randn(n),
    'category': np.random.choice(['A','B','C','D'], n),
    'value':    np.random.exponential(2, n),
})
df.head()"""),
            ("code", """\
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.scatterplot(data=df, x='x', y='y', hue='category', ax=axes[0, 0])
axes[0, 0].set_title('Scatter Plot')
sns.histplot(df['value'], bins=30, ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Distribution')
sns.boxplot(data=df, x='category', y='value', ax=axes[1, 0])
axes[1, 0].set_title('Box Plot by Category')
pivot = df.groupby('category')['value'].mean().reset_index()
sns.barplot(data=pivot, x='category', y='value', ax=axes[1, 1], palette='viridis')
axes[1, 1].set_title('Mean Value by Category')
plt.tight_layout()
plt.savefig('notebooks/viz_plot_""" + d + """.png', dpi=80, bbox_inches='tight')
plt.show()"""),
        ],
        "statistics": [
            ("md", "# Statistical Analysis\n*Auto-generated – " + d + "*"),
            ("code", """\
import numpy as np
from scipy import stats

np.random.seed(99)
group_a = np.random.normal(50, 10, 100)
group_b = np.random.normal(53, 10, 100)
print('Group A  mean={:.2f}  std={:.2f}'.format(group_a.mean(), group_a.std()))
print('Group B  mean={:.2f}  std={:.2f}'.format(group_b.mean(), group_b.std()))"""),
            ("code", """\
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print('T-statistic: {:.4f}'.format(t_stat))
print('P-value:     {:.4f}'.format(p_value))
print('Significant (p<0.05):', p_value < 0.05)"""),
            ("code", """\
n = 200
x = np.random.randn(n)
y = 0.7 * x + np.random.randn(n) * 0.5
r, p = stats.pearsonr(x, y)
print('Pearson r = {:.4f}, p = {:.4f}'.format(r, p))"""),
        ],
        "feature_engineering": [
            ("md", "# Feature Engineering\n*Auto-generated – " + d + "*"),
            ("code", """\
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

np.random.seed(21)
n = 300
df = pd.DataFrame({
    'age':       np.random.randint(18, 65, n),
    'income':    np.random.normal(50000, 20000, n).round(2),
    'purchases': np.random.poisson(5, n),
    'city':      np.random.choice(['Berlin','Munich','Hamburg'], n),
    'churn':     np.random.randint(0, 2, n),
})
df.head()"""),
            ("code", """\
df['income_log']    = np.log1p(df['income'].clip(lower=0))
df['age_group']     = pd.cut(df['age'], bins=[18,30,45,65], labels=['Young','Mid','Senior'])
df['high_value']    = (df['purchases'] > 5).astype(int)
df['city_encoded']  = LabelEncoder().fit_transform(df['city'])
scaler = StandardScaler()
df['income_scaled'] = scaler.fit_transform(df[['income']])
print(df.dtypes)
df.head()"""),
        ],
        "time_series": [
            ("md", "# Time Series Analysis\n*Auto-generated – " + d + "*"),
            ("code", """\
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(5)
dates = pd.date_range('2023-01-01', periods=365, freq='D')
trend = np.linspace(100, 150, 365)
seasonality = 15 * np.sin(2 * np.pi * np.arange(365) / 90)
noise = np.random.normal(0, 5, 365)
ts = pd.Series(trend + seasonality + noise, index=dates, name='value')
print(ts.describe())
ts.head(10)"""),
            ("code", """\
fig, axes = plt.subplots(2, 1, figsize=(12, 6))
ts.plot(ax=axes[0], title='Time Series')
ts.rolling(30).mean().plot(ax=axes[0], label='30-day MA', color='red')
axes[0].legend()
ts.resample('ME').mean().plot(kind='bar', ax=axes[1], title='Monthly Average', color='steelblue')
plt.tight_layout()
plt.savefig('notebooks/ts_plot_""" + d + """.png', dpi=80, bbox_inches='tight')
plt.show()"""),
            ("code", """\
monthly = ts.resample('ME').agg(['mean', 'std', 'min', 'max']).round(2)
print(monthly)"""),
        ],
    }[topic_key]


def make_notebook(topic_key):
    nb = nbf.v4.new_notebook()
    nb.cells = []
    for cell_type, source in cells(topic_key):
        if cell_type == "md":
            nb.cells.append(nbf.v4.new_markdown_cell(source))
        else:
            nb.cells.append(nbf.v4.new_code_cell(source))
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


os.makedirs("notebooks", exist_ok=True)
nb = make_notebook(topic)
with open(filename, "w") as f:
    nbf.write(nb, f)

print("Created:", filename)
