import pandas as pd


class DatasetProfiler:

    def profile(self, df):

        profile = {}

        # ==========================
        # Basic Information
        # ==========================

        profile["rows"] = len(df)
        profile["columns"] = len(df.columns)

        profile["memory"] = round(
            df.memory_usage(deep=True).sum() / 1024,
            2
        )

        profile["duplicates"] = int(
            df.duplicated().sum()
        )

        profile["missing"] = int(
            df.isna().sum().sum()
        )

        # ==========================
        # Column Classification
        # ==========================

        numeric = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        categorical = list(
            df.select_dtypes(
                include="object"
            ).columns
        )

        datetime_cols = []

        for col in df.columns:

            try:

                pd.to_datetime(
                    df[col],
                    errors="raise"
                )

                datetime_cols.append(col)

            except Exception:
                pass

        profile["numeric_columns"] = numeric
        profile["categorical_columns"] = categorical
        profile["date_columns"] = datetime_cols

        return profile
    

    def detect_measures(self, df):

        keywords = [
            "sales",
            "profit",
            "revenue",
            "amount",
            "cost",
            "price",
            "quantity",
            "income",
            "expense"
        ]

        measures = []

        for col in df.columns:

            name = col.lower()

            if any(word in name for word in keywords):
                measures.append(col)

        return measures
    
    def detect_dimensions(self, df):

        dimensions = []

        for col in df.columns:

            if df[col].dtype == "object":
                dimensions.append(col)

        return dimensions
    
    def recommend_chart(self, df):

        measures = self.detect_measures(df)

        dimensions = self.detect_dimensions(df)

        if measures and dimensions:

            return {
                "chart": "Bar Chart",
                "x": dimensions[0],
                "y": measures[0]
            }

        numeric = list(
            df.select_dtypes(include="number").columns
        )

        if len(numeric) >= 2:

            return {
                "chart": "Scatter Plot",
                "x": numeric[0],
                "y": numeric[1]
            }

        return {
            "chart": "Table"
        }
    
    