import pandas as pd


class ChartRecommender:

    def recommend(
        self,
        df,
        x_col,
        y_col=None
    ):

        if y_col is None:

            if pd.api.types.is_numeric_dtype(df[x_col]):

                return "Histogram"

            return "Pie Chart"

        x_numeric = pd.api.types.is_numeric_dtype(
            df[x_col]
        )

        y_numeric = pd.api.types.is_numeric_dtype(
            df[y_col]
        )

        if x_numeric and y_numeric:

            return "Scatter Plot"

        if (not x_numeric) and y_numeric:

            return "Bar Chart"

        if "date" in x_col.lower():

            return "Line Chart"

        return "Column Chart"