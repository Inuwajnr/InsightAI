import pandas as pd


class DataCleaner:

    def remove_duplicates(self, df):
        return df.drop_duplicates()

    def remove_missing_rows(self, df):
        return df.dropna()

    def fill_missing(self, df, value=0):
        return df.fillna(value)

    def trim_spaces(self, df):

        new_df = df.copy()

        for column in new_df.select_dtypes(include="object"):

            new_df[column] = (
                new_df[column]
                .astype(str)
                .str.strip()
            )

        return new_df

    def rename_columns(self, df):

        new_df = df.copy()

        new_df.columns = (
            new_df.columns
            .str.strip()
            .str.replace(" ", "_")
        )

        return new_df

    def lowercase_columns(self, df):

        new_df = df.copy()

        new_df.columns = (
            new_df.columns.str.lower()
        )

        return new_df
    
    def clean_dataset(self, df):

        report = {}

        original_rows = len(df)

        duplicate_rows = df.duplicated().sum()

        missing_before = df.isna().sum().sum()

        cleaned_df = self.trim_spaces(df)

        cleaned_df = self.remove_duplicates(cleaned_df)

        missing_after = cleaned_df.isna().sum().sum()

        report["original_rows"] = original_rows
        report["duplicates_removed"] = duplicate_rows
        report["missing_before"] = missing_before
        report["missing_after"] = missing_after
        report["final_rows"] = len(cleaned_df)

        return cleaned_df, report
    