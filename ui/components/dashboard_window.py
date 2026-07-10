import customtkinter as ctk


class DashboardWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("InsightAI Dashboard")

        self.geometry("1400x850")

        self.minsize(1200, 700)

        self.configure(fg_color="#F5F7FA")

        self.build_ui()

    # ==================================
    # BUILD UI
    # ==================================

    def build_ui(self):

        # -----------------------------
        # Header
        # -----------------------------

        header = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        title = ctk.CTkLabel(
            header,
            text="InsightAI Dashboard",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            side="left",
            padx=25,
            pady=18
        )

        # -----------------------------
        # KPI Area
        # -----------------------------

        self.kpi_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.kpi_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        # -----------------------------
        # Dashboard Canvas
        # -----------------------------

        self.canvas_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF"
        )

        self.canvas_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )