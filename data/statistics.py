import pandas as pd


class StatisticsEngine:

    def dataset_summary(self, df):

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "memory": round(
                df.memory_usage(deep=True).sum() / 1024,
                2
            ),
            "duplicates": df.duplicated().sum(),
            "missing": df.isna().sum().sum()
        }


    def descriptive_statistics(self, df):

        return df.describe(include="all").fillna("")


    def missing_values(self, df):

        return (
            df.isna()
            .sum()
            .reset_index()
            .rename(
                columns={
                    "index": "Column",
                    0: "Missing Values"
                }
            )
        )


    def data_types(self, df):

        return (
            df.dtypes
            .reset_index()
            .rename(
                columns={
                    "index": "Column",
                    0: "Data Type"
                }
            )
        )


    def numeric_columns(self, df):

        return list(
            df.select_dtypes(
                include="number"
            ).columns
        )


    def categorical_columns(self, df):

        return list(
            df.select_dtypes(
                include="object"
            ).columns
        )


    def correlation_matrix(self, df):

        numeric = df.select_dtypes(include="number")

        if numeric.empty:
            return None

        return numeric.corr()