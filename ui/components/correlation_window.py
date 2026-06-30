import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CorrelationWindow(ctk.CTkToplevel):

    def __init__(self, master, corr_matrix):

        super().__init__(master)

        self.title("Correlation Analysis")
        self.geometry("900x700")

        title = ctk.CTkLabel(
            self,
            text="📊 Correlation Analysis",
            font=("Arial", 22, "bold")
        )

        title.pack(
            pady=(15, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Relationship between all numeric variables",
            text_color="gray"
        )

        subtitle.pack(
            pady=(0, 10)
        )

        figure = Figure(
            figsize=(8, 6),
            dpi=100
        )

        ax = figure.add_subplot(111)

        im = ax.imshow(
            corr_matrix,
            cmap="coolwarm",
            vmin=-1,
            vmax=1
        )

        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))

        ax.set_xticklabels(
            corr_matrix.columns,
            rotation=45,
            ha="right"
        )

        ax.set_yticklabels(
            corr_matrix.columns
        )

        # Show correlation values
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                ax.text(
                    j,
                    i,
                    f"{corr_matrix.iloc[i, j]:.2f}",
                    ha="center",
                    va="center",
                    fontsize=9
                )

        figure.colorbar(im)

        canvas = FigureCanvasTkAgg(
            figure,
            self
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        insight_box = ctk.CTkTextbox(
            self,
            height=120
        )

        insight_box.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        insight_box.insert(
            "end",
            "Correlation Insights\n"
        )

        insight_box.insert(
            "end",
            "------------------------------\n\n"
        )


        cols = corr_matrix.columns

        for i in range(len(cols)):

            for j in range(i + 1, len(cols)):

                value = corr_matrix.iloc[i, j]

                if abs(value) >= 0.70:

                    if value > 0:

                        relation = "Strong Positive"

                    else:

                        relation = "Strong Negative"

                    insight_box.insert(
                        "end",
                        f"• {cols[i]} ↔ {cols[j]} : "
                        f"{relation} ({value:.2f})\n"
                    )

        insight_box.configure(
            state="disabled"
        )