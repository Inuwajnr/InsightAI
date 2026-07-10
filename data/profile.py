import pandas as pd


class DatasetProfile:

    def generate_profile(self, df):

        numeric_cols = list(
            df.select_dtypes(include="number").columns
        )

        categorical_cols = list(
            df.select_dtypes(exclude="number").columns
        )

        memory = (
            df.memory_usage(deep=True)
            .sum() / 1024 / 1024
        )

        profile = {

            # Basic information
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory": round(memory, 2),

            # Column counts
            "numeric_columns": len(numeric_cols),
            "categorical_columns": len(categorical_cols),

            # Column names
            "column_names": list(df.columns),
            "numeric_column_names": numeric_cols,
            "categorical_column_names": categorical_cols,

            # Data types
            "data_types": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            },

            # Missing values by column
            "missing_by_column": (
                df.isna()
                .sum()
                .to_dict()
            )

        }

        return profile