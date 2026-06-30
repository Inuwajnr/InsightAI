import pandas as pd


class DataQuality:

    def evaluate(self, df):

        rows = len(df)

        columns = len(df.columns)

        missing = int(df.isna().sum().sum())

        duplicates = int(df.duplicated().sum())

        constant_columns = 0

        for col in df.columns:

            if df[col].nunique(dropna=False) == 1:
                constant_columns += 1

        score = 100

        score -= min(missing, 30)

        score -= duplicates * 5

        score -= constant_columns * 5

        score = max(score, 0)

        recommendations = []

        # ----------------------------------
        # Missing Values
        # ----------------------------------

        if missing > 0:

            recommendations.append(
                f"⚠ {missing} missing values detected. Consider filling or removing them."
            )

        else:

            recommendations.append(
                "✓ No missing values detected."
            )

        # ----------------------------------
        # Duplicate Rows
        # ----------------------------------

        if duplicates > 0:

            recommendations.append(
                f"⚠ {duplicates} duplicate rows found."
            )

        else:

            recommendations.append(
                "✓ No duplicate rows found."
            )

        # ----------------------------------
        # Constant Columns
        # ----------------------------------

        if constant_columns > 0:

            recommendations.append(
                f"⚠ {constant_columns} constant column(s) detected."
            )

        else:

            recommendations.append(
                "✓ No constant columns detected."
            )

        # ----------------------------------
        # Overall Status
        # ----------------------------------

        if (
            missing == 0
            and duplicates == 0
            and constant_columns == 0
        ):

            recommendations.append(
                "🚀 Dataset is ready for analysis."
            )

        return {

            "score": score,

            "rows": rows,

            "columns": columns,

            "missing": missing,

            "duplicates": duplicates,

            "constant_columns": constant_columns,

            "recommendations": recommendations

        }