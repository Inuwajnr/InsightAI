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
            index=rows if rows else None,
            columns=columns if columns else None,
            values=values,
            aggfunc=agg_function,
            fill_value=0,
            observed=False
        )

        return pivot