from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd


class DataAnalysisPanel(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("InsightAI - Data Analysis")
        self.geometry("1200x760")
        self.minsize(1000, 650)

        self.transient(master)

        self._configure_treeview_style()

        # ==================================================
        # Header
        # ==================================================

        header = ctk.CTkFrame(
            self,
            corner_radius=12
        )
        header.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="📊 Data Analysis",
            font=("Arial", 24, "bold")
        )
        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 2)
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Explore, compare and analyze your dataset in one workspace.",
            font=("Arial", 13)
        )
        subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ==================================================
        # Main Analysis Workspace
        # ==================================================

        self.tabview = ctk.CTkTabview(
            self,
            corner_radius=12
        )
        self.tabview.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.tabview.add("🔢 Numeric Summary")
        self.tabview.add("📊 Group Analysis")
        self.tabview.add("🏆 Top / Bottom")
        self.tabview.add("📋 Category Frequency")
        self.tabview.add("⚠️ Outlier Detection")

        # Build all analysis sections inside the same page
        self._build_numeric_tab()
        self._build_group_tab()
        self._build_top_bottom_tab()
        self._build_frequency_tab()
        self._build_outlier_tab()

        # Open with Numeric Summary selected
        self.tabview.set("🔢 Numeric Summary")

    # ======================================================
    # Shared Helpers
    # ======================================================

    def _configure_treeview_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="#1E1E1E",
            foreground="white",
            fieldbackground="#1E1E1E",
            rowheight=30,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#343434",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#3B82F6")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

    def _create_title(self, parent, title, description):
        title_label = ctk.CTkLabel(
            parent,
            text=title,
            font=("Arial", 21, "bold")
        )
        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 3)
        )

        description_label = ctk.CTkLabel(
            parent,
            text=description,
            font=("Arial", 12)
        )
        description_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    def _create_table(self, parent):
        result_frame = ctk.CTkFrame(
            parent,
            corner_radius=10
        )
        result_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        tree_frame = tk.Frame(
            result_frame,
            bg="#1E1E1E"
        )
        tree_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tree = ttk.Treeview(
            tree_frame,
            show="headings"
        )

        vertical_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview
        )
        horizontal_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=tree.xview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )
        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )

        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        return tree

    def _display_dataframe(self, tree, dataframe):
        tree.delete(*tree.get_children())

        if dataframe is None or dataframe.empty:
            tree["columns"] = ["Message"]
            tree.heading("Message", text="Message")
            tree.column(
                "Message",
                width=500,
                anchor="center"
            )
            tree.insert(
                "",
                "end",
                values=("No results found.",)
            )
            return

        columns = list(dataframe.columns)
        tree["columns"] = columns

        for column in columns:
            tree.heading(
                column,
                text=str(column)
            )
            tree.column(
                column,
                width=150,
                minwidth=100,
                anchor="center"
            )

        for _, row in dataframe.iterrows():
            values = []

            for value in row:
                if value is None:
                    value = ""
                elif isinstance(value, float):
                    value = f"{value:,.2f}"
                else:
                    value = str(value)

                values.append(value)

            tree.insert(
                "",
                "end",
                values=values
            )

    def _get_dataframe(self):
        return self.master.current_df

    # ======================================================
    # Numeric Summary
    # ======================================================

    def _build_numeric_tab(self):

        tab = self.tabview.tab("🔢 Numeric Summary")

        self._create_title(
            tab,
            "🔢 Numeric Summary",
            "Analyze count, missing values, sum, minimum, maximum, median and standard deviation of numeric columns."
        )

        df = self._get_dataframe()

        # --------------------------------------------------
        # Get numeric columns
        # --------------------------------------------------

        numeric_columns = list(
            df.select_dtypes(include="number").columns
        )

        if not numeric_columns:

            ctk.CTkLabel(
                tab,
                text="No numeric columns were found in the dataset.",
                font=("Arial", 14)
            ).pack(
                pady=30
            )

            return

        # --------------------------------------------------
        # Calculate Numeric Summary
        # --------------------------------------------------

        result = pd.DataFrame({
            "Column": numeric_columns,
            "Count": [
                df[column].count()
                for column in numeric_columns
            ],
            "Missing": [
                df[column].isna().sum()
                for column in numeric_columns
            ],
            "Sum": [
                df[column].sum()
                for column in numeric_columns
            ],
            "Minimum": [
                df[column].min()
                for column in numeric_columns
            ],
            "Maximum": [
                df[column].max()
                for column in numeric_columns
            ],
            "Median": [
                df[column].median()
                for column in numeric_columns
            ],
            "Standard Deviation": [
                df[column].std()
                for column in numeric_columns
            ]
        })

        # --------------------------------------------------
        # Round numerical results
        # --------------------------------------------------

        numeric_result_columns = [
            "Sum",
            "Minimum",
            "Maximum",
            "Median",
            "Standard Deviation"
        ]

        result[numeric_result_columns] = (
            result[numeric_result_columns]
            .round(2)
        )

        # --------------------------------------------------
        # Display Results
        # --------------------------------------------------

        tree = self._create_table(
            tab
        )

        self._display_dataframe(
            tree,
            result
        )

    # ======================================================
    # Group Analysis
    # ======================================================

    def _build_group_tab(self):

        tab = self.tabview.tab("📊 Group Analysis")

        self._create_title(
            tab,
            "📊 Group Analysis",
            "Compare numerical values across categories."
        )

        df = self._get_dataframe()

        # --------------------------------------------------
        # Find categorical and numeric columns
        # --------------------------------------------------

        categorical_columns = list(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        )

        numeric_columns = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        if not categorical_columns:

            ctk.CTkLabel(
                tab,
                text="No categorical columns were found in the dataset.",
                font=("Arial", 14)
            ).pack(
                pady=30
            )

            return

        if not numeric_columns:

            ctk.CTkLabel(
                tab,
                text="No numeric columns were found in the dataset.",
                font=("Arial", 14)
            ).pack(
                pady=30
            )

            return

        # --------------------------------------------------
        # Controls
        # --------------------------------------------------

        controls = ctk.CTkFrame(
            tab,
            corner_radius=10
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # --------------------------------------------------
        # Category Column
        # --------------------------------------------------

        category_label = ctk.CTkLabel(
            controls,
            text="Category Column"
        )

        category_label.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(15, 5),
            sticky="w"
        )

        category_dropdown = ctk.CTkComboBox(
            controls,
            values=categorical_columns,
            width=250
        )

        category_dropdown.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15)
        )

        category_dropdown.set(
            categorical_columns[0]
        )

        # --------------------------------------------------
        # Numeric Column
        # --------------------------------------------------

        numeric_label = ctk.CTkLabel(
            controls,
            text="Numeric Column"
        )

        numeric_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        numeric_dropdown = ctk.CTkComboBox(
            controls,
            values=numeric_columns,
            width=250
        )

        numeric_dropdown.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 15)
        )

        numeric_dropdown.set(
            numeric_columns[0]
        )

        # --------------------------------------------------
        # Analysis Type
        # --------------------------------------------------

        analysis_label = ctk.CTkLabel(
            controls,
            text="Analysis"
        )

        analysis_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        analysis_dropdown = ctk.CTkComboBox(
            controls,
            values=[
                "All Statistics",
                "Sum",
                "Count",
                "Minimum",
                "Maximum",
                "Median",
                "Mean",
                "Standard Deviation"
            ],
            width=200
        )

        analysis_dropdown.grid(
            row=1,
            column=2,
            padx=10,
            pady=(0, 15)
        )

        analysis_dropdown.set(
            "All Statistics"
        )

        # --------------------------------------------------
        # Analyze Button
        # --------------------------------------------------

        analyze_button = ctk.CTkButton(
            controls,
            text="Analyze",
            width=150
        )

        analyze_button.grid(
            row=1,
            column=3,
            padx=(15, 20),
            pady=(0, 15)
        )

        # --------------------------------------------------
        # Results Table
        # --------------------------------------------------

        tree = self._create_table(
            tab
        )

        # --------------------------------------------------
        # Run Analysis
        # --------------------------------------------------

        def run_analysis():

            category_column = (
                category_dropdown.get()
            )

            numeric_column = (
                numeric_dropdown.get()
            )

            analysis_type = (
                analysis_dropdown.get()
            )

            # ----------------------------------------------
            # Validate selections
            # ----------------------------------------------

            if not category_column:

                messagebox.showwarning(
                    "Group Analysis",
                    "Please select a category column."
                )

                return

            if not numeric_column:

                messagebox.showwarning(
                    "Group Analysis",
                    "Please select a numeric column."
                )

                return

            # ----------------------------------------------
            # Prepare data
            # ----------------------------------------------

            working_df = df[
                [
                    category_column,
                    numeric_column
                ]
            ].copy()

            # Keep missing categories visible
            working_df[category_column] = (
                working_df[category_column]
                .fillna("Missing")
            )

            # Remove rows where numeric value is missing
            working_df = working_df.dropna(
                subset=[numeric_column]
            )

            if working_df.empty:

                messagebox.showwarning(
                    "Group Analysis",
                    "No valid data was found for the selected columns."
                )

                return

            # ----------------------------------------------
            # Group data
            # ----------------------------------------------

            grouped = (
                working_df
                .groupby(
                    category_column,
                    dropna=False
                )[numeric_column]
            )

            # ----------------------------------------------
            # All Statistics
            # ----------------------------------------------

            if analysis_type == "All Statistics":

                result = (
                    grouped
                    .agg(
                        Count="count",
                        Sum="sum",
                        Minimum="min",
                        Maximum="max",
                        Median="median"
                    )
                    .reset_index()
                )

                result[
                    [
                        "Sum",
                        "Minimum",
                        "Maximum",
                        "Median"
                    ]
                ] = result[
                    [
                        "Sum",
                        "Minimum",
                        "Maximum",
                        "Median"
                    ]
                ].round(2)

            # ----------------------------------------------
            # Sum
            # ----------------------------------------------

            elif analysis_type == "Sum":

                result = (
                    grouped
                    .sum()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Sum"
                    }
                )

                result["Sum"] = result["Sum"].round(2)

            # ----------------------------------------------
            # Count
            # ----------------------------------------------

            elif analysis_type == "Count":

                result = (
                    grouped
                    .count()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Count"
                    }
                )

            # ----------------------------------------------
            # Minimum
            # ----------------------------------------------

            elif analysis_type == "Minimum":

                result = (
                    grouped
                    .min()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Minimum"
                    }
                )

                result["Minimum"] = (
                    result["Minimum"]
                    .round(2)
                )

            # ----------------------------------------------
            # Maximum
            # ----------------------------------------------

            elif analysis_type == "Maximum":

                result = (
                    grouped
                    .max()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Maximum"
                    }
                )

                result["Maximum"] = (
                    result["Maximum"]
                    .round(2)
                )

            # ----------------------------------------------
            # Median
            # ----------------------------------------------

            elif analysis_type == "Median":

                result = (
                    grouped
                    .median()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Median"
                    }
                )

                result["Median"] = (
                    result["Median"]
                    .round(2)
                )

            # ----------------------------------------------
            # Mean
            # ----------------------------------------------

            elif analysis_type == "Mean":

                result = (
                    grouped
                    .mean()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Mean"
                    }
                )

                result["Mean"] = (
                    result["Mean"]
                    .round(2)
                )

            # ----------------------------------------------
            # Standard Deviation
            # ----------------------------------------------

            elif analysis_type == "Standard Deviation":

                result = (
                    grouped
                    .std()
                    .reset_index()
                )

                result = result.rename(
                    columns={
                        numeric_column: "Standard Deviation"
                    }
                )

                result["Standard Deviation"] = (
                    result["Standard Deviation"]
                    .round(2)
                )

            # ----------------------------------------------
            # Sort results
            # ----------------------------------------------

            if len(result) > 0:

                result = (
                    result
                    .sort_values(
                        by=result.columns[-1],
                        ascending=False
                    )
                    .reset_index(drop=True)
                )

            # ----------------------------------------------
            # No results
            # ----------------------------------------------

            if result.empty:

                messagebox.showwarning(
                    "Group Analysis",
                    "No analysis results were generated."
                )

                return

            # ----------------------------------------------
            # Display results
            # ----------------------------------------------

            self._display_dataframe(
                tree,
                result
            )

        analyze_button.configure(
            command=run_analysis
        )

    # ======================================================
    # Top / Bottom Analysis
    # ======================================================

    def _build_top_bottom_tab(self):

        tab = self.tabview.tab("🏆 Top / Bottom")

        self._create_title(
            tab,
            "🏆 Top / Bottom Analysis",
            "Find the highest or lowest values, either individually or by category."
        )

        df = self._get_dataframe()

        numeric_columns = (
            self.master.analysis.get_numeric_columns(df)
        )

        categorical_columns = (
            self.master.analysis.get_categorical_columns(df)
        )

        if not numeric_columns:
            ctk.CTkLabel(
                tab,
                text="No numeric columns were found in the dataset.",
                font=("Arial", 14)
            ).pack(
                pady=30
            )
            return

        # ======================================================
        # Controls
        # ======================================================

        controls = ctk.CTkFrame(
            tab,
            corner_radius=10
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # ======================================================
        # Analysis Mode
        # ======================================================

        mode_label = ctk.CTkLabel(
            controls,
            text="Analysis Mode"
        )

        mode_label.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(15, 5),
            sticky="w"
        )

        mode_dropdown = ctk.CTkComboBox(
            controls,
            values=[
                "Individual Records",
                "By Category"
            ],
            width=180
        )

        mode_dropdown.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15)
        )

        mode_dropdown.set(
            "Individual Records"
        )

        # ======================================================
        # Category Column
        # ======================================================

        category_label = ctk.CTkLabel(
            controls,
            text="Category Column"
        )

        category_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        category_dropdown = ctk.CTkComboBox(
            controls,
            values=(
                categorical_columns
                if categorical_columns
                else ["No categorical columns"]
            ),
            width=190
        )

        category_dropdown.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 15)
        )

        if categorical_columns:
            category_dropdown.set(
                categorical_columns[0]
            )
        else:
            category_dropdown.set(
                "No categorical columns"
            )

        # Disable category initially
        category_dropdown.configure(
            state="disabled"
        )

        # ======================================================
        # Numeric Column
        # ======================================================

        column_label = ctk.CTkLabel(
            controls,
            text="Numeric Column"
        )

        column_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        column_dropdown = ctk.CTkComboBox(
            controls,
            values=numeric_columns,
            width=190
        )

        column_dropdown.grid(
            row=1,
            column=2,
            padx=10,
            pady=(0, 15)
        )

        column_dropdown.set(
            numeric_columns[0]
        )

        # ======================================================
        # Analysis Type
        # ======================================================

        type_label = ctk.CTkLabel(
            controls,
            text="Analysis Type"
        )

        type_label.grid(
            row=0,
            column=3,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        type_dropdown = ctk.CTkComboBox(
            controls,
            values=[
                "Top",
                "Bottom"
            ],
            width=120
        )

        type_dropdown.grid(
            row=1,
            column=3,
            padx=10,
            pady=(0, 15)
        )

        type_dropdown.set(
            "Top"
        )

        # ======================================================
        # Number of Records
        # ======================================================

        records_label = ctk.CTkLabel(
            controls,
            text="Number"
        )

        records_label.grid(
            row=0,
            column=4,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        records_dropdown = ctk.CTkComboBox(
            controls,
            values=[
                "5",
                "10",
                "20",
                "50"
            ],
            width=90
        )

        records_dropdown.grid(
            row=1,
            column=4,
            padx=10,
            pady=(0, 15)
        )

        records_dropdown.set(
            "10"
        )

        # ======================================================
        # Analyze Button
        # ======================================================

        analyze_button = ctk.CTkButton(
            controls,
            text="Analyze",
            width=120
        )

        analyze_button.grid(
            row=1,
            column=5,
            padx=(15, 20),
            pady=(0, 15)
        )

        # ======================================================
        # Change Analysis Mode
        # ======================================================

        def update_mode(choice=None):

            if mode_dropdown.get() == "By Category":

                if categorical_columns:

                    category_dropdown.configure(
                        state="normal"
                    )

            else:

                category_dropdown.configure(
                    state="disabled"
                )

        mode_dropdown.configure(
            command=update_mode
        )

        # ======================================================
        # Results Table
        # ======================================================

        tree = self._create_table(
            tab
        )

        def run_analysis():

            analysis_type = type_dropdown.get()

            n = int(
                records_dropdown.get()
            )

            numeric_column = (
                column_dropdown.get()
            )

            # ==================================================
            # Individual Records
            # ==================================================

            if mode_dropdown.get() == "Individual Records":

                result = (
                    df[[numeric_column]]
                    .dropna()
                    .sort_values(
                        by=numeric_column,
                        ascending=(
                            analysis_type == "Bottom"
                        )
                    )
                    .head(n)
                    .reset_index(drop=True)
                )

            # ==================================================
            # By Category
            # ==================================================

            else:

                if not categorical_columns:

                    messagebox.showwarning(
                        "Top / Bottom Analysis",
                        "No categorical columns were found in the dataset."
                    )

                    return

                category_column = (
                    category_dropdown.get()
                )

                # Group numeric values by category
                result = (
                    df.groupby(
                        category_column,
                        dropna=False
                    )[numeric_column]
                    .sum()
                    .reset_index()
                )

                # Rename the calculated value
                result = result.rename(
                    columns={
                        numeric_column: "Total"
                    }
                )

                # Sort Top or Bottom
                result = (
                    result
                    .sort_values(
                        by="Total",
                        ascending=(
                            analysis_type == "Bottom"
                        )
                    )
                    .head(n)
                    .reset_index(drop=True)
                )

                result["Total"] = result["Total"].round(2)

            # ==================================================
            # No Results
            # ==================================================

            if result.empty:

                messagebox.showwarning(
                    "Top / Bottom Analysis",
                    "No results were found."
                )

                return

            # ==================================================
            # Display Results
            # ==================================================

            self._display_dataframe(
                tree,
                result
            )
        # Connect button
        analyze_button.configure(
            command=run_analysis
        )
    # ======================================================
    # Category Frequency
    # ======================================================

    def _build_frequency_tab(self):
        tab = self.tabview.tab("📋 Category Frequency")

        self._create_title(
            tab,
            "📋 Category Frequency",
            "Count how frequently each category appears."
        )

        df = self._get_dataframe()
        categorical_columns = (
            self.master.analysis.get_categorical_columns(df)
        )

        if not categorical_columns:
            ctk.CTkLabel(
                tab,
                text="No categorical columns were found in the dataset.",
                font=("Arial", 14)
            ).pack(
                pady=30
            )
            return

        controls = ctk.CTkFrame(
            tab,
            corner_radius=10
        )
        controls.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        column_label = ctk.CTkLabel(
            controls,
            text="Categorical Column"
        )
        column_label.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(15, 5),
            sticky="w"
        )

        column_dropdown = ctk.CTkComboBox(
            controls,
            values=categorical_columns,
            width=300
        )
        column_dropdown.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15)
        )
        column_dropdown.set(
            categorical_columns[0]
        )

        analyze_button = ctk.CTkButton(
            controls,
            text="Analyze",
            width=150
        )
        analyze_button.grid(
            row=1,
            column=1,
            padx=(15, 20),
            pady=(0, 15)
        )

        tree = self._create_table(
            tab
        )

        def run_analysis():
            result = self.master.analysis.category_frequency(
                df,
                column_dropdown.get()
            )

            if result.empty:
                messagebox.showwarning(
                    "Category Frequency",
                    "No frequency results were generated."
                )
                return

            self._display_dataframe(
                tree,
                result
            )

        analyze_button.configure(
            command=run_analysis
        )

    # ======================================================
    # Outlier Detection
    # ======================================================

    def _build_outlier_tab(self):

        tab = self.tabview.tab("⚠️ Outlier Detection")

        self._create_title(
            tab,
            "⚠️ Outlier Detection",
            "Identify unusually high or low numerical values using the IQR method."
        )

        df = self._get_dataframe()

        # --------------------------------------------------
        # Find numeric columns
        # --------------------------------------------------

        numeric_columns = list(
            df.select_dtypes(include="number").columns
        )

        if not numeric_columns:

            ctk.CTkLabel(
                tab,
                text="No numeric columns were found in the dataset.",
                font=("Arial", 14)
            ).pack(
                pady=30
            )

            return

        # --------------------------------------------------
        # Controls
        # --------------------------------------------------

        controls = ctk.CTkFrame(
            tab,
            corner_radius=10
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        column_label = ctk.CTkLabel(
            controls,
            text="Numeric Column"
        )

        column_label.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(15, 5),
            sticky="w"
        )

        column_dropdown = ctk.CTkComboBox(
            controls,
            values=numeric_columns,
            width=300
        )

        column_dropdown.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15)
        )

        column_dropdown.set(
            numeric_columns[0]
        )

        analyze_button = ctk.CTkButton(
            controls,
            text="Detect Outliers",
            width=160
        )

        analyze_button.grid(
            row=1,
            column=1,
            padx=(15, 20),
            pady=(0, 15)
        )

        # --------------------------------------------------
        # Outlier Summary
        # --------------------------------------------------

        summary_frame = ctk.CTkFrame(
            tab,
            corner_radius=10
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Outlier Summary",
            font=("Arial", 15, "bold")
        )

        summary_title.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=15,
            pady=(12, 8),
            sticky="w"
        )

        total_label = ctk.CTkLabel(
            summary_frame,
            text="Total Records: —"
        )

        total_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        outlier_label = ctk.CTkLabel(
            summary_frame,
            text="Outliers Found: —"
        )

        outlier_label.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        percentage_label = ctk.CTkLabel(
            summary_frame,
            text="Outlier %: —"
        )

        percentage_label.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        iqr_label = ctk.CTkLabel(
            summary_frame,
            text="IQR: —"
        )

        iqr_label.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        q1_label = ctk.CTkLabel(
            summary_frame,
            text="Q1: —"
        )

        q1_label.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        q3_label = ctk.CTkLabel(
            summary_frame,
            text="Q3: —"
        )

        q3_label.grid(
            row=2,
            column=1,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        lower_label = ctk.CTkLabel(
            summary_frame,
            text="Lower Bound: —"
        )

        lower_label.grid(
            row=2,
            column=2,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        upper_label = ctk.CTkLabel(
            summary_frame,
            text="Upper Bound: —"
        )

        upper_label.grid(
            row=2,
            column=3,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        # --------------------------------------------------
        # Results Table
        # --------------------------------------------------

        tree = self._create_table(
            tab
        )

        # --------------------------------------------------
        # Run Outlier Analysis
        # --------------------------------------------------

        def run_analysis():

            column = column_dropdown.get()

            if not column:
                return

            # ----------------------------------------------
            # Get valid numeric values
            # ----------------------------------------------

            values = (
                df[column]
                .dropna()
            )

            if values.empty:

                messagebox.showwarning(
                    "Outlier Detection",
                    "The selected column contains no valid numeric values."
                )

                return

            # ----------------------------------------------
            # Calculate Quartiles
            # ----------------------------------------------

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)

            # ----------------------------------------------
            # Calculate IQR
            # ----------------------------------------------

            iqr = q3 - q1

            # ----------------------------------------------
            # Calculate Bounds
            # ----------------------------------------------

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            # ----------------------------------------------
            # Detect Outliers
            # ----------------------------------------------

            outlier_mask = (
                (df[column] < lower_bound) |
                (df[column] > upper_bound)
            )

            result = (
                df.loc[
                    outlier_mask
                    & df[column].notna()
                ]
                .copy()
            )

            # ----------------------------------------------
            # Calculate Summary
            # ----------------------------------------------

            total_records = len(values)

            outlier_count = len(result)

            outlier_percentage = (
                (outlier_count / total_records) * 100
                if total_records > 0
                else 0
            )

            # ----------------------------------------------
            # Update Summary
            # ----------------------------------------------

            total_label.configure(
                text=f"Total Records: {total_records:,}"
            )

            outlier_label.configure(
                text=f"Outliers Found: {outlier_count:,}"
            )

            percentage_label.configure(
                text=f"Outlier %: {outlier_percentage:.2f}%"
            )

            iqr_label.configure(
                text=f"IQR: {iqr:,.2f}"
            )

            q1_label.configure(
                text=f"Q1: {q1:,.2f}"
            )

            q3_label.configure(
                text=f"Q3: {q3:,.2f}"
            )

            lower_label.configure(
                text=f"Lower Bound: {lower_bound:,.2f}"
            )

            upper_label.configure(
                text=f"Upper Bound: {upper_bound:,.2f}"
            )

            # ----------------------------------------------
            # Display Results
            # ----------------------------------------------

            self._display_dataframe(
                tree,
                result
            )

            # ----------------------------------------------
            # No Outliers
            # ----------------------------------------------

            if result.empty:

                messagebox.showinfo(
                    "Outlier Detection",
                    "No outliers were detected for the selected column."
                )

        analyze_button.configure(
            command=run_analysis
        )