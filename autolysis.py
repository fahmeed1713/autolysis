import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
import numpy as np
import argparse

def get_token():
    """
    Retrieves the token from the environment variable.
    Returns:
        str: Token value or None if not set.
    """
    return os.getenv("AIPROXY_TOKEN")

def load_dataset(filepath):
    """
    Load a dataset and provide basic statistics and missing value summary.
    Args:
        filepath (str): Path to the CSV file.
    Returns:
        tuple: DataFrame, summary statistics, and missing values summary.
    """
    df = pd.read_csv(filepath, encoding='ISO-8859-1')
    summary_stats = df.describe(include='all').transpose()
    missing_values = df.isnull().sum()
    return df, summary_stats, missing_values

def generate_correlation_heatmap(df, output_path):
    """
    Generate and save a heatmap of the correlation matrix for numeric data.
    Args:
        df (DataFrame): Input data.
        output_path (str): Path to save the heatmap image.
    """
    numeric_data = df.select_dtypes(include=[np.number])
    if numeric_data.empty:
        print("No numeric columns found for correlation matrix.")
        return
    correlation_matrix = numeric_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Correlation heatmap saved to {output_path}")

def generate_missing_values_plot(df, output_path):
    """
    Generate and save a bar plot of missing values for columns with missing data.
    Args:
        df (DataFrame): Input data.
        output_path (str): Path to save the bar plot image.
    """
    missing_counts = df.isnull().sum()
    missing_counts = missing_counts[missing_counts > 0]
    if missing_counts.empty:
        print("No missing values to visualize.")
        return
    plt.figure(figsize=(12, 6))
    sns.barplot(x=missing_counts.index, y=missing_counts.values, palette="viridis")
    plt.xticks(rotation=45)
    plt.xlabel("Columns")
    plt.ylabel("Missing Value Count")
    plt.title("Missing Values by Column")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Missing values bar plot saved to {output_path}")

def find_outliers(df):
    """
    Identify columns with outliers using Z-score analysis.
    Args:
        df (DataFrame): Input data.
    Returns:
        Series: Count of outliers for each numeric column.
    """
    numeric_data = df.select_dtypes(include=[np.number])
    if numeric_data.empty:
        print("No numeric columns available for outlier detection.")
        return pd.Series(dtype='int')
    z_scores = numeric_data.apply(zscore)
    outliers = (z_scores.abs() > 3).sum()
    return outliers

def create_analysis_report(df, summary, missing, heatmap_path, missing_plot_path, dataset_name):
    """
    Compile a markdown report summarizing the dataset analysis.
    Args:
        df (DataFrame): Loaded data.
        summary (DataFrame): Summary statistics.
        missing (Series): Missing values summary.
        heatmap_path (str): Path to the correlation heatmap.
        missing_plot_path (str): Path to the missing values plot.
        dataset_name (str): Name of the dataset.
    Returns:
        str: Compiled markdown report.
    """
    report = f"# Analysis Report: {dataset_name}\n\n"
    report += f"## Overview\nDataset contains {df.shape[0]} rows and {df.shape[1]} columns.\n\n"
    report += "### Columns:\n"
    for col in df.columns:
        report += f"- **{col}**: {df[col].dtype}\n"
    report += "\n## Summary Statistics\n"
    report += summary.to_markdown() + "\n\n"
    report += "## Missing Values\n"
    report += missing.to_markdown() + "\n\n"
    if heatmap_path:
        report += "## Correlation Heatmap\n"
        report += f"![Correlation Heatmap]({heatmap_path})\n\n"
    if missing_plot_path:
        report += "## Missing Values Plot\n"
        report += f"![Missing Values Bar Plot]({missing_plot_path})\n\n"
    outliers = find_outliers(df)
    if not outliers.empty:
        report += "## Outliers\n"
        report += "Detected outliers (Z-score > 3):\n"
        report += outliers.to_markdown() + "\n\n"
    return report

def main_analysis(filepath):
    """
    Run the analysis pipeline on the given dataset.
    Args:
        filepath (str): Path to the dataset file.
    """
    dataset_name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = dataset_name
    os.makedirs(output_dir, exist_ok=True)
    df, summary, missing = load_dataset(filepath)
    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    missing_plot_path = os.path.join(output_dir, "missing_values_plot.png")
    generate_correlation_heatmap(df, heatmap_path)
    generate_missing_values_plot(df, missing_plot_path)
    report = create_analysis_report(df, summary, missing, heatmap_path, missing_plot_path, dataset_name)
    report_path = os.path.join(output_dir, "README.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Analysis complete. Report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform analysis on a dataset.")
    parser.add_argument("filepath", type=str, help="Path to the CSV file.")
    args = parser.parse_args()
    main_analysis(args.filepath)
