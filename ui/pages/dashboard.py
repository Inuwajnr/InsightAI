import customtkinter as ctk

from ui.components.kpi_card import KPICard
from ui.components.chart_controls import ChartControls
from ui.components.chart_view import ChartView
from ui.components.data_grid import DataGrid
from ui.components.status_bar import StatusBar
from ui.components.profile_panel import ProfilePanel
from ui.components.quality_panel import QualityPanel


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ====================================
        # Header
        # ====================================

        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header_frame.pack(
            fill="x",
            pady=(5, 10)
        )

        title = ctk.CTkLabel(
            header_frame,
            text="📊 Data Analytics Dashboard",
            font=("Arial", 26, "bold")
        )

        title.pack(
            side="left",
            padx=15
        )

        self.sheet_dropdown = ctk.CTkOptionMenu(
            header_frame,
            values=["No Sheet Loaded"],
            width=220
        )

        self.sheet_dropdown.pack(
            side="right",
            padx=15
        )

        # ====================================
        # KPI Cards
        # ====================================

        self.kpi_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        self.kpi_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.rows_card = KPICard(
            self.kpi_frame,
            title="Rows",
            icon="📄",
            accent="#3B82F6"
        )

        self.rows_card.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.columns_card = KPICard(
            self.kpi_frame,
            title="Columns",
            icon="📋",
            accent="#8B5CF6"
        )

        self.columns_card.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.missing_card = KPICard(
            self.kpi_frame,
            title="Missing",
            icon="⚠️",
            accent="#F59E0B"
        )

        self.missing_card.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.memory_card = KPICard(
            self.kpi_frame,
            title="Memory",
            icon="💾",
            accent="#10B981"
        )

        self.memory_card.pack(
            side="left",
            padx=10,
            pady=10
        )

        # ====================================
        # Chart Controls
        # ====================================

        self.chart_controls = ChartControls(self)


        # ====================================
        # Visualization Area
        # ====================================

        visual_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        visual_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # -----------------------------
        # Chart (Left)
        # -----------------------------

        self.chart_view = ChartView(visual_frame)

        self.chart_view.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # -----------------------------
        # Right Side Panel
        # -----------------------------

        right_panel = ctk.CTkFrame(
            visual_frame,
            fg_color="transparent",
            width=320
        )

        right_panel.pack(
            side="right",
            fill="y"
        )

        # -----------------------------
        # Dataset Profile
        # -----------------------------

        self.profile_panel = ProfilePanel(
            right_panel
        )

        self.profile_panel.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )

        # -----------------------------
        # Data Quality
        # -----------------------------

        self.quality_panel = QualityPanel(
            right_panel
        )

        self.quality_panel.pack(
            fill="both",
            expand=True
        )

        # ====================================
        # Data Grid
        # ====================================

        self.data_grid = DataGrid(self)

        self.data_grid.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 5)
        )

        # ====================================
        # Status Bar
        # ====================================

        self.status_bar = StatusBar(self)

        self.status_bar.pack(
            fill="x",
            padx=10,
            pady=(5, 0)
        )