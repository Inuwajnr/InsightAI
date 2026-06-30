import pandas as pd
from matplotlib.ticker import FuncFormatter


class ChartGenerator:

    # ==========================================
    # Prepare Data
    # ==========================================

    def _prepare_grouped_data(self, df, x_col, y_col):

        data = df.copy()

        data[y_col] = pd.to_numeric(
            data[y_col],
            errors="coerce"
        )

        data = data.dropna(
            subset=[x_col, y_col]
        )

        grouped = (
            data.groupby(x_col)[y_col]
            .sum()
            .sort_values(ascending=False)
        )

        return grouped

    # ==========================================
    # Common Style
    # ==========================================

    def _style_chart(self, ax, title, xlabel="", ylabel=""):

        ax.set_title(
            title,
            fontsize=18,
            fontweight="bold",
            pad=18
        )

        ax.set_xlabel(
            xlabel,
            fontsize=12,
            fontweight="bold"
        )

        ax.set_ylabel(
            ylabel,
            fontsize=12,
            fontweight="bold"
        )

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.30
        )

        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.tick_params(
            axis="x",
            labelrotation=20,
            labelsize=10
        )

        ax.tick_params(
            axis="y",
            labelsize=10
        )

        # Format numbers with commas
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, p: f"{x:,.0f}")
        )

    # ==========================================
    # Bar Chart
    # ==========================================

    def bar_chart(
        self,
        ax,
        df,
        x_col,
        y_col,
        top_n="10"
    ):

        ax.clear()

        grouped = self._prepare_grouped_data(
            df,
            x_col,
            y_col
        )

        if grouped.empty:
            raise ValueError("No data available.")

        # Limit to Top N categories
        if top_n != "All":
            grouped = grouped.head(int(top_n))

        # Many categories -> Horizontal Bar
        if len(grouped) > 8:

            bars = ax.barh(
                grouped.index.astype(str),
                grouped.values,
                color="#3B82F6",
                height=0.65
            )

            ax.invert_yaxis()

            ax.set_xlabel(
                y_col,
                fontsize=12,
                fontweight="bold"
            )

            ax.set_ylabel(
                x_col,
                fontsize=12,
                fontweight="bold"
            )

            ax.set_title(
                f"Total {y_col} by {x_col}",
                fontsize=18,
                fontweight="bold",
                pad=20
            )

            ax.xaxis.set_major_formatter(
                FuncFormatter(lambda x, p: f"{x:,.0f}")
            )

            ax.bar_label(
                bars,
                fmt="%.0f",
                padding=5,
                fontsize=9,
                fontweight='bold'
            )

        # Few categories -> Vertical Bar
        else:

            bars = ax.bar(
                grouped.index.astype(str),
                grouped.values,
                color="#3B82F6",
                width=0.65
            )

            ax.set_xlabel(
                x_col,
                fontsize=12,
                fontweight="bold"
            )

            ax.set_ylabel(
                y_col,
                fontsize=12,
                fontweight="bold"
            )

            ax.set_title(
                f"Total {y_col} by {x_col}",
                fontsize=18,
                fontweight="bold",
                pad=20
            )

            ax.tick_params(
                axis="x",
                rotation=35
            )

            ax.yaxis.set_major_formatter(
                FuncFormatter(lambda x, p: f"{x:,.0f}")
            )

            ax.bar_label(
                bars,
                fmt="%.0f",
                padding=3,
                fontsize=9,
                fontweight= 'bold'
            )

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.figure.tight_layout()

    # ==========================================
    # Column Chart
    # ==========================================

    def column_chart(
            self,ax,df,x_col,y_col,top_n="10"):
        
        
        ax.clear()

        if top_n != "All":
            grouped = grouped.head(int(top_n))

        if grouped.empty:
            raise ValueError("No data available.")

        bars = ax.bar(
            grouped.index.astype(str),
            grouped.values,
            color="#10B981",
            width=0.65
        )

        ax.set_title(
            f"Total {y_col} by {x_col}",
            fontsize=18,
            fontweight="bold"
        )

        ax.set_xlabel(
            x_col,
            fontsize=12,
            fontweight="bold"
        )

        ax.set_ylabel(
            y_col,
            fontsize=12,
            fontweight="bold"
        )

        ax.tick_params(
            axis="x",
            rotation=35
        )

        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, p: f"{x:,.0f}")
        )

        ax.bar_label(
            bars,
            fmt="%.0f",
            padding=3,
            fontsize=9,
            fontweight='bold'
        )

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.figure.tight_layout()
    # ==========================================
    # Line Chart
    # ==========================================

    def line_chart(self, ax, df, x_col, y_col, top_n ="10"):

        ax.clear()

        if top_n != "All":
            grouped = grouped.head(int(top_n))

        grouped = self._prepare_grouped_data(
            df,
            x_col,
            y_col
        )

        ax.plot(
            grouped.index,
            grouped.values,
            marker="o",
            linewidth=3,
            color="#3B82F6"
        )

        for x, y in zip(grouped.index, grouped.values):

            ax.text(
                x,
                y,
                f"{y:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        self._style_chart(
            ax,
            f"Trend of {y_col}",
            x_col,
            y_col
        )

    # ==========================================
    # Scatter Plot
    # ==========================================

    def scatter_plot(self, ax, df, x_col, y_col):

        ax.clear()

        data = df.copy()

        data[x_col] = pd.to_numeric(
            data[x_col],
            errors="coerce"
        )

        data[y_col] = pd.to_numeric(
            data[y_col],
            errors="coerce"
        )

        data = data.dropna(
            subset=[x_col, y_col]
        )

        if data.empty:
            raise ValueError(
                "Scatter Plot requires two numeric columns."
            )

        ax.scatter(
            data[x_col],
            data[y_col],
            alpha=0.7,
            color="#3B82F6"
        )

        self._style_chart(
            ax,
            f"{y_col} vs {x_col}",
            x_col,
            y_col
        )

    # ==========================================
    # Pie Chart
    # ==========================================

    def pie_chart(self, ax, df, category_col):

        ax.clear()

        counts = (
            df[category_col]
            .value_counts()
            .head(8)
        )
        
        counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=90,
            ax=ax
        )

        ax.set_ylabel("")

        ax.set_title(
            f"{category_col} Distribution",
            fontsize=18,
            fontweight="bold"
        )

    # ==========================================
    # Histogram
    # ==========================================

    def histogram(self, ax, df, numeric_col):

        ax.clear()

        data = pd.to_numeric(
            df[numeric_col],
            errors="coerce"
        ).dropna()

        if data.empty:
            raise ValueError(
                "Selected column contains no numeric values."
            )

        ax.hist(
            data,
            bins=20,
            color="#3B82F6",
            edgecolor="black"
        )

        self._style_chart(
            ax,
            f"{numeric_col} Distribution",
            numeric_col,
            "Frequency"
        )