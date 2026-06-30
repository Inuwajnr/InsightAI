import pandas as pd


class CorrelationAnalyzer:

    def get_correlation_matrix(self, df):

        numeric_df = df.select_dtypes(
            include="number"
        )

        if numeric_df.shape[1] < 2:
            return None

        return numeric_df.corr()