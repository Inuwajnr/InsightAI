import customtkinter as ctk


class ProfilePanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=280,
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
            width=260,
            height=550
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

        print("\n===== PROFILE RECEIVED =====")
        print(profile)
        print("Numeric Columns:", profile.get("numeric_columns"))
        print("Numeric Names:", profile.get("numeric_column_names"))
        print("============================")

        text = f"""
📊 DATASET SUMMARY
────────────────────────

Rows:
{profile.get("rows", 0)}

Columns:
{profile.get("columns", 0)}

Numeric Columns:
{profile.get("numeric_columns", 0)}

Categorical Columns:
{profile.get("categorical_columns", 0)}

Duplicate Rows:
{profile.get("duplicate_rows", 0)}

Missing Values:
{profile.get("missing_values", 0)}

Memory Usage:
{profile.get("memory", 0)} KB

────────────────────────
NUMERIC COLUMNS
────────────────────────
"""

        numeric_cols = profile.get("numeric_column_names", [])

        if numeric_cols:
            for col in numeric_cols:
                text += f"\n• {col}"
        else:
            text += "\nNone"

        text += "\n\n────────────────────────\n"
        text += "CATEGORICAL COLUMNS\n"
        text += "────────────────────────\n"

        categorical_cols = profile.get("categorical_column_names", [])

        if categorical_cols:
            for col in categorical_cols:
                text += f"\n• {col}"
        else:
            text += "\nNone"

        text += "\n\n────────────────────────\n"
        text += "DATA TYPES\n"
        text += "────────────────────────\n"

        data_types = profile.get("data_types", {})

        for col, dtype in data_types.items():
            text += f"\n{col}: {dtype}"

        self.info_box.insert("1.0", text)

        self.info_box.configure(state="disabled")