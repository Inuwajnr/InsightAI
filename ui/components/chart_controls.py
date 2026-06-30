import customtkinter as ctk


class ChartControls(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        # ====================================
        # Main Container
        # ====================================

        self.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ====================================
        # Top Row
        # ====================================

        top_row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top_row.pack(
            fill="x",
            pady=(5, 0)
        )

        # --------------------
        # X Axis
        # --------------------

        ctk.CTkLabel(
            top_row,
            text="X Axis"
        ).pack(side="left", padx=(10, 5))

        self.x_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=["Select X"],
            width=170
        )

        self.x_dropdown.pack(side="left", padx=5)

        # --------------------
        # Y Axis
        # --------------------

        ctk.CTkLabel(
            top_row,
            text="Y Axis"
        ).pack(side="left", padx=(15, 5))

        self.y_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=["Select Y"],
            width=170
        )

        self.y_dropdown.pack(side="left", padx=5)

        # --------------------
        # Chart Type
        # --------------------

        ctk.CTkLabel(
            top_row,
            text="Chart"
        ).pack(side="left", padx=(15, 5))

        self.chart_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=[
                "Bar Chart",
                "Column Chart",
                "Line Chart",
                "Scatter Plot",
                "Pie Chart",
                "Histogram"
            ],
            width=170
        )

        self.chart_dropdown.pack(side="left", padx=5)

        # --------------------
        # Top N
        # --------------------

        ctk.CTkLabel(
            top_row,
            text="Top"
        ).pack(
            side="left",
            padx=(15, 5)
        )

        self.top_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=[
                "5",
                "10",
                "15",
                "20",
                "All"
            ],
            width=80
        )

        self.top_dropdown.pack(
            side="left",
            padx=5
        )

        self.top_dropdown.set("10")
        # --------------------
        # Buttons
        # --------------------

        self.generate_btn = ctk.CTkButton(
            top_row,
            text="Generate",
            width=120
        )

        self.generate_btn.pack(side="left", padx=(20, 10))

        self.export_btn = ctk.CTkButton(
            top_row,
            text="Export PNG",
            width=120
        )

        self.export_btn.pack(side="left")

        # ====================================
        # Recommendation Section
        # ====================================

        recommendation_frame = ctk.CTkFrame(
            self,
            corner_radius=8
        )

        recommendation_frame.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        self.recommendation_title = ctk.CTkLabel(
            recommendation_frame,
            text="💡 AI Recommendation",
            font=("Arial", 14, "bold")
        )

        self.recommendation_title.pack(
            anchor="w",
            padx=12,
            pady=(8, 2)
        )

        self.recommendation_label = ctk.CTkLabel(
            recommendation_frame,
            text="Upload a dataset to receive chart recommendations.",
            justify="left",
            wraplength=900
        )

        self.recommendation_label.pack(
            anchor="w",
            padx=12,
            pady=(0, 8)
        )

    # ====================================
    # Update Recommendation
    # ====================================

    def set_recommendation(self, text):

        self.recommendation_label.configure(
            text=text
        )