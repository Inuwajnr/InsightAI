import customtkinter as ctk


class QualityPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=320,
            corner_radius=12
        )

        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="🛡 Data Quality Center",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=(15, 10)
        )

        self.score_label = ctk.CTkLabel(
            self,
            text="Quality Score: --",
            font=("Arial", 16, "bold"),
            text_color="#2E86DE"
        )

        self.score_label.pack(
            pady=(5, 15)
        )

        self.info_box = ctk.CTkTextbox(
            self,
            width=260,
            height=650
        )

        self.info_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.info_box.configure(state="disabled")

    def update_quality(self, quality):

        score = quality["score"]

        if score >= 90:
            color = "#22C55E"      # Green
            status = "🟢 Excellent"

        elif score >= 70:
            color = "#F59E0B"      # Orange
            status = "🟡 Good"

        else:
            color = "#EF4444"      # Red
            status = "🔴 Needs Attention"

        self.score_label.configure(
            text=f"{status}\nQuality Score: {score}/100",
            text_color=color
        )

        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", "end")

        text = f"""
Rows:
{quality['rows']}

Columns:
{quality['columns']}

Missing Values:
{quality['missing']}

Duplicate Rows:
{quality['duplicates']}

Constant Columns:
{quality['constant_columns']}

Recommendations
-----------------------------
"""

        for item in quality["recommendations"]:
            text += f"\n• {item}"

        self.info_box.insert(
            "1.0",
            text
        )

        self.info_box.configure(state="disabled")