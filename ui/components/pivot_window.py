import customtkinter as ctk


class PivotWindow(ctk.CTkToplevel):

    def __init__(self, master, df, pivot_engine):

        super().__init__(master)

        self.df = df
        self.pivot_engine = pivot_engine

        self.title("Pivot Table Builder")
        self.geometry("1100x700")

        # ==================================
        # Header
        # ==================================

        title = ctk.CTkLabel(
            self,
            text="📊 Pivot Table Builder",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(15, 10)
        )

        # ==================================
        # Controls
        # ==================================

        control_frame = ctk.CTkFrame(self)

        control_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        columns = list(df.columns)

        # -----------------------
        # Rows
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Rows"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.row_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=columns,
            width=180
        )

        self.row_dropdown.grid(
            row=0,
            column=1,
            padx=5
        )

        # -----------------------
        # Columns
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Columns"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.column_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=columns,
            width=180
        )

        self.column_dropdown.grid(
            row=0,
            column=3,
            padx=5
        )

        # -----------------------
        # Values
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Values"
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.value_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=columns,
            width=180
        )

        self.value_dropdown.grid(
            row=0,
            column=5,
            padx=5
        )

        # -----------------------
        # Aggregation
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Aggregation"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=15
        )

        self.agg_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=[
                "sum",
                "mean",
                "count",
                "min",
                "max"
            ],
            width=180
        )

        self.agg_dropdown.set("sum")

        self.agg_dropdown.grid(
            row=1,
            column=1,
            padx=5
        )

        # -----------------------
        # Generate Button
        # -----------------------

        self.generate_btn = ctk.CTkButton(
            control_frame,
            text="Generate Pivot",
            command=self.generate_pivot
        )

        self.generate_btn.grid(
            row=1,
            column=5,
            pady=10,
            sticky="e"
        )

        # ==================================
        # Result Box
        # ==================================

        self.result_box = ctk.CTkTextbox(
            self,
            font=("Consolas", 12)
        )

        self.result_box.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ==================================
    # Display Pivot
    # ==================================

    def display_pivot(self, pivot_df):

        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")

        self.result_box.insert(
            "1.0",
            pivot_df.to_string(index=False)
        )

        self.result_box.configure(state="disabled")

    # ==================================
    # Generate Pivot
    # ==================================

    def generate_pivot(self):

        rows = self.row_dropdown.get()
        columns = self.column_dropdown.get()
        values = self.value_dropdown.get()
        agg = self.agg_dropdown.get()

        pivot = self.pivot_engine.create_pivot(
            self.df,
            rows,
            columns,
            values,
            agg
        )

        self.display_pivot(pivot)