import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    print("Loading Titanic dataset...")
    df = sns.load_dataset('titanic')
    
    print("\n--- Dtypes ---")
    print(df.dtypes)
    
    print("\n--- Missingness ---")
    print(df.isnull().sum())
    
    print("\n--- Descriptive Stats ---")
    print(df.describe())

    # Age buckets
    df['age_bucket'] = pd.cut(df['age'], bins=[0, 12, 18, 35, 60, 100], labels=['Child (0-12)', 'Teen (13-18)', 'Young Adult (19-35)', 'Adult (36-60)', 'Senior (60+)'])

    print("\n--- Survival by Sex ---")
    print(df.groupby('sex')['survived'].mean())

    print("\n--- Survival by Class ---")
    print(df.groupby('class')['survived'].mean())

    print("\n--- Survival by Age Bucket ---")
    print(df.groupby('age_bucket', observed=True)['survived'].mean())

    sns.set_theme(style="whitegrid")

    # 1. Bar chart: Survival by Sex and Class
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x='class', y='survived', hue='sex', errorbar=None)
    plt.title('Survival Rate by Sex and Class')
    plt.ylabel('Survival Rate')
    plt.savefig('survival_by_sex_class.png')
    plt.close()

    # 2. Bar chart: Survival by Age Bucket
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x='age_bucket', y='survived', hue='sex', errorbar=None)
    plt.title('Survival Rate by Age Bucket (by Sex)')
    plt.ylabel('Survival Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('survival_by_age_bucket.png')
    plt.close()

    # 3. Violin Plot: Age Distribution by Survival and Sex
    plt.figure(figsize=(8, 5))
    sns.violinplot(data=df, x='survived', y='age', hue='sex', split=True)
    plt.title('Age Distribution by Survival and Sex')
    plt.xticks([0, 1], ['Did Not Survive', 'Survived'])
    plt.savefig('age_survival_violin.png')
    plt.close()

    # 4. Boxplot: Age Distribution by Class and Survival
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='class', y='age', hue='survived')
    plt.title('Age Distribution by Class and Survival')
    plt.savefig('age_class_survival_boxplot.png')
    plt.close()
    
    print("\nAll visualizations saved successfully.")

if __name__ == '__main__':
    main()
