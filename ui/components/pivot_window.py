import customtkinter as ctk
from ui.components.pivot_grid import PivotGrid
from core.pivot_chart import PivotChart


class PivotWindow(ctk.CTkToplevel):

    def __init__(self, master, df, pivot_engine):

        super().__init__(master)

        self.df = df
        self.pivot_engine = pivot_engine
        self.chart_engine = PivotChart()

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
        field_options = ["(None)"] + columns
        placeholder = ["-- Select Field --"]

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
            values=field_options,
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
            values=field_options,
            width=180,
            command=self.update_chart_value
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
        # Chart Value
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Chart Value"
        ).grid(
            row=1,
            column=2,
            padx=10
        )

        self.chart_value_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=["Generate Pivot First"],
            width=180
        )

        self.chart_value_dropdown.grid(
            row=1,
            column=3,
            padx=5
        )

        # -----------------------
        # Chart Type
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Chart Type"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        self.chart_type_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=[
                "Bar",
                "Column",
                "Line",
                "Pie"
            ],
            width=180
        )

        self.chart_type_dropdown.set("Bar")

        self.chart_type_dropdown.grid(
            row=2,
            column=1,
            padx=5,
            pady=10
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

        # -----------------------
        # Create Chart Button
        # -----------------------

        self.chart_btn = ctk.CTkButton(
            control_frame,
            text="📊 Create Chart",
            command=self.create_chart
        )

        self.chart_btn.grid(
            row=1,
            column=6,
            padx=10,
            pady=10
        )

        # ==================================
        # Pivot Grid
        # ==================================

        self.result_grid = PivotGrid(self)

        self.result_grid.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ==================================
    # Display Pivot
    # ==================================

    def display_pivot(self, pivot_df):

        self.result_grid.load_dataframe(
            pivot_df.reset_index()
        )

    # ==================================
    # Update Chart Value
    # ==================================

    def update_chart_value(self, choice):

        self.chart_value_dropdown.configure(
            values=[choice]
        )

        self.chart_value_dropdown.set(choice)

    # ==================================
    # Generate Pivot
    # ==================================

    def generate_pivot(self):

        from tkinter import messagebox

        rows = self.row_dropdown.get()
        columns = self.column_dropdown.get()
        values = self.value_dropdown.get()
        agg = self.agg_dropdown.get()

        # ----------------------------
        # Convert "(None)" to None
        # ----------------------------

        if rows == "(None)":
            rows = None

        if columns == "(None)":
            columns = None

        # ----------------------------
        # Validation
        # ----------------------------

        if not values:

            messagebox.showwarning(
                "Missing Field",
                "Please select a Value field."
            )
            return

        if rows is None and columns is None:

            messagebox.showwarning(
                "Missing Field",
                "Please select either a Row field or a Column field."
            )
            return

        # ----------------------------
        # Create Pivot
        # ----------------------------

        self.current_pivot = self.pivot_engine.create_pivot(
            self.df,
            rows,
            columns,
            values,
            agg
        )

        self.display_pivot(self.current_pivot)

        numeric_cols = list(
            self.current_pivot.select_dtypes(include="number").columns
        )

        if numeric_cols:

            self.chart_value_dropdown.configure(
                values=numeric_cols
            )

            self.chart_value_dropdown.set(
                numeric_cols[0]
            )

    # ==================================
    # Create Chart
    # ==================================

    def create_chart(self):

        if not hasattr(self, "current_pivot"):
            return

        value_column = self.chart_value_dropdown.get()
        chart_type = self.chart_type_dropdown.get()

        self.chart_engine.create_chart(
            self.current_pivot,
            value_column,
            chart_type
        )