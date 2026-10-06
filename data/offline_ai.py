import json
import re
from typing import Any, Dict, Optional

import pandas as pd

from core.ollama_client import OllamaClient


class OfflineAIEngine:
    """
    Hybrid offline AI engine for InsightAI.

    Fast path:
        Handles obvious analytical questions directly with Pandas.

    AI path:
        Uses Qwen3 8B only when natural-language understanding
        is actually required.

    Pandas is always the authority for calculations.
    """

    def __init__(self):

        self.llm = OllamaClient(
            model="qwen3:8b",
            base_url="http://localhost:11434",
        )

    # ==========================================================
    # PUBLIC METHOD
    # ==========================================================

    def answer(
        self,
        df: pd.DataFrame,
        question: str
    ) -> str:

        if df is None or df.empty:

            return (
                "There is currently no usable dataset loaded. "
                "Please upload a CSV or Excel dataset first."
            )

        if not question or not question.strip():

            return (
                "Please enter a question about the dataset."
            )

        question = question.strip()

        try:

            # ==================================================
            # FAST PATH
            # ==================================================

            fast_result = self._fast_path(
                df,
                question
            )

            if fast_result is not None:

                return fast_result

            # ==================================================
            # AI PATH
            # ==================================================

            plan = self._understand_question(
                df,
                question
            )

            plan = self._validate_plan(
                df,
                plan
            )

            result = self._execute_plan(
                df,
                plan,
                question
            )

            if result is None:

                return self._fallback_answer(
                    df,
                    question
                )

            # Simple verified results do not require
            # another Qwen request.

            if self._is_simple_result(result):

                return self._format_result(
                    result
                )

            # Complex interpretation can use Qwen.

            return self._explain_result(
                question,
                result
            )

        except Exception as e:

            print(
                "OfflineAIEngine error:",
                repr(e)
            )

            return (
                "I couldn't complete that analysis right now. "
                "Please try rephrasing the question."
            )

    # ==========================================================
    # FAST PATH
    # ==========================================================

    def _fast_path(
        self,
        df: pd.DataFrame,
        question: str
    ) -> Optional[str]:

        q = question.lower().strip()

        # Get column types from the current dataset
        numeric_columns = list(
            df.select_dtypes(include="number").columns
        )

        categorical_columns = list(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        )

        normalized = re.sub(
            r"[^a-z0-9\s]",
            " ",
            q
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized
        ).strip()

        # ------------------------------------------------------
        # ROW COUNT
        # ------------------------------------------------------

        row_patterns = [
            r"\bhow many rows\b",
            r"\bnumber of rows\b",
            r"\btotal rows\b",
            r"\bhow many records\b",
            r"\bnumber of records\b",
            r"\btotal records\b",
            r"\bhow many observations\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in row_patterns
        ):

            return (
                f"The dataset contains "
                f"{len(df):,} rows."
            )

        # ------------------------------------------------------
        # COLUMN COUNT
        # ------------------------------------------------------

        column_count_patterns = [
            r"\bhow many columns\b",
            r"\bnumber of columns\b",
            r"\btotal columns\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in column_count_patterns
        ):

            return (
                f"The dataset contains "
                f"{len(df.columns):,} columns."
            )

        # ------------------------------------------------------
        # SHOW COLUMN NAMES
        # ------------------------------------------------------

        column_patterns = [
            r"\bwhat are the columns\b",
            r"\bwhich columns are there\b",
            r"\blist the columns\b",
            r"\bshow the columns\b",
            r"\bcolumn names\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in column_patterns
        ):

            columns = list(
                df.columns
            )

            return (
                "The dataset contains "
                f"{len(columns)} columns:\n\n"
                + "\n".join(
                    f"{i + 1}. {column}"
                    for i, column
                    in enumerate(columns)
                )
            )

        # ------------------------------------------------------
        # MISSING VALUES
        # ------------------------------------------------------

        missing_patterns = [
            r"\bmissing values\b",
            r"\bmissing data\b",
            r"\bnull values\b",
            r"\bnulls\b",
            r"\bwhich columns.*missing\b",
            r"\bcolumns.*missing\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in missing_patterns
        ):

            return self._fast_missing_values(
                df
            )

        # ------------------------------------------------------
        # DUPLICATES
        # ------------------------------------------------------

        duplicate_patterns = [
            r"\bduplicate rows\b",
            r"\bduplicates\b",
            r"\bduplicated rows\b",
            r"\bhow many duplicates\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in duplicate_patterns
        ):

            duplicates = int(
                df.duplicated().sum()
            )

            return (
                f"The dataset contains "
                f"{duplicates:,} duplicate rows."
            )

        # ------------------------------------------------------
        # DATA TYPES
        # ------------------------------------------------------

        datatype_patterns = [
            r"\bdata types\b",
            r"\bcolumn types\b",
            r"\btypes of columns\b",
            r"\bwhat type.*columns\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in datatype_patterns
        ):

            lines = []

            for column in df.columns:

                lines.append(
                    f"• {column}: "
                    f"{df[column].dtype}"
                )

            return (
                "Column data types:\n\n"
                + "\n".join(lines)
            )

        # ------------------------------------------------------
        # NUMERIC COLUMNS
        # ------------------------------------------------------

        numeric_patterns = [
            r"\bnumeric columns\b",
            r"\bnumber columns\b",
            r"\bwhich columns are numeric\b",
            r"\bwhich columns contain numbers\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in numeric_patterns
        ):

            numeric = list(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            if not numeric:

                return (
                    "There are no numeric "
                    "columns in the dataset."
                )

            return (
                "Numeric columns:\n\n"
                + "\n".join(
                    f"• {column}"
                    for column in numeric
                )
            )

        # ------------------------------------------------------
        # CATEGORICAL COLUMNS
        # ------------------------------------------------------

        categorical_patterns = [
            r"\bcategorical columns\b",
            r"\bwhich columns are categorical\b",
            r"\bwhich columns contain categories\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in categorical_patterns
        ):

            categorical = list(
                df.select_dtypes(
                    include=[
                        "object",
                        "category"
                    ]
                ).columns
            )

            if not categorical:

                return (
                    "There are no categorical "
                    "columns in the dataset."
                )

            return (
                "Categorical columns:\n\n"
                + "\n".join(
                    f"• {column}"
                    for column in categorical
                )
            )

        # ------------------------------------------------------
        # FILTERED TOTAL / SUM
        # Examples:
        # "What is the total quantity for South?"
        # "What is the total unit price for North?"
        # "Sum quantity for West"
        # ------------------------------------------------------

        filtered_total_match = re.search(
            r"\b(?:total|sum of|sum)\s+"
            r"(?:the\s+)?(.+?)\s+"
            r"(?:for|of|in)\s+"
            r"(.+?)(?:\?|$)",
            question.lower().strip()
        )

        if filtered_total_match:

            value_column_text = (
                filtered_total_match.group(1)
                .strip()
            )

            filter_value_text = (
                filtered_total_match.group(2)
                .strip()
            )

            # Find the numeric column
            value_col = None

            for col in numeric_columns:

                col_clean = (
                    str(col)
                    .lower()
                    .strip()
                )

                if (
                    value_column_text == col_clean
                    or value_column_text.rstrip("s")
                    == col_clean.rstrip("s")
                    or col_clean.rstrip("s")
                    == value_column_text.rstrip("s")
                ):
                    value_col = col
                    break

            # Find the categorical column and value
            filter_col = None
            filter_value = None

            for col in categorical_columns:

                values = (
                    df[col]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                for value in values:

                    value_clean = (
                        str(value)
                        .lower()
                        .strip()
                    )

                    if (
                        filter_value_text == value_clean
                        or filter_value_text in value_clean
                        or value_clean in filter_value_text
                    ):
                        filter_col = col
                        filter_value = value
                        break

                if filter_col:
                    break

            # Calculate filtered total
            if value_col and filter_col:

                filtered_df = df[
                    df[filter_col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == str(filter_value).strip().lower()
                ]

                if not filtered_df.empty:

                    total_value = filtered_df[value_col].sum()

                    total_value = self._clean_number(
                        total_value
                    )

                    return (
                        f"The total {value_col} for "
                        f"{filter_value} is "
                        f"{total_value:,}."
                    )

                return (
                    f"I couldn't find any records for "
                    f"{filter_value}."
                )

        # ------------------------------------------------------
        # TOTAL / SUM
        # ------------------------------------------------------

        if self._contains_any(
            normalized,
            [
                "total",
                "sum of",
                "sum",
            ]
        ):

            column = self._find_column_in_question(
                df,
                normalized
            )

            if column:

                if pd.api.types.is_numeric_dtype(
                    df[column]
                ):

                    value = df[
                        column
                    ].sum()

                    value = self._clean_number(
                        value
                    )

                    return (
                        f"The total {column} "
                        f"is {value:,}."
                    )
        # ---------------------------------------------------------
        # GROUPED HIGHEST / LOWEST
        # Example:
        # "Which region has the highest quantity?"
        # "Which category has the lowest sales?"
        # ---------------------------------------------------------
        group_match = re.search(
            r"\bwhich\s+(.+?)\s+has\s+the\s+(highest|lowest|max|min|maximum|minimum)\s+(.+?)(?:\?|$)",
            question.lower().strip()
        )

        if group_match:
            group_column_text = group_match.group(1).strip()
            direction = group_match.group(2)
            value_column_text = group_match.group(3).strip()

            # Find matching categorical column
            group_col = None
            for col in categorical_columns:
                col_clean = str(col).lower().strip()

                if (
                    group_column_text == col_clean
                    or group_column_text.rstrip("s") == col_clean.rstrip("s")
                    or col_clean.rstrip("s") == group_column_text.rstrip("s")
                ):
                    group_col = col
                    break

            # Find matching numeric column
            value_col = None
            for col in numeric_columns:
                col_clean = str(col).lower().strip()

                if (
                    value_column_text == col_clean
                    or value_column_text.rstrip("s") == col_clean.rstrip("s")
                    or col_clean.rstrip("s") == value_column_text.rstrip("s")
                ):
                    value_col = col
                    break

            if group_col and value_col:
                grouped = (
                    df.groupby(group_col, dropna=False)[value_col]
                    .sum()
                    .sort_values(
                        ascending=direction in ["lowest", "min", "minimum"]
                    )
                )

                if not grouped.empty:
                    result_group = grouped.index[0]
                    result_value = grouped.iloc[0]

                    return (
                        f"{result_group} has the "
                        f"{'lowest' if direction in ['lowest', 'min', 'minimum'] else 'highest'} "
                        f"{value_col}, with {result_value:,.0f}."
                    )
        # ------------------------------------------------------
        # HIGHEST / MAXIMUM
        # ------------------------------------------------------

        if self._contains_any(
            normalized,
            [
                "highest",
                "maximum",
                "max",
                "largest",
                "greatest",
            ]
        ):

            column = self._find_column_in_question(
                df,
                normalized
            )

            if column:

                if pd.api.types.is_numeric_dtype(
                    df[column]
                ):

                    value = df[
                        column
                    ].max()

                    value = self._clean_number(
                        value
                    )

                    return (
                        f"The highest {column} "
                        f"is {value:,}."
                    )

        # ------------------------------------------------------
        # LOWEST / MINIMUM
        # ------------------------------------------------------

        if self._contains_any(
            normalized,
            [
                "lowest",
                "minimum",
                "min",
                "smallest",
            ]
        ):

            column = self._find_column_in_question(
                df,
                normalized
            )

            if column:

                if pd.api.types.is_numeric_dtype(
                    df[column]
                ):

                    value = df[
                        column
                    ].min()

                    value = self._clean_number(
                        value
                    )

                    return (
                        f"The lowest {column} "
                        f"is {value:,}."
                    )

        # ------------------------------------------------------
        # UNIQUE COUNT
        # ------------------------------------------------------

        unique_patterns = [
            r"\bhow many unique\b",
            r"\bnumber of unique\b",
            r"\bunique values\b",
            r"\bdistinct values\b",
        ]

        if any(
            re.search(
                pattern,
                normalized
            )
            for pattern in unique_patterns
        ):

            column = self._find_column_in_question(
                df,
                normalized
            )

            if column:

                count = int(
                    df[column]
                    .nunique(
                        dropna=True
                    )
                )

                return (
                    f"{column} contains "
                    f"{count:,} unique values."
                )

        # ------------------------------------------------------
        # TOP N
        # ------------------------------------------------------

        top_match = re.search(
            r"\btop\s+(\d+)\b",
            normalized
        )

        if top_match:

            number = min(
                int(
                    top_match.group(1)
                ),
                50
            )

            column = self._find_column_in_question(
                df,
                normalized
            )

            if column and pd.api.types.is_numeric_dtype(
                df[column]
            ):

                values = (
                    df[column]
                    .nlargest(number)
                    .tolist()
                )

                lines = [
                    f"{i + 1}. {self._clean_number(value):,}"
                    for i, value
                    in enumerate(values)
                ]

                return (
                    f"Top {number} values "
                    f"for {column}:\n\n"
                    + "\n".join(lines)
                )

        # ------------------------------------------------------
        # BOTTOM N
        # ------------------------------------------------------

        bottom_match = re.search(
            r"\bbottom\s+(\d+)\b",
            normalized
        )

        if bottom_match:

            number = min(
                int(
                    bottom_match.group(1)
                ),
                50
            )

            column = self._find_column_in_question(
                df,
                normalized
            )

            if column and pd.api.types.is_numeric_dtype(
                df[column]
            ):

                values = (
                    df[column]
                    .nsmallest(number)
                    .tolist()
                )

                lines = [
                    f"{i + 1}. {self._clean_number(value):,}"
                    for i, value
                    in enumerate(values)
                ]

                return (
                    f"Bottom {number} values "
                    f"for {column}:\n\n"
                    + "\n".join(lines)
                )

        # ------------------------------------------------------
        # Nothing matched.
        #
        # Let Qwen handle it.
        # ------------------------------------------------------

        return None

    # ==========================================================
    # FAST MISSING VALUES
    # ==========================================================

    def _fast_missing_values(
        self,
        df: pd.DataFrame
    ) -> str:

        missing = df.isna().sum()

        total = int(
            missing.sum()
        )

        if total == 0:

            return (
                "The dataset contains "
                "no missing values."
            )

        lines = []

        for column, count in missing.items():

            if count > 0:

                lines.append(
                    f"• {column}: {int(count)}"
                )

        return (
            f"The dataset contains "
            f"{total:,} missing values.\n\n"
            + "\n".join(lines)
        )

    # ==========================================================
    # FIND COLUMN IN QUESTION
    # ==========================================================

    def _find_column_in_question(
        self,
        df: pd.DataFrame,
        question: str
    ) -> Optional[str]:

        normalized_question = self._normalize(
            question
        )

        # Exact normalized column name
        for column in df.columns:

            normalized_column = self._normalize(
                column
            )

            if not normalized_column:
                continue

            if normalized_column in normalized_question:

                return column

        # Token-based match
        question_tokens = set(
            normalized_question.split()
        )

        best_column = None
        best_score = 0

        for column in df.columns:

            column_tokens = set(
                self._normalize(
                    column
                ).split()
            )

            if not column_tokens:
                continue

            overlap = len(
                question_tokens
                & column_tokens
            )

            score = overlap / max(
                len(column_tokens),
                1
            )

            if score > best_score:

                best_score = score
                best_column = column

        if best_score >= 0.5:

            return best_column

        return None

    # ==========================================================
    # TEXT HELPERS
    # ==========================================================

    def _contains_any(
        self,
        text: str,
        words
    ) -> bool:

        for word in words:

            if re.search(
                rf"\b{re.escape(word)}\b",
                text
            ):

                return True

        return False

    def _normalize(
        self,
        value: Any
    ) -> str:

        value = str(
            value
        ).lower().strip()

        value = re.sub(
            r"[^a-z0-9]+",
            " ",
            value
        )

        return re.sub(
            r"\s+",
            " ",
            value
        ).strip()

    # ==========================================================
    # DATASET CONTEXT
    # ==========================================================

    def _dataset_context(
        self,
        df: pd.DataFrame
    ) -> Dict[str, Any]:

        columns = []

        for column in df.columns:

            series = df[column]

            info = {
                "name": str(column),
                "dtype": str(series.dtype),
                "numeric": bool(
                    pd.api.types.is_numeric_dtype(
                        series
                    )
                ),
                "missing": int(
                    series.isna().sum()
                ),
                "unique": int(
                    series.nunique(
                        dropna=True
                    )
                ),
            }

            if not pd.api.types.is_numeric_dtype(
                series
            ):

                info[
                    "sample_values"
                ] = (
                    series
                    .dropna()
                    .astype(str)
                    .value_counts()
                    .head(8)
                    .index
                    .tolist()
                )

            columns.append(
                info
            )

        return {
            "rows": int(
                len(df)
            ),
            "columns": int(
                len(df.columns)
            ),
            "column_information": columns,
        }

    # ==========================================================
    # UNDERSTAND QUESTION WITH QWEN
    # ==========================================================

    def _understand_question(
        self,
        df: pd.DataFrame,
        question: str
    ) -> Dict[str, Any]:

        context = self._dataset_context(
            df
        )

        prompt = f"""
You are the question-understanding component
of InsightAI Offline.

Understand the user's question about the dataset.

Do NOT calculate anything.

Do NOT write Python.

Do NOT invent column names.

Return ONLY valid JSON.

DATASET:
{json.dumps(
    context,
    indent=2,
    default=str
)}

USER QUESTION:
{question}

Return exactly:

{{
    "intent": "rows|columns|missing|duplicates|data_types|unique_values|count|sum|average|median|minimum|maximum|group_analysis|percentage|top|bottom|correlation|summary|outliers|unknown",
    "target_column": null,
    "group_column": null,
    "category_value": null,
    "number": null,
    "secondary_column": null
}}

Rules:

- target_column must be an actual dataset column.
- group_column must be an actual dataset column.
- secondary_column must be an actual dataset column.
- Use null if a column cannot be determined.
- number is for requests such as top 5.
- Use summary for broad questions.
- Use unknown when the operation cannot be determined.
"""

        raw = self.llm.generate(
            prompt
        )

        return self._parse_plan(
            raw,
            df
        )

    # ==========================================================
    # PARSE PLAN
    # ==========================================================

    def _parse_plan(
        self,
        response: str,
        df: pd.DataFrame
    ) -> Dict[str, Any]:

        default = {
            "intent": "unknown",
            "target_column": None,
            "group_column": None,
            "category_value": None,
            "number": None,
            "secondary_column": None,
        }

        if not response:

            return default

        response = response.strip()

        response = re.sub(
            r"```json\s*",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"```\s*$",
            "",
            response
        )

        match = re.search(
            r"\{.*\}",
            response,
            flags=re.DOTALL
        )

        if not match:

            return default

        try:

            plan = json.loads(
                match.group(0)
            )

        except json.JSONDecodeError:

            return default

        valid_intents = {
            "rows",
            "columns",
            "missing",
            "duplicates",
            "data_types",
            "unique_values",
            "count",
            "sum",
            "average",
            "median",
            "minimum",
            "maximum",
            "group_analysis",
            "percentage",
            "top",
            "bottom",
            "correlation",
            "summary",
            "outliers",
            "unknown",
        }

        intent = str(
            plan.get(
                "intent",
                "unknown"
            )
        ).lower().strip()

        if intent not in valid_intents:

            intent = "unknown"

        plan["intent"] = intent

        plan[
            "target_column"
        ] = self._match_column(
            plan.get(
                "target_column"
            ),
            df
        )

        plan[
            "group_column"
        ] = self._match_column(
            plan.get(
                "group_column"
            ),
            df
        )

        plan[
            "secondary_column"
        ] = self._match_column(
            plan.get(
                "secondary_column"
            ),
            df
        )

        return plan

    # ==========================================================
    # MATCH COLUMN
    # ==========================================================

    def _match_column(
        self,
        requested: Any,
        df: pd.DataFrame
    ) -> Optional[str]:

        if requested is None:

            return None

        requested = str(
            requested
        ).strip()

        if not requested:

            return None

        normalized = self._normalize(
            requested
        )

        for column in df.columns:

            if self._normalize(
                column
            ) == normalized:

                return column

        requested_tokens = set(
            normalized.split()
        )

        best_column = None
        best_score = 0

        for column in df.columns:

            column_tokens = set(
                self._normalize(
                    column
                ).split()
            )

            if not column_tokens:

                continue

            overlap = len(
                requested_tokens
                & column_tokens
            )

            score = overlap / max(
                len(requested_tokens),
                len(column_tokens)
            )

            if score > best_score:

                best_score = score
                best_column = column

        if best_score >= 0.5:

            return best_column

        return None

    # ==========================================================
    # VALIDATE PLAN
    # ==========================================================

    def _validate_plan(
        self,
        df: pd.DataFrame,
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:

        valid_columns = set(
            df.columns
        )

        for key in [
            "target_column",
            "group_column",
            "secondary_column",
        ]:

            if plan.get(key) not in valid_columns:

                plan[key] = None

        number = plan.get(
            "number"
        )

        try:

            if number is not None:

                number = int(
                    number
                )

                if number <= 0:

                    number = None

                elif number > 50:

                    number = 50

        except (
            TypeError,
            ValueError
        ):

            number = None

        plan["number"] = number

        return plan

    # ==========================================================
    # EXECUTE PLAN
    # ==========================================================

    def _execute_plan(
        self,
        df: pd.DataFrame,
        plan: Dict[str, Any],
        question: str
    ) -> Optional[Dict[str, Any]]:

        intent = plan.get(
            "intent"
        )

        target = plan.get(
            "target_column"
        )

        group = plan.get(
            "group_column"
        )

        secondary = plan.get(
            "secondary_column"
        )

        category = plan.get(
            "category_value"
        )

        number = plan.get(
            "number"
        )

        if intent == "rows":

            return {
                "type": "rows",
                "rows": int(
                    len(df)
                )
            }

        if intent == "columns":

            return {
                "type": "columns",
                "columns": list(
                    df.columns
                )
            }

        if intent == "missing":

            return self._missing_values(
                df
            )

        if intent == "duplicates":

            return {
                "type": "duplicates",
                "duplicates": int(
                    df.duplicated().sum()
                )
            }

        if intent == "data_types":

            return {
                "type": "data_types",
                "data_types": {
                    str(column): str(
                        df[column].dtype
                    )
                    for column in df.columns
                }
            }

        if intent == "unique_values":

            if not target:

                return None

            values = (
                df[target]
                .dropna()
                .unique()
                .tolist()
            )

            return {
                "type": "unique_values",
                "column": target,
                "count": len(values),
                "values": values[:100]
            }

        if intent == "count":

            if not target:

                return {
                    "type": "rows",
                    "rows": int(
                        len(df)
                    )
                }

            return {
                "type": "count",
                "column": target,
                "count": int(
                    df[target].count()
                )
            }

        if intent == "sum":

            target = self._ensure_numeric_column(
                df,
                target
            )

            if not target:

                return None

            return {
                "type": "sum",
                "column": target,
                "value": self._clean_number(
                    df[target].sum()
                )
            }

        if intent == "average":

            target = self._ensure_numeric_column(
                df,
                target
            )

            if not target:

                return None

            return {
                "type": "average",
                "column": target,
                "value": self._clean_number(
                    df[target].mean()
                )
            }

        if intent == "median":

            target = self._ensure_numeric_column(
                df,
                target
            )

            if not target:

                return None

            return {
                "type": "median",
                "column": target,
                "value": self._clean_number(
                    df[target].median()
                )
            }

        if intent == "minimum":

            target = self._ensure_numeric_column(
                df,
                target
            )

            if not target:

                return None

            return {
                "type": "minimum",
                "column": target,
                "value": self._clean_number(
                    df[target].min()
                )
            }

        if intent == "maximum":

            target = self._ensure_numeric_column(
                df,
                target
            )

            if not target:

                return None

            return {
                "type": "maximum",
                "column": target,
                "value": self._clean_number(
                    df[target].max()
                )
            }

        if intent == "group_analysis":

            return self._group_analysis(
                df,
                target,
                group
            )

        if intent == "percentage":

            return self._percentage_analysis(
                df,
                target,
                category
            )

        if intent in {
            "top",
            "bottom"
        }:

            return self._ranking_analysis(
                df,
                target,
                group,
                number,
                intent
            )

        if intent == "correlation":

            return self._correlation_analysis(
                df,
                target,
                secondary
            )

        if intent == "outliers":

            return self._outlier_analysis(
                df,
                target
            )

        if intent == "summary":

            return self._summary_analysis(
                df
            )

        return None

    # ==========================================================
    # NUMERIC COLUMN
    # ==========================================================

    def _ensure_numeric_column(
        self,
        df: pd.DataFrame,
        column: Optional[str]
    ) -> Optional[str]:

        if column and column in df.columns:

            if pd.api.types.is_numeric_dtype(
                df[column]
            ):

                return column

        numeric = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        if numeric:

            return numeric[0]

        return None

    # ==========================================================
    # NUMBER CLEANING
    # ==========================================================

    def _clean_number(
        self,
        value
    ):

        try:

            value = float(
                value
            )

            if value.is_integer():

                return int(
                    value
                )

            return round(
                value,
                2
            )

        except Exception:

            return value

    # ==========================================================
    # MISSING
    # ==========================================================

    def _missing_values(
        self,
        df: pd.DataFrame
    ) -> Dict[str, Any]:

        missing = df.isna().sum()

        columns = {
            str(column): int(value)
            for column, value
            in missing.items()
            if value > 0
        }

        return {
            "type": "missing",
            "columns": columns,
            "total": int(
                missing.sum()
            )
        }

    # ==========================================================
    # GROUP ANALYSIS
    # ==========================================================

    def _group_analysis(
        self,
        df: pd.DataFrame,
        target: Optional[str],
        group: Optional[str]
    ) -> Optional[Dict[str, Any]]:

        if not group:

            categorical = list(
                df.select_dtypes(
                    include=[
                        "object",
                        "category"
                    ]
                ).columns
            )

            if categorical:

                group = categorical[0]

        if not group:

            return None

        target = (
            self._ensure_numeric_column(
                df,
                target
            )
            if target
            else None
        )

        if target:

            grouped = (
                df.groupby(
                    group,
                    dropna=False
                )[target]
                .agg([
                    "count",
                    "sum",
                    "mean",
                    "min",
                    "max"
                ])
                .round(2)
                .reset_index()
            )

            return {
                "type": "group_analysis",
                "group_column": group,
                "target_column": target,
                "results": grouped.to_dict(
                    orient="records"
                )
            }

        grouped = (
            df[group]
            .value_counts(
                dropna=False
            )
            .reset_index()
        )

        grouped.columns = [
            group,
            "count"
        ]

        return {
            "type": "group_count",
            "group_column": group,
            "results": grouped.to_dict(
                orient="records"
            )
        }

    # ==========================================================
    # PERCENTAGE
    # ==========================================================

    def _percentage_analysis(
        self,
        df: pd.DataFrame,
        target: Optional[str],
        category: Any
    ) -> Optional[Dict[str, Any]]:

        if not target:

            return None

        values = df[
            target
        ].dropna()

        if values.empty:

            return None

        if category is not None:

            category_text = str(
                category
            ).strip().lower()

            matches = (
                values.astype(str)
                .str.lower()
                == category_text
            )

            count = int(
                matches.sum()
            )

            percentage = (
                count
                / len(values)
            ) * 100

            return {
                "type": "percentage",
                "column": target,
                "category": category,
                "count": count,
                "total": len(values),
                "percentage": round(
                    percentage,
                    2
                )
            }

        distribution = (
            values.value_counts(
                normalize=True
            )
            .mul(100)
            .round(2)
        )

        return {
            "type": "percentage_distribution",
            "column": target,
            "results": distribution.to_dict()
        }

    # ==========================================================
    # TOP / BOTTOM
    # ==========================================================

    def _ranking_analysis(
        self,
        df: pd.DataFrame,
        target: Optional[str],
        group: Optional[str],
        number: Any,
        direction: str
    ) -> Optional[Dict[str, Any]]:

        limit = number or 5

        try:

            limit = int(
                limit
            )

        except (
            TypeError,
            ValueError
        ):

            limit = 5

        limit = max(
            1,
            min(limit, 50)
        )

        if group:

            target = self._ensure_numeric_column(
                df,
                target
            )

            if not target:

                return None

            grouped = (
                df.groupby(
                    group,
                    dropna=False
                )[target]
                .sum()
                .sort_values(
                    ascending=(
                        direction == "bottom"
                    )
                )
                .head(limit)
                .round(2)
            )

            return {
                "type": direction,
                "column": target,
                "group_column": group,
                "results": grouped.to_dict()
            }

        target = self._ensure_numeric_column(
            df,
            target
        )

        if not target:

            return None

        sorted_df = df.sort_values(
            target,
            ascending=(
                direction == "bottom"
            )
        )

        result = sorted_df[
            [target]
        ].head(limit)

        return {
            "type": direction,
            "column": target,
            "results": result[
                target
            ].tolist()
        }

    # ==========================================================
    # CORRELATION
    # ==========================================================

    def _correlation_analysis(
        self,
        df: pd.DataFrame,
        target: Optional[str],
        secondary: Optional[str]
    ) -> Optional[Dict[str, Any]]:

        numeric = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        if target not in numeric:

            target = (
                numeric[0]
                if numeric
                else None
            )

        if secondary not in numeric:

            secondary = (
                numeric[1]
                if len(numeric) > 1
                else None
            )

        if not target or not secondary:

            return None

        value = df[
            target
        ].corr(
            df[secondary]
        )

        if pd.isna(value):

            return None

        return {
            "type": "correlation",
            "column_1": target,
            "column_2": secondary,
            "value": round(
                float(value),
                4
            )
        }

    # ==========================================================
    # OUTLIERS
    # ==========================================================

    def _outlier_analysis(
        self,
        df: pd.DataFrame,
        target: Optional[str]
    ) -> Optional[Dict[str, Any]]:

        target = self._ensure_numeric_column(
            df,
            target
        )

        if not target:

            return None

        series = df[
            target
        ].dropna()

        if series.empty:

            return None

        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1

        lower = q1 - (
            1.5 * iqr
        )

        upper = q3 + (
            1.5 * iqr
        )

        outliers = series[
            (series < lower)
            | (series > upper)
        ]

        return {
            "type": "outliers",
            "column": target,
            "count": int(
                len(outliers)
            ),
            "lower_bound": round(
                float(lower),
                2
            ),
            "upper_bound": round(
                float(upper),
                2
            ),
            "values": outliers.tolist()[
                :50
            ]
        }

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def _summary_analysis(
        self,
        df: pd.DataFrame
    ) -> Dict[str, Any]:

        numeric = df.select_dtypes(
            include="number"
        )

        categorical = df.select_dtypes(
            include=[
                "object",
                "category"
            ]
        )

        return {
            "type": "summary",
            "rows": int(
                len(df)
            ),
            "columns": int(
                len(df.columns)
            ),
            "numeric_columns": list(
                numeric.columns
            ),
            "categorical_columns": list(
                categorical.columns
            ),
            "missing_values": int(
                df.isna().sum().sum()
            ),
            "duplicates": int(
                df.duplicated().sum()
            )
        }

    # ==========================================================
    # SIMPLE RESULT CHECK
    # ==========================================================

    def _is_simple_result(
        self,
        result: Dict[str, Any]
    ) -> bool:

        return result.get(
            "type"
        ) in {
            "rows",
            "columns",
            "missing",
            "duplicates",
            "data_types",
            "unique_values",
            "count",
            "sum",
            "average",
            "median",
            "minimum",
            "maximum",
            "percentage",
            "percentage_distribution",
            "top",
            "bottom",
            "correlation",
            "outliers",
        }

    # ==========================================================
    # FORMAT RESULT
    # ==========================================================

    def _format_result(
        self,
        result: Dict[str, Any]
    ) -> str:

        result_type = result.get(
            "type"
        )

        if result_type == "rows":

            return (
                f"The dataset contains "
                f"{result['rows']:,} rows."
            )

        if result_type == "columns":

            columns = result[
                "columns"
            ]

            return (
                "The dataset contains "
                f"{len(columns)} columns:\n\n"
                + "\n".join(
                    f"{i + 1}. {column}"
                    for i, column
                    in enumerate(columns)
                )
            )

        if result_type == "missing":

            if result["total"] == 0:

                return (
                    "The dataset contains "
                    "no missing values."
                )

            lines = [
                f"• {column}: {count}"
                for column, count
                in result[
                    "columns"
                ].items()
            ]

            return (
                f"The dataset contains "
                f"{result['total']:,} "
                "missing values.\n\n"
                + "\n".join(lines)
            )

        if result_type == "duplicates":

            return (
                f"The dataset contains "
                f"{result['duplicates']:,} "
                "duplicate rows."
            )

        if result_type == "data_types":

            lines = [
                f"• {column}: {dtype}"
                for column, dtype
                in result[
                    "data_types"
                ].items()
            ]

            return (
                "Column data types:\n\n"
                + "\n".join(lines)
            )

        if result_type == "unique_values":

            values = result[
                "values"
            ]

            preview = ", ".join(
                str(value)
                for value in values[:30]
            )

            if len(values) > 30:

                preview += ", ..."

            return (
                f"{result['column']} contains "
                f"{result['count']:,} "
                "unique values.\n\n"
                f"Values: {preview}"
            )

        if result_type == "count":

            return (
                f"{result['column']} contains "
                f"{result['count']:,} "
                "non-missing values."
            )

        if result_type == "sum":

            return (
                f"The total {result['column']} "
                f"is {result['value']:,}."
            )

        if result_type == "average":

            return (
                f"The average {result['column']} "
                f"is {result['value']:,}."
            )

        if result_type == "median":

            return (
                f"The median {result['column']} "
                f"is {result['value']:,}."
            )

        if result_type == "minimum":

            return (
                f"The minimum {result['column']} "
                f"is {result['value']:,}."
            )

        if result_type == "maximum":

            return (
                f"The maximum {result['column']} "
                f"is {result['value']:,}."
            )

        if result_type == "percentage":

            return (
                f"{result['category']} accounts for "
                f"{result['percentage']}% of "
                f"{result['column']} "
                f"({result['count']} out of "
                f"{result['total']} records)."
            )

        if result_type == "percentage_distribution":

            lines = [
                f"• {value}: {percentage}%"
                for value, percentage
                in result[
                    "results"
                ].items()
            ]

            return (
                f"Percentage distribution for "
                f"{result['column']}:\n\n"
                + "\n".join(lines)
            )

        if result_type == "top":

            if result.get(
                "group_column"
            ):

                lines = [
                    f"• {key}: {value:,}"
                    for key, value
                    in result[
                        "results"
                    ].items()
                ]

                return (
                    f"Top {len(lines)} "
                    f"{result['group_column']} "
                    f"by {result['column']}:\n\n"
                    + "\n".join(lines)
                )

            values = result[
                "results"
            ]

            return (
                f"Top {len(values)} values "
                f"for {result['column']}:\n\n"
                + "\n".join(
                    f"• {value:,}"
                    for value in values
                )
            )

        if result_type == "bottom":

            if result.get(
                "group_column"
            ):

                lines = [
                    f"• {key}: {value:,}"
                    for key, value
                    in result[
                        "results"
                    ].items()
                ]

                return (
                    f"Bottom {len(lines)} "
                    f"{result['group_column']} "
                    f"by {result['column']}:\n\n"
                    + "\n".join(lines)
                )

            values = result[
                "results"
            ]

            return (
                f"Bottom {len(values)} values "
                f"for {result['column']}:\n\n"
                + "\n".join(
                    f"• {value:,}"
                    for value in values
                )
            )

        if result_type == "correlation":

            value = result[
                "value"
            ]

            if value > 0:

                direction = "positive"

            elif value < 0:

                direction = "negative"

            else:

                direction = "no"

            return (
                f"The correlation between "
                f"{result['column_1']} and "
                f"{result['column_2']} is "
                f"{value} "
                f"({direction} correlation)."
            )

        if result_type == "outliers":

            if result["count"] == 0:

                return (
                    f"No outliers were detected "
                    f"in {result['column']} using "
                    "the IQR method."
                )

            return (
                f"{result['count']} outlier(s) were "
                f"detected in {result['column']} "
                "using the IQR method.\n\n"
                f"Lower bound: "
                f"{result['lower_bound']}\n"
                f"Upper bound: "
                f"{result['upper_bound']}\n"
                f"Outlier values: "
                f"{result['values']}"
            )

        return str(
            result
        )

    # ==========================================================
    # EXPLAIN COMPLEX RESULT
    # ==========================================================

    def _explain_result(
        self,
        question: str,
        result: Dict[str, Any]
    ) -> str:

        prompt = f"""
You are InsightAI, an offline data-analysis assistant.

Answer the user's question using ONLY the verified
Pandas result below.

Do not invent numbers.

Do not invent columns.

Do not make causal claims.

Give a concise and useful interpretation.

USER QUESTION:
{question}

VERIFIED PANDAS RESULT:
{json.dumps(
    result,
    indent=2,
    default=str
)}

Return only the answer.
"""

        try:

            answer = self.llm.generate(
                prompt
            )

            if answer:

                return answer.strip()

        except Exception as e:

            print(
                "Explanation error:",
                repr(e)
            )

        return self._format_result(
            result
        )

    # ==========================================================
    # FALLBACK
    # ==========================================================

    def _fallback_answer(
        self,
        df: pd.DataFrame,
        question: str
    ) -> str:

        columns = ", ".join(
            str(column)
            for column in df.columns
        )

        return (
            "I couldn't determine a reliable analysis "
            "for that question from the current dataset.\n\n"
            f"Available columns: {columns}\n\n"
            "Try asking about totals, counts, missing values, "
            "groups, top/bottom values, percentages, "
            "correlations, or unusual values."
        )