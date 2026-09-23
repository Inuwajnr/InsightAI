import customtkinter as ctk


class ProfilePanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=340,
            height=420,
            corner_radius=12
        )

        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="Dataset Profile",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=(15, 10)
        )

        self.info_box = ctk.CTkTextbox(
            self,
            width=320,
            height=300
        )

        self.info_box.pack(
            padx=10,
            pady=10,
            fill="both",
            expand=True
        )

        self.info_box.configure(state="disabled")

    def update_profile(self, profile):

        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", "end")

        memory = profile.get("memory", 0)

        if memory >= 1024:
            memory_text = f"{memory / 1024:.2f} GB"
        else:
            memory_text = f"{memory:.2f} MB"

        text = f"""
    📊 DATASET SUMMARY
    ────────────────────────

    Rows: {profile.get("rows", 0):,}

    Columns: {profile.get("columns", 0)}

    Numeric Columns: {profile.get("numeric_columns", 0)}

    Categorical Columns: {profile.get("categorical_columns", 0)}

    Missing Values: {profile.get("missing_values", 0)}

    Duplicate Rows: {profile.get("duplicate_rows", 0)}

    Memory Usage: {memory_text}

    ────────────────────────
    NUMERIC COLUMNS
    ────────────────────────
    """

        numeric_cols = profile.get(
            "numeric_column_names",
            []
        )

        if numeric_cols:

            for col in numeric_cols[:10]:

                text += f"\n• {col}"

            if len(numeric_cols) > 10:

                text += (
                    f"\n\n+{len(numeric_cols) - 10} more..."
                )

        else:

            text += "\nNone"

        text += """



    ────────────────────────
    CATEGORICAL COLUMNS
    ────────────────────────
    """

        categorical_cols = profile.get(
            "categorical_column_names",
            []
        )

        if categorical_cols:

            for col in categorical_cols[:10]:

                text += f"\n• {col}"

            if len(categorical_cols) > 10:

                text += (
                    f"\n\n+{len(categorical_cols) - 10} more..."
                )

        else:

            text += "\nNone"

        self.info_box.insert(
            "1.0",
            text
        )

        self.info_box.configure(
            state="disabled"
        )