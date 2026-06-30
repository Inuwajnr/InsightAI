import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class ChartView(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            height=350
        )

        self.pack_propagate(False)

        # =====================================
        # Figure
        # =====================================

        self.figure = Figure(
            figsize=(10, 6),
            dpi=100,
            constrained_layout=True
        )

        self.ax = self.figure.add_subplot(111)

        # =====================================
        # Canvas
        # =====================================

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # =====================================
        # Navigation Toolbar
        # =====================================

        self.toolbar = NavigationToolbar2Tk(
            self.canvas,
            self,
            pack_toolbar=False
        )

        self.toolbar.update()

        self.toolbar.pack(
            fill="x",
            padx=5,
            pady=(0, 5)
        )

    # =====================================
    # Clear Chart
    # =====================================

    def clear(self):

        self.ax.clear()

        self.canvas.draw_idle()

    # =====================================
    # Draw Chart
    # =====================================

    def draw(self):

        self.canvas.draw_idle()

    # =====================================
    # Refresh
    # =====================================

    def refresh(self):

        self.canvas.draw_idle()

    # =====================================
    # Export Chart
    # =====================================

    def save_chart(self, filename):

        self.figure.savefig(
            filename,
            dpi=300,
            bbox_inches="tight",
            facecolor="white"
        )