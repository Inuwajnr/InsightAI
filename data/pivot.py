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

        pivot = pd.pivot_table(
            df,
            index=rows,
            columns=columns,
            values=values,
            aggfunc=agg_function,
            fill_value=0
        )

        return pivot.reset_index()