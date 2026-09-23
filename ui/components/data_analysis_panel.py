import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class DataAnalysisPanel(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("InsightAI - Data Analysis")
        self.geometry("1100x700")
        self.minsize(900, 600)

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
            text="Explore, compare and analyze your dataset.",
            font=("Arial", 13)
        )
        subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ==================================================
        # Main Content
        # ==================================================

        content = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )

        content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ==================================================
        # Analysis Options
        # ==================================================

        options_title = ctk.CTkLabel(
            content,
            text="Analysis Tools",
            font=("Arial", 19, "bold")
        )

        options_title.pack(
            anchor="w",
            padx=10,
            pady=(10, 15)
        )

        # ==================================================
        # Numeric Summary
        # ==================================================

        self.create_analysis_card(
            content,
            "🔢 Numeric Summary",
            "Analyze minimum, maximum, median and standard deviation of numeric columns.",
            "numeric"
        )

        # ==================================================
        # Group Analysis
        # ==================================================

        self.create_analysis_card(
            content,
            "📊 Group Analysis",
            "Compare numerical values across categories.",
            "group"
        )

        # ==================================================
        # Top / Bottom Analysis
        # ==================================================

        self.create_analysis_card(
            content,
            "🏆 Top / Bottom Analysis",
            "Find the highest or lowest values in a numerical column.",
            "top_bottom"
        )

        # ==================================================
        # Category Frequency
        # ==================================================

        self.create_analysis_card(
            content,
            "📋 Category Frequency",
            "Count how frequently each category appears.",
            "frequency"
        )

        # ==================================================
        # Outlier Detection
        # ==================================================

        self.create_analysis_card(
            content,
            "⚠️ Outlier Detection",
            "Identify unusually high or low numerical values.",
            "outliers"
        )

    # ======================================================
    # Analysis Card
    # ======================================================

    def create_analysis_card(
        self,
        master,
        title,
        description,
        analysis_type
    ):

        card = ctk.CTkFrame(
            master,
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 17, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        description_label = ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 12),
            wraplength=750,
            justify="left"
        )

        description_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        button = ctk.CTkButton(
            card,
            text="Open Analysis",
            width=150,
            command=lambda: self.open_analysis(analysis_type)
        )

        button.pack(
            anchor="e",
            padx=20,
            pady=(0, 15)
        )

    # ======================================================
    # Open Analysis
    # ======================================================

    def open_analysis(self, analysis_type):

        if analysis_type == "numeric":

            self.show_numeric_summary()

        elif analysis_type == "group":

            self.show_group_analysis()

        else:

            print(
                f"Analysis not implemented yet: {analysis_type}"
            )


    # ======================================================
    # Numeric Summary
    # ======================================================

    def show_numeric_summary(self):

        try:

            dataframe = self.master.analysis.numeric_summary(
                self.master.current_df
            )

            if dataframe.empty:

                ctk.CTkMessagebox if False else None

                from tkinter import messagebox

                messagebox.showwarning(
                    "Numeric Summary",
                    "No numeric columns were found in the dataset."
                )

                return

            window = ctk.CTkToplevel(self)

            window.title(
                "InsightAI - Numeric Summary"
            )

            window.geometry(
                "900x550"
            )

            title = ctk.CTkLabel(
                window,
                text="🔢 Numeric Summary",
                font=("Arial", 22, "bold")
            )

            title.pack(
                anchor="w",
                padx=20,
                pady=(20, 10)
            )

            # ----------------------------------------------
            # Table
            # ----------------------------------------------

            table_frame = ctk.CTkFrame(
                window,
                corner_radius=10
            )

            table_frame.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=(0, 20)
            )


            tree_frame = tk.Frame(
                table_frame,
                bg="#1E1E1E"
            )

            tree_frame.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            columns = list(
                dataframe.columns
            )

            tree = ttk.Treeview(
                tree_frame,
                columns=columns,
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

            for column in columns:

                tree.heading(
                    column,
                    text=column
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

            # ----------------------------------------------
            # Treeview styling
            # ----------------------------------------------

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

        except Exception as e:

            from tkinter import messagebox

            messagebox.showerror(
                "Numeric Summary Error",
                str(e)
            )

    # ======================================================
    # Group Analysis
    # ======================================================

    def show_group_analysis(self):

        try:

            df = self.master.current_df

            categorical_columns = (
                self.master.analysis.get_categorical_columns(df)
            )

            numeric_columns = (
                self.master.analysis.get_numeric_columns(df)
            )

            if not categorical_columns:

                from tkinter import messagebox

                messagebox.showwarning(
                    "Group Analysis",
                    "No categorical columns were found in the dataset."
                )

                return

            if not numeric_columns:

                from tkinter import messagebox

                messagebox.showwarning(
                    "Group Analysis",
                    "No numeric columns were found in the dataset."
                )

                return

            window = ctk.CTkToplevel(self)

            window.title(
                "InsightAI - Group Analysis"
            )

            window.geometry(
                "1000x650"
            )

            # ==================================================
            # Header
            # ==================================================

            title = ctk.CTkLabel(
                window,
                text="📊 Group Analysis",
                font=("Arial", 22, "bold")
            )

            title.pack(
                anchor="w",
                padx=20,
                pady=(20, 5)
            )

            subtitle = ctk.CTkLabel(
                window,
                text="Compare a numerical column across categories.",
                font=("Arial", 12)
            )

            subtitle.pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

            # ==================================================
            # Controls
            # ==================================================

            controls = ctk.CTkFrame(
                window,
                corner_radius=10
            )

            controls.pack(
                fill="x",
                padx=20,
                pady=(0, 15)
            )

            # Category column

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

            # Numeric column

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

            # Analyze button

            analyze_button = ctk.CTkButton(
                controls,
                text="Analyze",
                width=150
            )

            analyze_button.grid(
                row=1,
                column=2,
                padx=(20, 20),
                pady=(0, 15)
            )

            # ==================================================
            # Result Area
            # ==================================================

            result_frame = ctk.CTkFrame(
                window,
                corner_radius=10
            )

            result_frame.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=(0, 20)
            )

            # ==================================================
            # Treeview
            # ==================================================
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

            # ==================================================
            # Display Results
            # ==================================================

            def display_results(dataframe):

                tree.delete(
                    *tree.get_children()
                )

                tree["columns"] = list(
                    dataframe.columns
                )

                for column in dataframe.columns:

                    tree.heading(
                        column,
                        text=column
                    )

                    tree.column(
                        column,
                        width=140,
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

            # ==================================================
            # Run Analysis
            # ==================================================

            def run_analysis():

                category_column = (
                    category_dropdown.get()
                )

                numeric_column = (
                    numeric_dropdown.get()
                )

                result = (
                    self.master.analysis.group_analysis(
                        df,
                        category_column,
                        numeric_column
                    )
                )

                if result.empty:

                    from tkinter import messagebox

                    messagebox.showwarning(
                        "Group Analysis",
                        "No analysis results were generated."
                    )

                    return

                display_results(result)

            analyze_button.configure(
                command=run_analysis
            )

            # ==================================================
            # Treeview Styling
            # ==================================================

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

        except Exception as e:

            from tkinter import messagebox

            messagebox.showerror(
                "Group Analysis Error",
                str(e)
            )