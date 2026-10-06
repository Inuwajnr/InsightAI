import os
import sys
import customtkinter as ctk
from PIL import Image


def resource_path(relative_path):
    """Get the correct resource path for development and PyInstaller."""

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

    return os.path.join(
        base_path,
        relative_path
    )


class AboutWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # ==============================
        # Window
        # ==============================

        self.title("About InsightAI Offline")
        self.geometry("520x650")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        # ==============================
        # Application Icon
        # ==============================

        icon_path = resource_path(
            r"assets\insightai.ico"
        )

        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        # ==============================
        # Main Container
        # ==============================

        container = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # ==============================
        # InsightAI Logo
        # ==============================

        logo_path = resource_path(
            r"assets\insightai_logo.png"
        )

        self.logo_image = None

        if os.path.exists(logo_path):

            try:
                logo = Image.open(logo_path)

                self.logo_image = ctk.CTkImage(
                    light_image=logo,
                    dark_image=logo,
                    size=(110, 110)
                )

                logo_label = ctk.CTkLabel(
                    container,
                    text="",
                    image=self.logo_image
                )

                logo_label.pack(
                    pady=(15, 2)
                )

            except Exception:
                self._create_fallback_logo(container)

        else:
            self._create_fallback_logo(container)

        # ==============================
        # Application Name
        # ==============================

        title = ctk.CTkLabel(
            container,
            text="InsightAI Offline",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(0, 5)
        )

        # ==============================
        # Version
        # ==============================

        version = ctk.CTkLabel(
            container,
            text="Version 1.0.0",
            font=ctk.CTkFont(
                size=14
            )
        )

        version.pack(
            pady=(0, 10)
        )

        # ==============================
        # Description
        # ==============================

        description = ctk.CTkLabel(
            container,
            text=(
                "An offline AI-powered data analysis "
                "and visualization desktop application."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            wraplength=400,
            justify="center"
        )

        description.pack(
            pady=(0, 10)
        )

        # ==============================
        # Features
        # ==============================

        features_title = ctk.CTkLabel(
            container,
            text="Key Features",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        features_title.pack(
            pady=(5, 8)
        )

        features = (
            "✓ Data Analysis\n"
            "✓ Data Cleaning\n"
            "✓ Data Visualization\n"
            "✓ Statistics\n"
            "✓ Pivot Tables\n"
            "✓ Correlation Analysis\n"
            "✓ Offline AI Chat\n"
            "✓ Document Assistant"
        )

        features_label = ctk.CTkLabel(
            container,
            text=features,
            font=ctk.CTkFont(
                size=13
            ),
            justify="left"
        )

        features_label.pack(
            pady=(0, 15)
        )

        # ==============================
        # Technology
        # ==============================

        technology = ctk.CTkLabel(
            container,
            text=(
                "Powered by local/offline processing\n"
                "and Ollama + Qwen3."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            justify="center"
        )

        technology.pack(
            pady=(5, 10)
        )

        # ==============================
        # Copyright
        # ==============================

        copyright_label = ctk.CTkLabel(
            container,
            text="© 2026 InsightAI Offline. All rights reserved. BY: INUWA JOONIOR",
            font=ctk.CTkFont(
                size=12
            )
        )

        copyright_label.pack(
            pady=(5, 10)
        )

        # ==============================
        # Close Button
        # ==============================

        close_button = ctk.CTkButton(
            container,
            text="Close",
            width=140,
            height=38,
            command=self.destroy
        )

        close_button.pack(
            pady=(5, 15)
        )

    # ==============================
    # Fallback Logo
    # ==============================

    def _create_fallback_logo(self, container):

        logo_label = ctk.CTkLabel(
            container,
            text="◈",
            font=ctk.CTkFont(
                size=52,
                weight="bold"
            )
        )

        logo_label.pack(
            pady=(25, 5)
        )