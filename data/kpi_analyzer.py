import pandas as pd


class KPIAnalyzer:

    def generate(self, df):

        kpis = []

        numeric_cols = list(
            df.select_dtypes(include="number").columns
        )

        categorical_cols = list(
            df.select_dtypes(exclude="number").columns
        )

        # ---------------------------------
        # Rows
        # ---------------------------------

        kpis.append((
            "Rows",
            f"{len(df):,}"
        ))

        # ---------------------------------
        # Columns
        # ---------------------------------

        kpis.append((
            "Columns",
            str(len(df.columns))
        ))

        # ---------------------------------
        # Business KPIs
        # ---------------------------------

        business_kpis = self._business_kpis(df)

        if business_kpis:

            return business_kpis

        # ---------------------------------
        # Generic numeric KPIs
        # ---------------------------------

        if numeric_cols:

            primary_col = numeric_cols[0]

            values = pd.to_numeric(
                df[primary_col],
                errors="coerce"
            ).dropna()

            if len(values):

                kpis.append((
                    f"Avg {primary_col}",
                    self.format_number(
                        values.mean()
                    )
                ))

                kpis.append((
                    f"Max {primary_col}",
                    self.format_number(
                        values.max()
                    )
                ))

        return kpis[:4]

    def _business_kpis(self, df):

        cols = {
            c.lower(): c
            for c in df.columns
        }

        kpis = []

        sales_cols = [
            "sales",
            "revenue",
            "amount",
            "total_sales"
        ]

        profit_cols = [
            "profit",
            "net_profit"
        ]

        order_cols = [
            "order_id",
            "orderid",
            "invoice",
            "invoice_id"
        ]

        customer_cols = [
            "customer",
            "customer_id",
            "customerid"
        ]

        sales = self._find_column(
            cols,
            sales_cols
        )

        profit = self._find_column(
            cols,
            profit_cols
        )

        orders = self._find_column(
            cols,
            order_cols
        )

        customers = self._find_column(
            cols,
            customer_cols
        )

        if orders:

            kpis.append((
                "Orders",
                f"{df[orders].nunique():,}"
            ))

        if profit:

            total = pd.to_numeric(
                df[profit],
                errors="coerce"
            ).sum()

            kpis.append((
                "Total Profit",
                self.format_number(total)
            ))

        if customers:

            kpis.append((
                "Customers",
                f"{df[customers].nunique():,}"
            ))

        if sales:

            total = pd.to_numeric(
                df[sales],
                errors="coerce"
            ).sum()

            kpis.append((
                "Total Sales",
                self.format_number(total)
            ))

        return kpis

    def _find_column(self, cols, names):

        for name in names:

            if name in cols:

                return cols[name]

        return None

    def format_number(self, value):

        if abs(value) >= 1_000_000_000:

            return f"{value/1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:

            return f"{value/1_000_000:.2f}M"

        if abs(value) >= 1_000:

            return f"{value/1_000:.2f}K"

        return f"{value:,.2f}"