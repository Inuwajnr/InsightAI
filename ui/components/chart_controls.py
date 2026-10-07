import customtkinter as ctk


class ChartControls(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.pack(
            fill="x",
            padx=20,
            pady=10
        )

        top_row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        top_row.pack(
            fill="x",
            pady=(5, 0)
        )

        # ----------------------------------------
        # X Axis
        # ----------------------------------------

        ctk.CTkLabel(
            top_row,
            text="X Axis"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.x_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=["Select X"],
            width=100
        )

        self.x_dropdown.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------
        # Y Axis
        # ----------------------------------------

        ctk.CTkLabel(
            top_row,
            text="Y Axis"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.y_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=["Select Y"],
            width=100
        )

        self.y_dropdown.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------
        # Chart Type
        # ----------------------------------------

        ctk.CTkLabel(
            top_row,
            text="Chart"
        ).pack(
            side="left",
            padx=(10, 5)
        )

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
            width=100,
            command=self.update_color_controls
        )

        self.chart_dropdown.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------
        # Time Grain
        # ----------------------------------------

        ctk.CTkLabel(
            top_row,
            text="Time Grain"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.time_grain_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=[
                "Auto",
                "Daily",
                "Weekly",
                "Monthly",
                "Quarterly",
                "Yearly"
            ],
            width=100
        )

        self.time_grain_dropdown.pack(
            side="left",
            padx=5
        )

        self.time_grain_dropdown.set(
            "Monthly"
        )

        # ----------------------------------------
        # Date Range
        # ----------------------------------------

        ctk.CTkLabel(
            top_row,
            text="Date Range"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.date_range_dropdown = ctk.CTkOptionMenu(
            top_row,
            values=[
                "All Time",
                "Last 3 Months",
                "Last 6 Months",
                "Last 12 Months"
            ],
            width=100
        )

        self.date_range_dropdown.pack(
            side="left",
            padx=5
        )

        self.date_range_dropdown.set(
            "All Time"
        )

        # ----------------------------------------
        # Top
        # ----------------------------------------

        ctk.CTkLabel(
            top_row,
            text="Top"
        ).pack(
            side="left",
            padx=(10, 5)
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
            width=100
        )

        self.top_dropdown.pack(
            side="left",
            padx=5
        )

        self.top_dropdown.set(
            "10"
        )
        # ----------------------------------------
        # Chart Action Row
        # ----------------------------------------

        bottom_row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom_row.pack(
            fill="x",
            pady=(10, 0)
        )

        # ----------------------------------------
        # Color
        # ----------------------------------------

        self.color_label = ctk.CTkLabel(
            bottom_row,
            text="Color"
        )
        self.color_label.pack(
            side="left",
            padx=(10, 5)
        )

        self.color_dropdown = ctk.CTkOptionMenu(
            bottom_row,
            values=[
                "Blue",
                "Green",
                "Red",
                "Orange",
                "Purple",
                "Black",
                "Cyan",
                "Magenta",
                "Yellow",
                "Gray",
                "Brown",
                "Pink",
                "Teal",
                "Lime",
                "Indigo",
                "Violet",
                "Gold",
                "Silver",
                "Maroon",
                "Olive",
                "Navy",
                "Turquoise",
                "Coral",
                "Salmon",
                "Chocolate",
                "Tan",
                "Plum",
                "Lavender",
                "Mint",
                "Peach",
                "Sky Blue",
                "Sea Green",
                "Crimson",
                "Slate Gray",
                "Khaki",
                "Orchid",
                "Periwinkle",
                "Rose",
                "Sienna",
                "Amber",
                "Azure",
                "Emerald",
                "Ruby",
                "Topaz",
                "Cobalt",
                "Jade",
                "Onyx",
                "Pearl",
            ],
            width=100
        )

        self.color_dropdown.pack(
            side="left",
            padx=5
        )

        self.color_dropdown.set(
            "Blue"
        )

        # ----------------------------------------
        # Pie Chart Palette
        # ----------------------------------------

        self.palette_label = ctk.CTkLabel(
            bottom_row,
            text="Palette"
        )
        self.palette_label.pack(
            side="left",
            padx=(15, 5)
        )

        self.palette_dropdown = ctk.CTkOptionMenu(
            bottom_row,
            values=[
                "Default",
                "Ocean",
                "Nature",
                "Warm",
                "Purple",
                "Monochrome"
            ],
            width=120
        )

        self.palette_dropdown.pack(
            side="left",
            padx=5
        )

        self.palette_dropdown.set(
            "Default"
        )

        # ----------------------------------------
        # Generate
        # ----------------------------------------

        self.generate_btn = ctk.CTkButton(
            bottom_row,
            text="Generate",
            width=100
        )

        self.generate_btn.pack(
            side="left",
            padx=(15, 8)
        )

        # ----------------------------------------
        # Apply Color
        # ----------------------------------------

        self.apply_color_btn = ctk.CTkButton(
            bottom_row,
            text="Apply Color",
            width=100
        )

        self.apply_color_btn.pack(
            side="left",
            padx=(0, 10)
        )

        # ----------------------------------------
        # Export
        # ----------------------------------------

        self.export_btn = ctk.CTkButton(
            bottom_row,
            text="Export PNG",
            width=100
        )

        self.export_btn.pack(
            side="left"
        )

        # ----------------------------------------
        # AI Recommendation
        # ----------------------------------------

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

    def set_recommendation(self, text):

        self.recommendation_label.configure(
            text=text
        )

        self.update_color_controls(
            self.chart_dropdown.get()
        )

    def update_color_controls(self, chart_type):

        if chart_type == "Pie Chart":

            # Hide normal color controls
            self.color_label.pack_forget()
            self.color_dropdown.pack_forget()

            # Show pie palette controls
            self.palette_label.pack(
                side="left",
                padx=(15, 5)
            )

            self.palette_dropdown.pack(
                side="left",
                padx=5
            )

        else:

            # Hide pie palette controls
            self.palette_label.pack_forget()
            self.palette_dropdown.pack_forget()

            # Show normal color controls
            self.color_label.pack(
                side="left",
                padx=(15, 5)
            )

            self.color_dropdown.pack(
                side="left",
                padx=5
            )

        