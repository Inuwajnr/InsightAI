import pandas as pd


class DataAnalyzer:

    # ==========================================
    # File Handling
    # ==========================================

    def get_sheet_names(self, file_path):

        excel_file = pd.ExcelFile(file_path)

        return excel_file.sheet_names

    def load_file(self, file_path, sheet_name=None):

        if file_path.lower().endswith(".csv"):

            df = pd.read_csv(file_path)

        elif file_path.lower().endswith((".xlsx", ".xls")):

            if sheet_name:

                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name
                )

            else:

                df = pd.read_excel(file_path)

        else:

            raise ValueError(
                "Unsupported file type."
            )

        # ------------------------------------------
        # Automatically detect date-like columns
        # ------------------------------------------
        df = self.detect_date_columns(df)

        return df

    # ==========================================
    # Date Detection
    # ==========================================

    def detect_date_columns(self, df):

        new_df = df.copy()

        for column in new_df.columns:

            # Only inspect text/object columns.
            # Numeric columns and existing datetime
            # columns should remain untouched.
            if not (
                pd.api.types.is_object_dtype(
                    new_df[column]
                )
                or pd.api.types.is_string_dtype(
                    new_df[column]
                )
            ):
                continue

            # Don't try to convert completely empty columns
            non_empty = new_df[column].dropna()

            if non_empty.empty:
                continue

            # Convert a copy so the original values
            # remain untouched if this isn't a date column.
            converted = pd.to_datetime(
                non_empty,
                errors="coerce",
                dayfirst=True
            )

            valid_ratio = (
                converted.notna().mean()
            )

            # Only convert the column when a high
            # percentage of its non-empty values
            # can be interpreted as dates.
            if valid_ratio >= 0.80:

                new_df[column] = pd.to_datetime(
                    new_df[column],
                    errors="coerce",
                    dayfirst=True
                )

        return new_df

    # ==========================================
    # Main Dataset Profile
    # ==========================================

    def get_dataset_profile(self, df):

        memory = round(
            df.memory_usage(deep=True).sum() / 1024,
            2
        )

        numeric_columns = list(
            df.select_dtypes(include="number").columns
        )

        categorical_columns = list(
            df.select_dtypes(exclude="number").columns
        )

        profile = {

            # Basic Information

            "rows": len(df),

            "columns": len(df.columns),

            "missing_values": int(
                df.isna().sum().sum()
            ),

            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "memory": memory,

            # Counts

            "numeric_columns": len(
                numeric_columns
            ),

            "categorical_columns": len(
                categorical_columns
            ),

            # Lists

            "column_names": list(
                df.columns
            ),

            "numeric_column_names": numeric_columns,

            "categorical_column_names": (
                categorical_columns
            ),

            # Data Types

            "data_types": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            },

            # Missing By Column

            "missing_by_column": (
                df.isna().sum().to_dict()
            )
        }

        return profile

    # ==========================================
    # Compatibility Wrapper
    # ==========================================

    def get_summary(self, df):

        return self.get_dataset_profile(df)

    # ==========================================
    # Helper Functions
    # ==========================================

    def get_numeric_columns(self, df):

        return list(
            df.select_dtypes(
                include="number"
            ).columns
        )

    def get_categorical_columns(self, df):

        return list(
            df.select_dtypes(
                exclude="number"
            ).columns
        )

    def get_memory_usage(self, df):

        return round(
            df.memory_usage(
                deep=True
            ).sum() / 1024,
            2
        )

    def get_duplicate_count(self, df):

        return int(
            df.duplicated().sum()
        )

    def get_missing_by_column(self, df):

        return df.isna().sum().to_dict()

    def get_shape(self, df):

        return {

            "rows": df.shape[0],

            "columns": df.shape[1]
        }

    def get_data_types(self, df):

        return {

            col: str(dtype)

            for col, dtype in df.dtypes.items()

        }