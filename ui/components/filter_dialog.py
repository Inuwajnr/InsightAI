import customtkinter as ctk


class FilterDialog(ctk.CTkToplevel):

    def __init__(self, master, df, filters):

        super().__init__(master)

        self.df = df
        self.filters = filters
        self.result = {}

        self.title("Pivot Filters")
        self.geometry("400x500")

        self.dropdown_widgets = {}

        ctk.CTkLabel(
            self,
            text="Select Filter Values",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )

        # -------------------------
        # Create one dropdown
        # for each selected filter
        # -------------------------

        for field in filters:

            ctk.CTkLabel(
                self,
                text=field
            ).pack(
                anchor="w",
                padx=20,
                pady=(10, 2)
            )

            values = sorted(
                self.df[field]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            combo = ctk.CTkOptionMenu(
                self,
                values=values
            )

            combo.pack(
                fill="x",
                padx=20
            )

            self.dropdown_widgets[field] = combo

        ctk.CTkButton(
            self,
            text="Apply Filters",
            command=self.apply_filters
        ).pack(
            pady=20
        )

    def apply_filters(self):

        for field, widget in self.dropdown_widgets.items():

            self.result[field] = widget.get()

        self.destroy()