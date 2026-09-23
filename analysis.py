import pandas as pd


class DataAnalysisEngine:

    # ======================================================
    # Numeric Summary
    # ======================================================

    def numeric_summary(self, df):

        if df is None or df.empty:
            return pd.DataFrame()

        numeric = df.select_dtypes(include="number")

        if numeric.empty:
            return pd.DataFrame()

        summary = pd.DataFrame({
            "Column": numeric.columns,
            "Minimum": numeric.min().values,
            "Maximum": numeric.max().values,
            "Median": numeric.median().values,
            "Standard Deviation": numeric.std().values
        })

        return summary.round(2)


    # ======================================================
    # Group Analysis
    # ======================================================

    def group_analysis(self, df, category_column, numeric_column):

        if df is None or df.empty:
            return pd.DataFrame()

        if category_column not in df.columns:
            return pd.DataFrame()

        if numeric_column not in df.columns:
            return pd.DataFrame()

        result = (
            df.groupby(category_column)[numeric_column]
            .agg(
                Count="count",
                Sum="sum",
                Minimum="min",
                Maximum="max",
                Median="median"
            )
            .reset_index()
        )

        return result.round(2)


    # ======================================================
    # Top / Bottom Analysis
    # ======================================================

    def top_bottom(self, df, column, n=10, ascending=False):

        if df is None or df.empty:
            return pd.DataFrame()

        if column not in df.columns:
            return pd.DataFrame()

        result = (
            df[[column]]
            .dropna()
            .sort_values(
                by=column,
                ascending=ascending
            )
            .head(n)
        )

        return result.reset_index(drop=True)


    # ======================================================
    # Category Frequency
    # ======================================================

    def category_frequency(self, df, column):

        if df is None or df.empty:
            return pd.DataFrame()

        if column not in df.columns:
            return pd.DataFrame()

        result = (
            df[column]
            .value_counts(dropna=False)
            .reset_index()
        )

        result.columns = [
            column,
            "Count"
        ]

        return result


    # ======================================================
    # Outlier Detection
    # ======================================================

    def detect_outliers(self, df, column):

        if df is None or df.empty:
            return pd.DataFrame()

        if column not in df.columns:
            return pd.DataFrame()

        if not pd.api.types.is_numeric_dtype(df[column]):
            return pd.DataFrame()

        series = df[column].dropna()

        if series.empty:
            return pd.DataFrame()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ].copy()

        return outliers


    # ======================================================
    # Numeric / Categorical Columns
    # ======================================================

    def get_numeric_columns(self, df):

        if df is None or df.empty:
            return []

        return list(
            df.select_dtypes(include="number").columns
        )


    def get_categorical_columns(self, df):

        if df is None or df.empty:
            return []

        return list(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        )

    