import matplotlib.pyplot as plt
import pandas as pd


class PivotChart:

    def create_chart(self, pivot_df, value_column, chart_type, row_fields):

        data = pivot_df.reset_index()
        print("\n===== PIVOT DATA =====")
        print(data)

        print("\n===== COLUMNS =====")
        print(data.columns.tolist())

        print("\nSelected Value Column:")
        print(value_column)

        print("\nSeries being plotted:")
        print(data[value_column])

        if row_fields:
            x = data[row_fields].astype(str).agg(" - ".join, axis=1)
        else:
            x = data.iloc[:, 0].astype(str)
        y = pd.to_numeric(
                data[value_column],
                errors="coerce"
            ).fillna(0)
        plt.figure(figsize=(10, 6))

        # ==========================
        # BAR CHART (Horizontal)
        # ==========================

        if chart_type == "Bar":

            bars = plt.barh(
                x,
                y,
                color="#3B82F6"
            )

            # Display the aggregated value above each bar
            for bar in bars:

                width = bar.get_width()

                plt.text(
                    width + (max(y) * 0.01),           # Slightly to the right of the bar
                    bar.get_y() + bar.get_height()/2,  # Middle of the bar
                    f"{width:,.2f}",
                    ha="left",
                    va="center",
                    fontsize=10,
                    fontweight="bold"
                )

        # ==========================
        # COLUMN CHART (Vertical))
        # ==========================

        elif chart_type == "Column":

            bars = plt.bar(
                x,
                y,
                color="#10B981"
            )

            # Display the aggregated value above each bar
            for bar in bars:

                height = bar.get_height()

                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{height:,.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold"
                )

        # ==========================
        # LINE CHART
        # ==========================

        elif chart_type == "Line":

            plt.plot(
                x,
                y,
                marker="o",
                linewidth=3
            )

            # Display value on each point
            for i, value in enumerate(y):

                plt.text(
                    x[i],
                    value,
                    f"{value:,.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold"
                )
        # ==========================
        # PIE CHART
        # ==========================

        elif chart_type == "Pie":

            plt.pie(
                y,
                labels=x,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title(value_column)
            plt.tight_layout()
            plt.show()
            return

        # ==========================
        # COMMON SETTINGS
        # ==========================

        plt.title(f"{value_column} by {data.columns[0]}")
        plt.xlabel(data.columns[0])
        plt.ylabel(value_column)

        plt.xticks(rotation=30)
        if chart_type == "Bar":
            plt.xlim(0, max(y) * 1.15)

        elif chart_type == "Column":
            plt.ylim(0, max(y) * 1.10)
        plt.tight_layout()

        plt.show()