import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("books_dataset.csv")

print("Original data:")
print(df.head())

# -----------------------------------------
# Convert Price column to numeric
# -----------------------------------------

df["Price"] = (
    df["Price"]
    .astype(str)
    .str.extract(r"([0-9]+(?:\.[0-9]+)?)")[0]
)

df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Remove rows where price could not be converted
df = df.dropna(subset=["Price"])

print("\nCleaned Price values:")
print(df["Price"].head())

print("\nNumber of valid prices:", len(df))
print("Minimum price:", df["Price"].min())
print("Maximum price:", df["Price"].max())
print("Average price:", round(df["Price"].mean(), 2))

# -----------------------------------------
# Graph 1: Distribution of Book Prices
# -----------------------------------------

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="Price",
    bins=20,
    kde=True
)

plt.title("Distribution of Book Prices")
plt.xlabel("Price")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.show()

# -----------------------------------------
# Graph 2: Book Price Boxplot
# -----------------------------------------

plt.figure(figsize=(10, 5))

sns.boxplot(
    x=df["Price"]
)

plt.title("Book Price Boxplot")
plt.xlabel("Price")
plt.tight_layout()
plt.show()

# -----------------------------------------
# Graph 3: Rating Distribution
# -----------------------------------------

if "Rating" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x="Rating"
    )

    plt.title("Book Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.show()

print("\nEDA graphs generated successfully!")