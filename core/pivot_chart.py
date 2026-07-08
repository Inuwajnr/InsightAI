import matplotlib.pyplot as plt
import pandas as pd


class PivotChart:

    def create_chart(self, pivot_df, value_column, chart_type, row_fields,x_axis):

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
        # STACKED COLUMN CHART 
        # ==========================

        elif chart_type == "Stacked Column":
            
            x = data.iloc[:, 0].astype(str)

            numeric_data = data.select_dtypes(include="number")

            bottom = [0] * len(x)

            for column in numeric_data.columns:

                bars = plt.bar(
                    x,
                    numeric_data[column],
                    bottom=bottom,
                    label=column
                )

                # Display labels inside each stack
                for bar in bars:

                    height = bar.get_height()

                    # Skip labels for zero values
                    if height == 0:
                        continue

                    plt.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_y() + height / 2,
                        f"{height:,.2f}",
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="white",
                        fontweight="bold"
                    )

                # Update bottom for next stack
                bottom = [
                    b + v
                    for b, v in zip(bottom, numeric_data[column])
                ]

            plt.legend(title="Series")


        # ==========================
        # 100% STACKED COLUMN CHART
        # ==========================

        elif chart_type == "100% Stacked Column":

            x = data.iloc[:, 0].astype(str)

            numeric_data = data.select_dtypes(include="number")

            # Convert each row to percentages
            percent_data = numeric_data.div(
                numeric_data.sum(axis=1),
                axis=0
            ) * 100

            bottom = [0] * len(x)

            for column in percent_data.columns:

                bars = plt.bar(
                    x,
                    percent_data[column],
                    bottom=bottom,
                    label=column
                )

                # Display percentage labels
                for bar in bars:

                    height = bar.get_height()

                    if height <= 0:
                        continue

                    plt.text(
                        bar.get_x() + bar.get_width()/2,
                        bar.get_y() + height/2,
                        f"{height:.1f}%",
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="white",
                        fontweight="bold"
                    )

                bottom = [
                    b + v
                    for b, v in zip(bottom, percent_data[column])
                ]

            plt.legend(title="Series")

            plt.ylim(0, 100)

        # ==========================
        # STACKED BAR CHART
        # ==========================

        elif chart_type == "Stacked Bar":

            # First column contains row labels
            y_labels = data.iloc[:, 0].astype(str)

            # Remaining numeric columns
            numeric_data = data.select_dtypes(include="number")

            left = [0] * len(y_labels)

            for column in numeric_data.columns:

                bars = plt.barh(
                    y_labels,
                    numeric_data[column],
                    left=left,
                    label=column
                )

                # Display labels
                for bar in bars:

                    width = bar.get_width()

                    if width == 0:
                        continue

                    plt.text(
                        bar.get_x() + width / 2,
                        bar.get_y() + bar.get_height() / 2,
                        f"{width:,.2f}",
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="white",
                        fontweight="bold"
                    )

                # Update left position
                left = [
                    l + v
                    for l, v in zip(left, numeric_data[column])
                ]

            plt.legend(title="Series")

        # ==========================
        # 100% STACKED BAR CHART
        # ==========================

        elif chart_type == "100% Stacked Bar":

            y_labels = data.iloc[:, 0].astype(str)

            numeric_data = data.select_dtypes(include="number")

            # Convert each row to percentages
            percent_data = numeric_data.div(
                numeric_data.sum(axis=1),
                axis=0
            ) * 100

            left = [0] * len(y_labels)

            for column in percent_data.columns:

                bars = plt.barh(
                    y_labels,
                    percent_data[column],
                    left=left,
                    label=column
                )

                # Display percentage labels
                for bar in bars:

                    width = bar.get_width()

                    if width <= 0:
                        continue

                    plt.text(
                        bar.get_x() + width / 2,
                        bar.get_y() + bar.get_height() / 2,
                        f"{width:.1f}%",
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="white",
                        fontweight="bold"
                    )

                left = [
                    l + v
                    for l, v in zip(left, percent_data[column])
                ]

            plt.legend(title="Series")

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
        # AREA CHART
        # ==========================

        elif chart_type == "Area":

            plt.fill_between(
                range(len(y)),
                y,
                alpha=0.4
            )

            plt.plot(
                range(len(y)),
                y,
                marker="o",
                linewidth=3
            )

            plt.xticks(
                range(len(x)),
                x,
                rotation=30
            )

            # Display value on each point
            for i, value in enumerate(y):

                plt.text(
                    i,
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
        # DOUGHNUT CHART
        # ==========================

        elif chart_type == "Doughnut":

            plt.pie(
                y,
                labels=x,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(width=0.45)
            )

            plt.title(value_column)
            plt.tight_layout()
            plt.show()
            return
        

        # ==========================
        # SCATTER CHART
        # ==========================

        elif chart_type == "Scatter":

            x = pd.to_numeric(
                data[x_axis],
                errors="coerce"
            ).fillna(0)

            y = pd.to_numeric(
                data[value_column],
                errors="coerce"
            ).fillna(0)

            plt.scatter(
                x,
                y,
                s=80,
                alpha=0.8
            )

            # Show value labels
            for i in range(len(x)):

                plt.text(
                    x.iloc[i],
                    y.iloc[i],
                    f"{y.iloc[i]:,.2f}",
                    fontsize=8,
                    ha="left",
                    va="bottom"
                )

            plt.xlabel(x_axis)
            plt.ylabel(value_column)

            plt.title(f"{value_column} vs {x_axis}")

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
            plt.xlim(0, max(y) * 1.10)

        elif chart_type == "Stacked Bar":
            max_total = numeric_data.sum(axis=1).max()
            plt.xlim(0, max_total * 1.10)

        elif chart_type == "100% Stacked Bar":
            plt.xlim(0, 100)

        elif chart_type == "Column":
            plt.ylim(0, max(y) * 1.10)

        elif chart_type == "Stacked Column":
            max_total = numeric_data.sum(axis=1).max()
            plt.ylim(0, max_total * 1.10)

        elif chart_type == "100% Stacked Column":
            plt.ylim(0, 100)
        plt.tight_layout()

        plt.show()