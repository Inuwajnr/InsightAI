import pandas as pd


class SmartKPIEngine:

    # ---------------------------------
    # Keywords
    # ---------------------------------

    MONEY_WORDS = [
        "sales",
        "revenue",
        "profit",
        "income",
        "amount",
        "balance",
        "cost",
        "price"
    ]

    ID_WORDS = [
        "id",
        "customer",
        "patient",
        "student",
        "employee",
        "order",
        "invoice"
    ]

    DATE_WORDS = [
        "date",
        "time",
        "year",
        "month"
    ]

    AVERAGE_WORDS = [
        "age",
        "score",
        "rating",
        "quantity",
        "discount",
        "salary",
        "price",
        "cost"
    ]


    # ---------------------------------
    # KPI Scoring Engine
    # ---------------------------------

    def calculate_score(self, column_name, column):

        score = 0

        name = column_name.lower()

        # ----------------------------
        # Money Columns
        # ----------------------------

        if any(word in name for word in self.MONEY_WORDS):
            score += 150

        # ----------------------------
        # ID Columns
        # ----------------------------

        if any(word in name for word in self.ID_WORDS):
            score += 80

        # ----------------------------
        # Business Entity Bonus
        # ----------------------------

        if "customer" in name:
            score += 30

        if "order" in name:
            score += 30

        if "invoice" in name:
            score += 30

        if "product" in name:
            score += 20

        if "employee" in name:
            score += 20

        if "student" in name:
            score += 20

        if "patient" in name:
            score += 20

        # ----------------------------
        # Date Columns
        # ----------------------------

        if any(word in name for word in self.DATE_WORDS):
            score += 40

        # ----------------------------
        # Average Columns
        # ----------------------------

        if any(word in name for word in self.AVERAGE_WORDS):
            score += 25

        # ----------------------------
        # High Cardinality Bonus
        # ----------------------------

        try:

            unique_ratio = column.nunique() / len(column)

            if unique_ratio > 0.70:
                score += 15

            elif unique_ratio > 0.40:
                score += 10

        except Exception:
            pass

        return score

    # ---------------------------------
    # Main Engine
    # ---------------------------------

    def generate(self, df):

        kpis = []

        columns = list(df.columns)

        numeric_cols = list(
            df.select_dtypes(include="number").columns
        )

        # ---------------------------------
        # ID Columns
        # ---------------------------------

        for col in columns:

            lower = col.lower()

            if any(word in lower for word in self.ID_WORDS):

                score = self.calculate_score(
                    col,
                    df[col]
                )

                title = self.clean_title(col)

                value = f"{df[col].nunique():,}"

                kpis.append({

                    "title": title,

                    "value": value,

                    "score": score

                })

        # ---------------------------------
        # Numeric Columns
        # ---------------------------------

        for col in numeric_cols:

            series = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            lower = col.lower()

            # -----------------------
            # Money Columns
            # -----------------------

            if any(word in lower for word in self.MONEY_WORDS):

                
                score = self.calculate_score(
                    col,
                    df[col]
                )

                value = self.format_number(
                    series.sum()
                )

                kpis.append({

                    "title": f"Total {col}",

                    "value": value,

                    "score": score

                })

                continue

            # -----------------------
            # Generic Numeric
            # -----------------------

            score = self.calculate_score(
                col,
                df[col]
            )

            value = self.format_number(
                series.mean()
            )

            kpis.append({

                "title": f"Average {col}",

                "value": value,

                "score": score

            })

        # ---------------------------------
        # Dataset KPIs
        # ---------------------------------

        kpis.append({

            "title": "Rows",

            "value": f"{len(df):,}",

            "score": 20

        })

        kpis.append({

            "title": "Columns",

            "value": str(len(df.columns)),

            "score": 15

        })

        # ---------------------------------
        # Remove duplicates
        # ---------------------------------

        unique = {}

        for item in kpis:

            unique[item["title"]] = item

        kpis = list(unique.values())

        # ---------------------------------
        # Sort by score
        # ---------------------------------

        kpis.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        # ---------------------------------
        # Return Top 4
        # ---------------------------------

        return [

            (k["title"], k["value"])

            for k in kpis[:4]

        ]

    # ---------------------------------
    # Clean Titles
    # ---------------------------------

    def clean_title(self, name):

        lower = name.lower()

        if "customer" in lower:
            return "Customers"

        if "order" in lower:
            return "Orders"

        if "product" in lower:
            return "Products"

        if "invoice" in lower:
            return "Invoices"

        if "employee" in lower:
            return "Employees"

        if "patient" in lower:
            return "Patients"

        if "student" in lower:
            return "Students"

        if "location" in lower:
            return "Locations"

        return name.replace("_", " ").title()

    # ---------------------------------
    # Number Formatter
    # ---------------------------------

    def format_number(self, value):

        if pd.isna(value):

            return "-"

        if abs(value) >= 1_000_000_000:

            return f"{value/1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:

            return f"{value/1_000_000:.2f}M"

        if abs(value) >= 1_000:

            return f"{value/1_000:.2f}K"

        return f"{value:,.2f}"