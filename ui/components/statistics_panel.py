import customtkinter as ctk
import tkinter as tk
from tkinter import ttk


class StatisticsPanel(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        summary,
        descriptive,
        missing,
        data_types,
        numeric_columns,
        categorical_columns
    ):

        super().__init__(master)

        self.title("InsightAI - Dataset Statistics")
        self.geometry("1100x750")
        self.minsize(900, 600)

        # ==========================================
        # Header
        # ==========================================

        header = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        header.pack(
            fill="x"
        )

        title = ctk.CTkLabel(
            header,
            text="📈 Dataset Statistics",
            font=("Arial", 24, "bold")
        )
        title.pack(
            side="left",
            padx=20,
            pady=15
        )

        # ==========================================
        # Main Scrollable Area
        # ==========================================

        scroll_frame = ctk.CTkScrollableFrame(
            self
        )

        scroll_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # ==========================================
        # Dataset Summary
        # ==========================================

        summary_title = ctk.CTkLabel(
            scroll_frame,
            text="📊 Dataset Summary",
            font=("Arial", 18, "bold")
        )

        summary_title.pack(
            anchor="w",
            pady=(5, 10)
        )

        summary_frame = ctk.CTkFrame(
            scroll_frame
        )

        summary_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        self.create_summary_card(
            summary_frame,
            "Rows",
            summary["rows"]
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.create_summary_card(
            summary_frame,
            "Columns",
            summary["columns"]
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.create_summary_card(
            summary_frame,
            "Missing Values",
            summary["missing"]
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.create_summary_card(
            summary_frame,
            "Duplicate Rows",
            summary["duplicates"]
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.create_summary_card(
            summary_frame,
            "Memory",
            f"{summary['memory']} KB"
        ).grid(
            row=0,
            column=4,
            padx=10,
            pady=10,
            sticky="ew"
        )

        for column in range(5):
            summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # ==========================================
        # Numeric Columns
        # ==========================================

        self.create_column_section(
            scroll_frame,
            "🔢 Numeric Columns",
            numeric_columns
        )

        # ==========================================
        # Categorical Columns
        # ==========================================

        self.create_column_section(
            scroll_frame,
            "🔤 Categorical Columns",
            categorical_columns
        )

        # ==========================================
        # Descriptive Statistics
        # ==========================================

        self.create_table_section(
            scroll_frame,
            "📋 Descriptive Statistics",
            descriptive
        )

        # ==========================================
        # Missing Values
        # ==========================================

        self.create_table_section(
            scroll_frame,
            "⚠️ Missing Values",
            missing
        )

        # ==========================================
        # Data Types
        # ==========================================

        self.create_table_section(
            scroll_frame,
            "🧬 Data Types",
            data_types
        )

    # ==================================================
    # Summary Card
    # ==================================================

    def create_summary_card(
        self,
        master,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            master,
            corner_radius=10
        )

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 12)
        )

        title_label.pack(
            pady=(10, 2)
        )

        value_label = ctk.CTkLabel(
            frame,
            text=str(value),
            font=("Arial", 20, "bold")
        )

        value_label.pack(
            pady=(2, 10)
        )

        return frame

    # ==================================================
    # Column Section
    # ==================================================

    def create_column_section(
        self,
        master,
        title,
        columns
    ):

        title_label = ctk.CTkLabel(
            master,
            text=title,
            font=("Arial", 18, "bold")
        )

        title_label.pack(
            anchor="w",
            pady=(5, 8)
        )

        frame = ctk.CTkFrame(
            master
        )

        frame.pack(
            fill="x",
            pady=(0, 20)
        )

        if not columns:

            ctk.CTkLabel(
                frame,
                text="None"
            ).pack(
                anchor="w",
                padx=15,
                pady=10
            )

            return

        for column in columns:

            ctk.CTkLabel(
                frame,
                text=f"• {column}",
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=3
            )
    # ==================================================
    # Table Section
    # ==================================================

    def create_table_section(
        self,
        master,
        title,
        dataframe
    ):

        title_label = ctk.CTkLabel(
            master,
            text=title,
            font=("Arial", 18, "bold")
        )

        title_label.pack(
            anchor="w",
            pady=(5, 8)
        )

        # ==========================================
        # Table Container
        # ==========================================

        table_container = ctk.CTkFrame(
            master,
            corner_radius=10
        )

        table_container.pack(
            fill="both",
            expand=True,
            pady=(0, 20)
        )

        if dataframe is None or dataframe.empty:

            ctk.CTkLabel(
                table_container,
                text="No data available."
            ).pack(
                padx=15,
                pady=15
            )

            return

        # ==========================================
        # Convert dataframe values to strings
        # ==========================================

        dataframe = dataframe.copy()

        dataframe.columns = [
            str(column)
            for column in dataframe.columns
        ]

        dataframe = dataframe.reset_index(
            drop=True
        )

        # ==========================================
        # Treeview
        # ==========================================

        tree_frame = tk.Frame(
            table_container,
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
            show="headings",
            height=10
        )

        # ==========================================
        # Vertical Scrollbar
        # ==========================================

        vertical_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # Horizontal Scrollbar
        # ==========================================

        horizontal_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=tree.xview
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

        # ==========================================
        # Table Headers
        # ==========================================

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=130,
                minwidth=100,
                anchor="center"
            )

        # ==========================================
        # Insert Rows
        # ==========================================

        for _, row in dataframe.iterrows():

            values = []

            for value in row:

                if value is None:

                    value = ""

                elif isinstance(
                    value,
                    float
                ):

                    value = f"{value:,.2f}"

                else:

                    value = str(value)

                values.append(value)

            tree.insert(
                "",
                "end",
                values=values
            )

        # ==========================================
        # Treeview Styling
        # ==========================================

        style = ttk.Style()

        try:

            style.theme_use(
                "clam"
            )

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