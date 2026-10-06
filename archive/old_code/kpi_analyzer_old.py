import pandas as pd


class KPIAnalyzer:

    BUSINESS_COLUMNS = {
        "sales": ["sales", "revenue", "amount", "total_sales"],
        "profit": ["profit", "net_profit"],
        "orders": ["order_id", "orderid", "invoice", "invoice_id"],
        "customers": ["customer", "customer_id", "customerid"]
    }

    def generate(self, df):

        cols = {c.lower(): c for c in df.columns}

        kpis = []

        # -------------------------
        # Sales
        # -------------------------
        sales_col = self._find_column(cols, self.BUSINESS_COLUMNS["sales"])

        if sales_col:
            total_sales = pd.to_numeric(
                df[sales_col],
                errors="coerce"
            ).sum()

            kpis.append((
                "Total Sales",
                self.format_number(total_sales)
            ))

        # -------------------------
        # Profit
        # -------------------------
        profit_col = self._find_column(cols, self.BUSINESS_COLUMNS["profit"])

        if profit_col:
            total_profit = pd.to_numeric(
                df[profit_col],
                errors="coerce"
            ).sum()

            kpis.append((
                "Total Profit",
                self.format_number(total_profit)
            ))

        # -------------------------
        # Orders
        # -------------------------
        order_col = self._find_column(cols, self.BUSINESS_COLUMNS["orders"])

        if order_col:
            kpis.append((
                "Orders",
                f"{df[order_col].nunique():,}"
            ))

        # -------------------------
        # Customers
        # -------------------------
        customer_col = self._find_column(cols, self.BUSINESS_COLUMNS["customers"])

        if customer_col:
            kpis.append((
                "Customers",
                f"{df[customer_col].nunique():,}"
            ))

        return kpis

    def _find_column(self, cols, names):

        for n in names:
            if n in cols:
                return cols[n]

        return None

    def format_number(self, value):

        if value >= 1_000_000_000:
            return f"₦{value/1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"₦{value/1_000_000:.2f}M"

        if value >= 1_000:
            return f"₦{value/1_000:.2f}K"

        return f"₦{value:,.2f}"