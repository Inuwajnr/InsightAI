import tkinter as tk
import customtkinter as ctk
from ui.components.pivot_grid import PivotGrid
from core.pivot_chart import PivotChart
from ui.components.filter_dialog import FilterDialog


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
            sticky="n"
        )

        self.row_frame = ctk.CTkScrollableFrame(
            control_frame,
            width=180,
            height=120
        )

        self.row_frame.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.row_vars = {}

        for col in columns:

            var = ctk.BooleanVar()

            chk = ctk.CTkCheckBox(
                self.row_frame,
                text=col,
                variable=var
            )

            chk.pack(
                anchor="w",
                padx=5,
                pady=2
            )

            self.row_vars[col] = var

       # -----------------------
        # Columns
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Columns"
        ).grid(
            row=0,
            column=2,
            padx=10,
            sticky="n"
        )

        self.column_frame = ctk.CTkScrollableFrame(
            control_frame,
            width=180,
            height=120
        )

        self.column_frame.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        self.column_vars = {}

        for col in columns:

            var = ctk.BooleanVar()

            chk = ctk.CTkCheckBox(
                self.column_frame,
                text=col,
                variable=var
            )

            chk.pack(
                anchor="w",
                padx=5,
                pady=2
            )

            self.column_vars[col] = var
        # -----------------------
        # Values (Multi Select)
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Values"
        ).grid(
            row=0,
            column=4,
            padx=10,
            sticky="n"
        )

        self.value_listbox = ctk.CTkScrollableFrame(
            control_frame,
            width=180,
            height=120
        )

        self.value_listbox.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        self.value_vars = {}

        for col in columns:

            var = ctk.BooleanVar()

            chk = ctk.CTkCheckBox(
                self.value_listbox,
                text=col,
                variable=var
            )

            chk.pack(
                anchor="w",
                padx=5,
                pady=2
            )

            self.value_vars[col] = var
        # -----------------------
        # Filters
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Filters"
        ).grid(
            row=0,
            column=6,
            padx=10,
            sticky="n"
        )

        self.filter_listbox = ctk.CTkScrollableFrame(
            control_frame,
            width=180,
            height=120
        )

        self.filter_listbox.grid(
            row=0,
            column=7,
            padx=5,
            pady=5
        )

        self.filter_vars = {}

        for col in columns:

            var = ctk.BooleanVar()

            chk = ctk.CTkCheckBox(
                self.filter_listbox,
                text=col,
                variable=var
            )

            chk.pack(
                anchor="w",
                padx=5,
                pady=2
            )

            self.filter_vars[col] = var
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
        # X Axis (Scatter Chart)
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="X-Axis"
        ).grid(
            row=1,
            column=4,
            padx=10
        )

        self.x_axis_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=["Generate Pivot First"],
            width=180
        )

        self.x_axis_dropdown.grid(
            row=1,
            column=5,
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
                "Stacked Column",
                "100% Stacked Column",
                "Stacked Bar",
                "100% Stacked Bar",
                "Line",
                "Area",
                "Pie",
                "Doughnut",
                "Scatter",
                "Histogram",
                "Box Plot",
                "Heatmap",
                "Treemap",
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
        # Analysis Field
        # -----------------------

        ctk.CTkLabel(
            control_frame,
            text="Analysis Field"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10
        )

        self.analysis_field_dropdown = ctk.CTkOptionMenu(
            control_frame,
            values=["Select Numeric Field"],
            width=180
        )

        self.analysis_field_dropdown.grid(
            row=3,
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
            row=2,
            column=3,
            padx=10,
            pady=10,
            sticky="w"
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
            row=2,
            column=4,
            padx=10,
            pady=10,
            sticky="w"
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

        # ----------------------------
        # Rows
        # ----------------------------

        rows = [
            field
            for field, var in self.row_vars.items()
            if var.get()
        ]
        self.current_row_fields = rows.copy()

        # ----------------------------
        # Columns
        # ----------------------------

        columns = [
            field
            for field, var in self.column_vars.items()
            if var.get()
        ]
        self.current_column_fields = columns.copy()

        # ----------------------------
        # Values & Aggregation
        # ----------------------------

        values = [
            field
            for field, var in self.value_vars.items()
            if var.get()
        ]
        agg = self.agg_dropdown.get()


        # ----------------------------
        # Filters
        # ----------------------------

        filters = [
            field
            for field, var in self.filter_vars.items()
            if var.get()
        ]

        print("Filters:", filters)

        # ----------------------------
        # Debug
        # ----------------------------

        print("Rows:", rows)
        print("Columns:", columns)
        print("Values:", values)
        print("Aggregation:", agg)

        # ----------------------------
        # Convert Empty Selection to None
        # ----------------------------

        if len(rows) == 0:
            rows = None

        if len(columns) == 0:
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
        # Show Filter Dialog
        # ----------------------------

        filtered_df = self.df

        if filters:

            dialog = FilterDialog(
                self,
                self.df,
                filters
            )

            self.wait_window(dialog)

            selected_filters = dialog.result

            print(selected_filters)

            filtered_df = self.df.copy()

            for field, value in selected_filters.items():

                filtered_df = filtered_df[
                    filtered_df[field].astype(str) == value
                ]

        # ----------------------------
        # Create Pivot
        # ----------------------------

        self.current_pivot = self.pivot_engine.create_pivot(
            filtered_df,
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

            print(numeric_cols)
            print(type(numeric_cols[0]))

        # Populate Analysis Field dropdown
        original_numeric_cols = list(
            self.df.select_dtypes(include="number").columns
        )

        if original_numeric_cols:

            self.analysis_field_dropdown.configure(
                values=original_numeric_cols
            )

            self.analysis_field_dropdown.set(
                original_numeric_cols[0]
            )

        # Populate X-Axis dropdown
        x_cols = list(
            self.current_pivot.select_dtypes(include="number").columns
        )

        self.x_axis_dropdown.configure(
            values=x_cols
        )

        self.x_axis_dropdown.set(x_cols[0])

    # ==================================
    # Create Chart
    # ==================================

    def create_chart(self):

        if not hasattr(self, "current_pivot"):
            return

        chart_type = self.chart_type_dropdown.get()

        # Statistical charts use original dataset
        if chart_type in [
            "Histogram",
            "Box Plot",
            "Heatmap",
            "Bubble",
            "Pareto",
            "Waterfall",
        ]:
            value_column = self.analysis_field_dropdown.get()
        else:
            value_column = self.chart_value_dropdown.get()

        row_fields = getattr(self, "current_row_fields", [])


        x_axis = self.x_axis_dropdown.get()
        self.chart_engine.create_chart(
            self.current_pivot,
            value_column,
            chart_type,
            row_fields,
            x_axis,
            self.df
        )