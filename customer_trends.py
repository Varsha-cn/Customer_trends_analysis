# %%
import pandas as pd
from sqlalchemy import create_engine

# %%
df = pd.read_csv(r"C:\Users\Admin\Downloads\Customer_trends_analysis\customer_shopping_behavior.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.describe(include='all'))
print(df.isnull().sum())

# %%
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

# %%
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

# %%
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
print(df.columns) 

# %%
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
print(df[['age', 'age_group']].head(10))

# %%
# create new column purchase_frequency_days

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
# %%
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases', 'purchase_frequency_days']].head(10))

# %%
print(df[['discount_applied','promo_code_used']].head(10))
print((df['discount_applied'] == df['promo_code_used']).all())

# %%
df = df.drop('promo_code_used', axis=1)
print(df.columns)

# %%
#db connection
username = "root"
password = "Varsha_29"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
print(pd.read_sql("SELECT * FROM customer LIMIT 5;", engine))

