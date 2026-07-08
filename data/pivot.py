import pandas as pd


class PivotEngine:

    def create_pivot(
        self,
        df,
        rows,
        columns,
        values,
        agg_function
    ):

        if not rows:
            rows = None

        if not columns:
            columns = None

        # Single value
        if len(values) == 1:
            values = values[0]

        pivot = pd.pivot_table(
            df,
            index=rows,
            columns=columns,
            values=values,
            aggfunc=agg_function,
            fill_value=0,
            observed=False
        )

        if isinstance(pivot.columns, pd.MultiIndex):

            pivot.columns = [
                " - ".join(map(str, col))
                for col in pivot.columns
            ]

        return pivot