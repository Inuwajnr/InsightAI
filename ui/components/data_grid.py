import customtkinter as ctk
from tksheet import Sheet


class DataGrid(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        self.sheet = Sheet(self)

        self.sheet.enable_bindings((
            "single_select",
            "row_select",
            "column_select",
            "arrowkeys",
            "right_click_popup_menu",
            "rc_select",
            "copy",
            "select_all",
        ))

        self.sheet.pack(
            fill="both",
            expand=True
        )

    def load_dataframe(self, df):

        self.sheet.headers(
            list(df.columns)
        )

        self.sheet.set_sheet_data(
            df.values.tolist()
        )