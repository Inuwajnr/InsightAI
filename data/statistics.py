import pandas as pd


class StatisticsEngine:

    # ==========================================
    # DATASET SUMMARY
    # ==========================================

    def dataset_summary(self, df):

        if df is None or df.empty:
            return {
                "rows": 0,
                "columns": 0,
                "memory": 0,
                "duplicates": 0,
                "missing": 0
            }

        return {
            "rows": len(df),

            "columns": len(df.columns),

            "memory": round(
                df.memory_usage(deep=True).sum() / 1024,
                2
            ),

            "duplicates": int(
                df.duplicated().sum()
            ),

            "missing": int(
                df.isna().sum().sum()
            )
        }

    # ==========================================
    # DESCRIPTIVE STATISTICS
    # ==========================================

    def descriptive_statistics(self, df):

        if df is None or df.empty:
            return pd.DataFrame()

        return (
            df.describe(
                include="all"
            )
            .fillna("")
        )

    # ==========================================
    # MISSING VALUES
    # ==========================================

    def missing_values(self, df):

        if df is None or df.empty:
            return pd.DataFrame(
                columns=[
                    "Column",
                    "Missing Values"
                ]
            )

        result = (
            df.isna()
            .sum()
            .reset_index()
        )

        result.columns = [
            "Column",
            "Missing Values"
        ]

        return result

    # ==========================================
    # DATA TYPES
    # ==========================================

    def data_types(self, df):

        if df is None or df.empty:
            return pd.DataFrame(
                columns=[
                    "Column",
                    "Data Type"
                ]
            )

        result = (
            df.dtypes
            .reset_index()
        )

        result.columns = [
            "Column",
            "Data Type"
        ]

        return result

    # ==========================================
    # NUMERIC COLUMNS
    # ==========================================

    def numeric_columns(self, df):

        if df is None or df.empty:
            return []

        return list(
            df.select_dtypes(
                include="number"
            ).columns
        )

    # ==========================================
    # CATEGORICAL COLUMNS
    # ==========================================

    def categorical_columns(self, df):

        if df is None or df.empty:
            return []

        return list(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        )

    # ==========================================
    # CORRELATION MATRIX
    # ==========================================

    def correlation_matrix(self, df):

        if df is None or df.empty:
            return None

        numeric = df.select_dtypes(
            include="number"
        )

        if numeric.empty:
            return None

        return numeric.corr()