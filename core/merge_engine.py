import pandas as pd


class MergeEngine:

    def merge(
        self,
        left_df,
        right_df,
        left_key,
        right_key,
        join_type="left"
    ):
        """
        Merge two datasets.

        join_type:
            left
            right
            inner
            outer
        """

        merged = pd.merge(
            left_df,
            right_df,
            left_on=left_key,
            right_on=right_key,
            how=join_type
        )

        return merged