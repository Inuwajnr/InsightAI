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

            "rows": len(df),

            "columns": len(df.columns),

            "numeric": len(numeric_cols),

            "categorical": len(categorical_cols),

            "missing": int(
                df.isna().sum().sum()
            ),

            "duplicates": int(
                df.duplicated().sum()
            ),

            "memory": round(memory, 2)

        }

        return profile