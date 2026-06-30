import customtkinter as ctk


class KPICard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        title,
        value="0",
        icon="📊",
        accent="#3B82F6"
    ):
        super().__init__(
            master,
            corner_radius=15,
            width=190,
            height=110,
            border_width=2,
            border_color=accent
        )

        self.pack_propagate(False)

        # ====================================
        # Top Row
        # ====================================

        top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top_frame.pack(
            fill="x",
            padx=12,
            pady=(10, 0)
        )

        self.icon_label = ctk.CTkLabel(
            top_frame,
            text=icon,
            font=("Arial", 22)
        )

        self.icon_label.pack(
            side="left"
        )

        self.title_label = ctk.CTkLabel(
            top_frame,
            text=title,
            font=("Arial", 14)
        )

        self.title_label.pack(
            side="left",
            padx=(8, 0)
        )

        # ====================================
        # Value
        # ====================================

        self.value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Arial", 30, "bold"),
            text_color=accent
        )

        self.value_label.pack(
            expand=True
        )

    # ====================================
    # Update KPI
    # ====================================

    def update_value(self, value):

        self.value_label.configure(
            text=str(value)
        )

    # ====================================
    # Get Value
    # ====================================

    def get_value(self):

        return self.value_label.cget("text")