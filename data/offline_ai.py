# data/offline_ai.py

import re
import difflib
import pandas as pd


class OfflineAIEngine:
    """
    Dataset-independent offline natural-language analytics engine.

    The engine:
    1. Reads the actual dataset structure.
    2. Understands common natural-language questions.
    3. Detects columns dynamically.
    4. Detects filters dynamically from dataset values.
    5. Performs calculations using pandas.
    6. Returns a natural-language answer.

    No internet.
    No API.
    No external AI model.
    """

    def __init__(self):
        self.stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "of",
            "to",
            "for",
            "in",
            "on",
            "at",
            "by",
            "with",
            "from",
            "and",
            "or",
            "me",
            "show",
            "tell",
            "give",
            "please",
            "what",
            "which",
            "how",
            "many",
            "much",
            "does",
            "do",
            "did",
            "can",
            "you",
            "my",
            "dataset",
            "data",
            "values",
        }

    # ==========================================================
    # PUBLIC ENTRY POINT
    # ==========================================================

    def answer(self, df, question):
        """
        Main entry point.

        Parameters
        ----------
        df : pandas.DataFrame
        question : str

        Returns
        -------
        str
        """

        if df is None or not isinstance(df, pd.DataFrame):
            return "There is currently no valid dataset loaded."

        if df.empty:
            return "The dataset is empty. Please load a dataset containing some rows."

        if not question or not question.strip():
            return "Please enter a question about the dataset."

        q = self._normalize(question)

        try:
            # --------------------------------------------------
            # Dataset structure questions
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "column names",
                    "name of columns",
                    "names of columns",
                    "list columns",
                    "list the columns",
                    "what columns",
                    "which columns",
                    "columns are there",
                ],
            ):
                return self._column_names(df)

            if self._contains_any(
                q,
                [
                    "number of columns",
                    "how many columns",
                    "total columns",
                    "count of columns",
                ],
            ):
                return f"The dataset has {len(df.columns):,} columns."

            if self._contains_any(
                q,
                [
                    "number of rows",
                    "how many rows",
                    "total rows",
                    "row count",
                    "number of records",
                    "how many records",
                    "number of entries",
                    "how many entries",
                ],
            ):
                return f"The dataset contains {len(df):,} rows."

            if self._contains_any(
                q,
                [
                    "shape of dataset",
                    "shape of the dataset",
                    "dataset shape",
                    "data shape",
                    "size of dataset",
                ],
            ):
                return (
                    f"The dataset has {len(df):,} rows "
                    f"and {len(df.columns):,} columns."
                )

            # --------------------------------------------------
            # Missing values
            # IMPORTANT: before generic column questions
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "missing",
                    "null",
                    "nulls",
                    "empty values",
                    "blank values",
                    "missing values",
                    "columns with missing",
                    "which columns have missing",
                    "where are the missing",
                ],
            ):
                return self._missing_values(df)

            # --------------------------------------------------
            # Duplicate questions
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "duplicates",
                    "duplicate rows",
                    "duplicated rows",
                    "repeated rows",
                    "repeated records",
                ],
            ):
                return self._duplicates(df)

            # --------------------------------------------------
            # Data type questions
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "data types",
                    "datatype",
                    "data type",
                    "types of columns",
                    "column types",
                    "type of each column",
                ],
            ):
                return self._data_types(df)

            if self._contains_any(
                q,
                [
                    "numeric columns",
                    "numerical columns",
                    "number columns",
                    "columns containing numbers",
                ],
            ):
                return self._numeric_columns(df)

            if self._contains_any(
                q,
                [
                    "categorical columns",
                    "category columns",
                    "categorical data",
                    "text columns",
                ],
            ):
                return self._categorical_columns(df)

            # --------------------------------------------------
            # Unique values
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "unique values",
                    "distinct values",
                    "different values",
                    "unique categories",
                    "distinct categories",
                ],
            ):
                return self._unique_values(df, q)

            # --------------------------------------------------
            # Percentage questions
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "percentage",
                    "percent",
                    "proportion",
                    "share",
                    "%",
                ],
            ):
                result = self._percentage_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Correlation
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "correlation",
                    "correlated",
                    "relationship between",
                    "relationship of",
                ],
            ):
                return self._correlation_analysis(df, q)

            # --------------------------------------------------
            # Group analysis
            # --------------------------------------------------

            if self._is_group_question(q):
                result = self._group_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Top / bottom
            # --------------------------------------------------

            if self._is_top_bottom_question(q):
                result = self._top_bottom_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Average / mean
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "average",
                    "mean",
                    "avg",
                ],
            ):
                result = self._mean_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Median
            # --------------------------------------------------

            if "median" in q:
                result = self._median_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Most common / mode
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "most common",
                    "most frequent",
                    "frequently occurs",
                    "highest frequency",
                    "mode",
                ],
            ):
                result = self._mode_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Minimum / lowest
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "lowest",
                    "smallest",
                    "minimum",
                    "minimum value",
                    "least",
                    "least value",
                ],
            ):
                result = self._min_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Maximum / highest
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "highest",
                    "largest",
                    "maximum",
                    "maximum value",
                    "greatest",
                    "most",
                ],
            ):
                result = self._max_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Sum / total
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "total",
                    "sum",
                    "combined",
                    "altogether",
                    "overall amount",
                ],
            ):
                result = self._sum_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Count questions
            # --------------------------------------------------

            if self._is_count_question(q):
                result = self._count_analysis(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Show / list values
            # --------------------------------------------------

            if self._contains_any(
                q,
                [
                    "show values",
                    "list values",
                    "show the values",
                    "list the values",
                    "what are the values",
                ],
            ):
                result = self._show_values(df, q)

                if result:
                    return result

            # --------------------------------------------------
            # Generic column-specific request
            # --------------------------------------------------

            column = self._find_column(df, q)

            if column:
                return self._generic_column_answer(df, column, q)

            # --------------------------------------------------
            # Fallback
            # --------------------------------------------------

            return self._fallback(df)

        except Exception as e:
            return (
                "I understood the question, but I couldn't complete "
                f"the analysis.\n\nTechnical detail: {e}"
            )

    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def _normalize(self, text):
        text = str(text).lower().strip()

        text = text.replace("_", " ")
        text = text.replace("-", " ")
        text = text.replace("/", " ")
        text = re.sub(r"\s+", " ", text)

        return text

    def _normalize_column(self, text):
        text = self._normalize(text)

        text = re.sub(r"[^a-z0-9 ]", "", text)

        return text.strip()

    def _contains_any(self, text, phrases):
        return any(phrase in text for phrase in phrases)

    # ==========================================================
    # COLUMN DETECTION
    # ==========================================================

    def _find_column(self, df, question):
        """
        Dynamically identify a column from the user's question.

        Priority:
        1. Exact column name
        2. Normalized exact match
        3. Token overlap
        4. Fuzzy matching
        """

        q = self._normalize(question)

        columns = list(df.columns)

        if not columns:
            return None

        # ------------------------------------------------------
        # Exact original / normalized column names
        # ------------------------------------------------------

        normalized_columns = {}

        for col in columns:
            normalized_columns[col] = self._normalize_column(col)

        for col, normalized in normalized_columns.items():

            if normalized and normalized in q:
                return col

        # ------------------------------------------------------
        # Token-based matching
        # ------------------------------------------------------

        q_tokens = {
            token
            for token in q.split()
            if token not in self.stop_words
        }

        best_column = None
        best_score = 0

        for col, normalized in normalized_columns.items():

            column_tokens = set(normalized.split())

            if not column_tokens:
                continue

            overlap = q_tokens.intersection(column_tokens)

            if overlap:
                score = len(overlap) / len(column_tokens)

                if score > best_score:
                    best_score = score
                    best_column = col

        if best_column is not None and best_score >= 0.5:
            return best_column

        # ------------------------------------------------------
        # Fuzzy matching
        # ------------------------------------------------------

        candidates = list(normalized_columns.values())

        words = [
            token
            for token in q.split()
            if token not in self.stop_words
        ]

        for word in words:

            matches = difflib.get_close_matches(
                word,
                candidates,
                n=1,
                cutoff=0.75,
            )

            if matches:

                matched = matches[0]

                for col, normalized in normalized_columns.items():

                    if normalized == matched:
                        return col

        return None

    # ==========================================================
    # NUMERIC COLUMN DETECTION
    # ==========================================================

    def _numeric_columns_list(self, df):
        return list(df.select_dtypes(include="number").columns)

    def _categorical_columns_list(self, df):
        return list(
            df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns
        )

    def _find_numeric_column(self, df, question):
        """
        Find a numeric column mentioned in the question.
        """

        numeric_columns = self._numeric_columns_list(df)

        if not numeric_columns:
            return None

        # First try normal column matching.
        column = self._find_column(df, question)

        if column in numeric_columns:
            return column

        # Try each numeric column independently.
        q = self._normalize(question)

        best_column = None
        best_score = 0

        for col in numeric_columns:

            normalized = self._normalize_column(col)

            tokens = normalized.split()

            score = 0

            for token in tokens:

                if token in q.split():
                    score += 1

            if tokens:
                ratio = score / len(tokens)

                if ratio > best_score:
                    best_score = ratio
                    best_column = col

        if best_score >= 0.5:
            return best_column

        # If only one numeric column exists, use it.
        if len(numeric_columns) == 1:
            return numeric_columns[0]

        return None

    # ==========================================================
    # CATEGORY VALUE DETECTION
    # ==========================================================

    def _find_category_value(self, df, question, exclude_column=None):
        """
        Find an actual categorical value mentioned in the question.

        Example:

        Dataset:
        Department = Sales, IT, HR

        Question:
        "What is the total salary for people in IT?"

        Returns:
        ("Department", "IT")
        """

        q = self._normalize(question)

        categorical_columns = self._categorical_columns_list(df)

        for col in categorical_columns:

            if exclude_column and col == exclude_column:
                continue

            values = df[col].dropna().astype(str).unique()

            # Prefer longer values first.
            values = sorted(
                values,
                key=lambda x: len(str(x)),
                reverse=True,
            )

            for value in values:

                value_normalized = self._normalize(str(value))

                if not value_normalized:
                    continue

                pattern = r"\b" + re.escape(value_normalized) + r"\b"

                if re.search(pattern, q):
                    return col, value

        return None, None

    # ==========================================================
    # DATASET INFORMATION
    # ==========================================================

    def _column_names(self, df):
        columns = list(df.columns)

        if not columns:
            return "The dataset has no columns."

        lines = ["The dataset contains these columns:"]

        for index, column in enumerate(columns, start=1):
            lines.append(f"{index}. {column}")

        return "\n".join(lines)

    def _data_types(self, df):
        lines = ["Column data types:"]

        for column in df.columns:
            dtype = str(df[column].dtype)

            lines.append(
                f"• {column}: {dtype}"
            )

        return "\n".join(lines)

    def _numeric_columns(self, df):
        columns = self._numeric_columns_list(df)

        if not columns:
            return "There are no numeric columns in this dataset."

        return (
            "Numeric columns:\n"
            + "\n".join(f"• {column}" for column in columns)
        )

    def _categorical_columns(self, df):
        columns = self._categorical_columns_list(df)

        if not columns:
            return "There are no categorical columns in this dataset."

        return (
            "Categorical columns:\n"
            + "\n".join(f"• {column}" for column in columns)
        )

    # ==========================================================
    # MISSING VALUES
    # ==========================================================

    def _missing_values(self, df):
        missing = df.isna().sum()

        missing = missing[missing > 0]

        if missing.empty:
            return "There are no missing values in the dataset."

        lines = ["Columns containing missing values:"]

        for column, count in missing.items():
            lines.append(
                f"• {column}: {int(count):,} missing"
            )

        total = int(missing.sum())

        lines.append("")
        lines.append(
            f"Total missing values: {total:,}"
        )

        return "\n".join(lines)

    # ==========================================================
    # DUPLICATES
    # ==========================================================

    def _duplicates(self, df):
        count = int(df.duplicated().sum())

        if count == 0:
            return "There are no duplicate rows in the dataset."

        return (
            f"The dataset contains {count:,} duplicate rows."
        )

    # ==========================================================
    # UNIQUE VALUES
    # ==========================================================

    def _unique_values(self, df, question):
        column = self._find_column(df, question)

        if not column:
            categorical = self._categorical_columns_list(df)

            if len(categorical) == 1:
                column = categorical[0]

        if not column:
            return (
                "I couldn't determine which column you want "
                "the unique values for."
            )

        values = df[column].dropna().unique()

        if len(values) == 0:
            return f"The column '{column}' contains no non-empty values."

        if len(values) > 30:
            preview = values[:30]

            return (
                f"'{column}' contains {len(values):,} unique values.\n\n"
                "First 30 values:\n"
                + "\n".join(
                    f"• {value}"
                    for value in preview
                )
            )

        return (
            f"'{column}' contains {len(values):,} unique values:\n\n"
            + "\n".join(
                f"• {value}"
                for value in values
            )
        )

    # ==========================================================
    # SUM
    # ==========================================================

    def _sum_analysis(self, df, question):
        column = self._find_numeric_column(df, question)

        if not column:
            return None

        data = df[column].dropna()

        if data.empty:
            return f"There are no numeric values available in '{column}'."

        category_col, category_value = self._find_category_value(
            df,
            question,
            exclude_column=column,
        )

        if category_col and category_value is not None:

            filtered = df[
                df[category_col].astype(str).str.lower()
                == str(category_value).lower()
            ]

            values = pd.to_numeric(
                filtered[column],
                errors="coerce",
            ).dropna()

            if values.empty:
                return (
                    f"There are no numeric values in '{column}' "
                    f"for {category_col} = {category_value}."
                )

            total = values.sum()

            return (
                f"The total {column} for "
                f"{category_col} = {category_value} is "
                f"{self._format_number(total)}."
            )

        total = pd.to_numeric(
            data,
            errors="coerce",
        ).sum()

        return (
            f"The total {column} is "
            f"{self._format_number(total)}."
        )

    # ==========================================================
    # MEAN
    # ==========================================================

    def _mean_analysis(self, df, question):
        column = self._find_numeric_column(df, question)

        if not column:
            return None

        values = pd.to_numeric(
            df[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return None

        category_col, category_value = self._find_category_value(
            df,
            question,
            exclude_column=column,
        )

        if category_col and category_value is not None:

            filtered = df[
                df[category_col].astype(str).str.lower()
                == str(category_value).lower()
            ]

            values = pd.to_numeric(
                filtered[column],
                errors="coerce",
            ).dropna()

            if values.empty:
                return None

            result = values.mean()

            return (
                f"The average {column} for "
                f"{category_col} = {category_value} is "
                f"{self._format_number(result)}."
            )

        result = values.mean()

        return (
            f"The average {column} is "
            f"{self._format_number(result)}."
        )

    # ==========================================================
    # MEDIAN
    # ==========================================================

    def _median_analysis(self, df, question):
        column = self._find_numeric_column(df, question)

        if not column:
            return None

        values = pd.to_numeric(
            df[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return None

        result = values.median()

        return (
            f"The median {column} is "
            f"{self._format_number(result)}."
        )

    # ==========================================================
    # MODE / MOST COMMON
    # ==========================================================

    def _mode_analysis(self, df, question):
        column = self._find_column(df, question)

        if not column:
            categorical = self._categorical_columns_list(df)

            if len(categorical) == 1:
                column = categorical[0]

        if not column:
            return None

        values = df[column].dropna()

        if values.empty:
            return None

        mode = values.mode()

        if mode.empty:
            return None

        if len(mode) == 1:
            return (
                f"The most common value in '{column}' is "
                f"'{mode.iloc[0]}'."
            )

        return (
            f"The most common values in '{column}' are: "
            + ", ".join(
                str(value)
                for value in mode
            )
            + "."
        )

    # ==========================================================
    # MAXIMUM
    # ==========================================================

    def _max_analysis(self, df, question):
        column = self._find_numeric_column(df, question)

        if not column:
            return None

        values = pd.to_numeric(
            df[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return None

        maximum = values.max()

        row = df.loc[
            pd.to_numeric(
                df[column],
                errors="coerce",
            ).idxmax()
        ]

        category_col, category_value = self._find_category_value(
            df,
            question,
            exclude_column=column,
        )

        if category_col and category_value is not None:

            filtered = df[
                df[category_col].astype(str).str.lower()
                == str(category_value).lower()
            ]

            filtered_values = pd.to_numeric(
                filtered[column],
                errors="coerce",
            ).dropna()

            if not filtered_values.empty:

                maximum = filtered_values.max()

                return (
                    f"The highest {column} for "
                    f"{category_col} = {category_value} is "
                    f"{self._format_number(maximum)}."
                )

        return (
            f"The highest {column} is "
            f"{self._format_number(maximum)}."
        )

    # ==========================================================
    # MINIMUM
    # ==========================================================

    def _min_analysis(self, df, question):
        column = self._find_numeric_column(df, question)

        if not column:
            return None

        values = pd.to_numeric(
            df[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return None

        minimum = values.min()

        return (
            f"The lowest {column} is "
            f"{self._format_number(minimum)}."
        )

    # ==========================================================
    # COUNT
    # ==========================================================

    def _count_analysis(self, df, question):
        """
        Handles questions such as:

        How many employees?
        How many products?
        How many are female?
        How many sales are in Lagos?
        Count the records where Department is IT.
        """

        category_col, category_value = self._find_category_value(
            df,
            question,
        )

        if category_col and category_value is not None:

            filtered = df[
                df[category_col].astype(str).str.lower()
                == str(category_value).lower()
            ]

            return (
                f"There are {len(filtered):,} rows where "
                f"{category_col} = {category_value}."
            )

        column = self._find_column(df, question)

        if column:

            count = int(df[column].notna().sum())

            return (
                f"'{column}' contains "
                f"{count:,} non-empty values."
            )

        return (
            f"The dataset contains {len(df):,} rows."
        )

    # ==========================================================
    # PERCENTAGE
    # ==========================================================

    def _percentage_analysis(self, df, question):
        category_col, category_value = self._find_category_value(
            df,
            question,
        )

        if category_col and category_value is not None:

            matching = (
                df[category_col].astype(str).str.lower()
                == str(category_value).lower()
            )

            percentage = (
                matching.sum()
                / len(df)
                * 100
            )

            return (
                f"{category_value} represents "
                f"{percentage:.2f}% of the dataset "
                f"({matching.sum():,} out of {len(df):,} rows)."
            )

        # Percentage of a column that is non-empty
        column = self._find_column(df, question)

        if column:

            non_empty = int(df[column].notna().sum())

            percentage = (
                non_empty
                / len(df)
                * 100
            )

            return (
                f"{percentage:.2f}% of the values in "
                f"'{column}' are non-empty."
            )

        return None

    # ==========================================================
    # GROUP ANALYSIS
    # ==========================================================

    def _is_group_question(self, question):
        return self._contains_any(
            question,
            [
                "by",
                "per",
                "for each",
                "grouped by",
                "group by",
                "compare",
                "breakdown",
                "break down",
                "according to",
            ],
        )

    def _group_analysis(self, df, question):
        numeric_columns = self._numeric_columns_list(df)
        categorical_columns = self._categorical_columns_list(df)

        if not categorical_columns:
            return None

        # ------------------------------------------------------
        # Detect grouping column.
        # ------------------------------------------------------

        group_column = None

        # Try column mentioned after "by"
        patterns = [
            r"\bby\s+(.+?)(?:$|,|\?| for | with )",
            r"\bper\s+(.+?)(?:$|,|\?| for | with )",
            r"\bgrouped by\s+(.+?)(?:$|,|\?| for | with )",
        ]

        for pattern in patterns:

            match = re.search(pattern, question)

            if match:

                candidate = match.group(1).strip()

                group_column = self._find_column(
                    df,
                    candidate,
                )

                if group_column in categorical_columns:
                    break

                group_column = None

        # Generic column detection
        if not group_column:

            for column in categorical_columns:

                normalized = self._normalize_column(column)

                if normalized in question:
                    group_column = column
                    break

        # If only one categorical column exists
        if not group_column and len(categorical_columns) == 1:
            group_column = categorical_columns[0]

        if not group_column:
            return None

        # ------------------------------------------------------
        # Detect numeric metric.
        # ------------------------------------------------------

        metric_column = self._find_numeric_column(
            df,
            question,
        )

        if not metric_column and numeric_columns:
            metric_column = numeric_columns[0]

        if not metric_column:
            return None

        grouped = (
            df.groupby(group_column)[metric_column]
            .agg(["count", "sum", "mean"])
            .sort_values("sum", ascending=False)
        )

        if grouped.empty:
            return None

        lines = [
            f"Analysis of '{metric_column}' by '{group_column}':",
            "",
        ]

        for index, row in grouped.head(20).iterrows():

            lines.append(
                f"• {index}: "
                f"count={int(row['count']):,}, "
                f"total={self._format_number(row['sum'])}, "
                f"average={self._format_number(row['mean'])}"
            )

        if len(grouped) > 20:
            lines.append("")
            lines.append(
                f"Showing the first 20 of {len(grouped):,} groups."
            )

        return "\n".join(lines)

    # ==========================================================
    # TOP / BOTTOM
    # ==========================================================

    def _is_top_bottom_question(self, question):
        return self._contains_any(
            question,
            [
                "top",
                "highest",
                "largest",
                "bottom",
                "lowest",
                "smallest",
                "best",
                "worst",
            ],
        )

    def _extract_number(self, question):
        patterns = [
            r"\b(?:top|bottom|first|last)\s+(\d+)\b",
            r"\b(\d+)\s+(?:highest|lowest|largest|smallest)\b",
            r"\btop\s+(\d+)",
            r"\bbottom\s+(\d+)",
        ]

        for pattern in patterns:

            match = re.search(pattern, question)

            if match:
                return int(match.group(1))

        return 5

    def _top_bottom_analysis(self, df, question):
        number = self._extract_number(question)

        column = self._find_numeric_column(df, question)

        if not column:
            return None

        ascending = self._contains_any(
            question,
            [
                "bottom",
                "lowest",
                "smallest",
                "worst",
            ],
        )

        result = df.sort_values(
            by=column,
            ascending=ascending,
        ).head(number)

        if result.empty:
            return None

        direction = "lowest" if ascending else "highest"

        lines = [
            f"Top {number} rows by '{column}' ({direction}):",
            "",
        ]

        for index, row in result.iterrows():

            value = row[column]

            lines.append(
                f"• Row {index}: "
                f"{self._format_number(value)}"
            )

        return "\n".join(lines)

    # ==========================================================
    # CORRELATION
    # ==========================================================

    def _correlation_analysis(self, df, question):
        numeric = self._numeric_columns_list(df)

        if len(numeric) < 2:
            return (
                "Correlation requires at least two numeric columns."
            )

        mentioned = []

        for column in numeric:

            normalized = self._normalize_column(column)

            if normalized in question:
                mentioned.append(column)

        if len(mentioned) >= 2:
            first = mentioned[0]
            second = mentioned[1]

        else:
            first = numeric[0]
            second = numeric[1]

        values = df[[first, second]].apply(
            pd.to_numeric,
            errors="coerce",
        ).dropna()

        if len(values) < 2:
            return "There are not enough valid values to calculate correlation."

        correlation = values[first].corr(values[second])

        strength = self._correlation_strength(correlation)

        direction = (
            "positive"
            if correlation > 0
            else "negative"
            if correlation < 0
            else "no"
        )

        return (
            f"The correlation between '{first}' and '{second}' "
            f"is {correlation:.3f}.\n\n"
            f"This indicates a {strength} {direction} linear relationship."
        )

    def _correlation_strength(self, value):
        absolute = abs(value)

        if absolute >= 0.8:
            return "strong"

        if absolute >= 0.5:
            return "moderate"

        if absolute >= 0.3:
            return "weak"

        return "very weak"

    # ==========================================================
    # SHOW VALUES
    # ==========================================================

    def _show_values(self, df, question):
        column = self._find_column(df, question)

        if not column:
            return None

        values = df[column].dropna().unique()

        if len(values) > 30:
            values = values[:30]

        return (
            f"Values in '{column}':\n"
            + "\n".join(
                f"• {value}"
                for value in values
            )
        )

    # ==========================================================
    # GENERIC COLUMN ANSWER
    # ==========================================================

    def _generic_column_answer(self, df, column, question):
        series = df[column]

        if pd.api.types.is_numeric_dtype(series):

            values = pd.to_numeric(
                series,
                errors="coerce",
            ).dropna()

            if values.empty:
                return (
                    f"'{column}' is numeric, but it contains "
                    "no usable numeric values."
                )

            return (
                f"'{column}' is a numeric column.\n"
                f"Non-empty values: {len(values):,}\n"
                f"Minimum: {self._format_number(values.min())}\n"
                f"Maximum: {self._format_number(values.max())}\n"
                f"Unique values: {values.nunique():,}"
            )

        values = series.dropna()

        return (
            f"'{column}' contains {len(values):,} non-empty values "
            f"and {values.nunique():,} unique values."
        )

    # ==========================================================
    # FALLBACK
    # ==========================================================

    def _fallback(self, df):
        numeric = self._numeric_columns_list(df)
        categorical = self._categorical_columns_list(df)

        lines = [
            "I couldn't determine the exact analysis you want.",
            "",
            "I can analyze this dataset using questions such as:",
            "",
            "• How many rows are there?",
            "• Which columns have missing values?",
            "• What are the column names?",
            "• What is the total [numeric column]?",
            "• What is the highest [numeric column]?",
            "• What is the lowest [numeric column]?",
            "• What is the average [numeric column]?",
            "• What is the median [numeric column]?",
            "• What is the most common [categorical column]?",
            "• Show [numeric column] by [categorical column].",
            "• What percentage is [category value]?",
            "• What is the correlation between [column 1] and [column 2]?",
            "• Show the top 5 [numeric column] values.",
            "",
            f"Detected numeric columns: {len(numeric)}",
            f"Detected categorical columns: {len(categorical)}",
        ]

        return "\n".join(lines)

    # ==========================================================
    # FORMATTING
    # ==========================================================

    def _format_number(self, value):
        try:

            if pd.isna(value):
                return "N/A"

            value = float(value)

            if value.is_integer():
                return f"{int(value):,}"

            return f"{value:,.2f}"

        except Exception:
            return str(value)