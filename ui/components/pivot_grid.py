import customtkinter as ctk
from tkinter import ttk


class PivotGrid(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.tree = ttk.Treeview(self)

        scrollbar_y = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.pack(
            side="top",
            fill="both",
            expand=True
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

    # ===================================
    # Load Pivot
    # ===================================

    def load_dataframe(self, df):

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = list(df.columns)

        self.tree["show"] = "headings"

        for col in df.columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                anchor="center",
                width=120
            )

        for row in df.values.tolist():

            self.tree.insert(
                "",
                "end",
                values=row
            )