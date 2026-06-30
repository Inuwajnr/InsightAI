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

            return pd.read_csv(file_path)

        elif file_path.lower().endswith((".xlsx", ".xls")):

            if sheet_name:

                return pd.read_excel(
                    file_path,
                    sheet_name=sheet_name
                )

            return pd.read_excel(file_path)

        raise ValueError(
            "Unsupported file type."
        )

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

            "numeric_columns": len(numeric_columns),

            "categorical_columns": len(categorical_columns),

            # Lists

            "column_names": list(df.columns),

            "numeric_column_names": numeric_columns,

            "categorical_column_names": categorical_columns,

            # Data Types

            "data_types": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            },

            # Missing By Column

            "missing_by_column": df.isna().sum().to_dict()
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
            df.select_dtypes(include="number").columns
        )

    def get_categorical_columns(self, df):

        return list(
            df.select_dtypes(exclude="number").columns
        )

    def get_memory_usage(self, df):

        return round(
            df.memory_usage(deep=True).sum() / 1024,
            2
        )

    def get_duplicate_count(self, df):

        return int(df.duplicated().sum())

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