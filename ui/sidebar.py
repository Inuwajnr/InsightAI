import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=250
        )

        self.pack(
            side="left",
            fill="y"
        )

        # =====================================
        # Logo / Title
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="InsightAI Offline",
            font=("Arial", 22, "bold")
        )

        title.pack(
            pady=20
        )

        # =====================================
        # Upload Dataset
        # =====================================

        self.upload_btn = ctk.CTkButton(
            self,
            text="📂 Upload Dataset",
            command=master.upload_file
        )

        self.upload_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # Merge Data
        # =====================================

        self.merge_btn = ctk.CTkButton(
            self,
            text="🔗 Merge Data",
            command=master.open_merge_panel
        )

        self.merge_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # Clean Data
        # =====================================

        self.clean_btn = ctk.CTkButton(
            self,
            text="🧹 Clean Data",
            command=master.clean_data
        )

        self.clean_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # Dataset Statistics
        # =====================================

        self.statistics_btn = ctk.CTkButton(
            self,
            text="📈 Statistics",
            command=master.show_statistics
        )

        self.statistics_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        self.correlation_btn = ctk.CTkButton(
            self,
            text="🔥 Correlation",
            command=master.show_correlation
        )

        self.correlation_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # Data Analysis
        # =====================================

        self.analysis_btn = ctk.CTkButton(
            self,
            text="📊 Data Analysis"
        )

        self.analysis_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # Document Assistant
        # =====================================

        self.docs_btn = ctk.CTkButton(
            self,
            text="📄 Document Assistant"
        )

        self.docs_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # AI Chat
        # =====================================

        self.chat_btn = ctk.CTkButton(
            self,
            text="🤖 AI Chat"
        )

        self.chat_btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =====================================
        # Spacer
        # =====================================

        ctk.CTkLabel(
            self,
            text=""
        ).pack(
            expand=True
        )

        # =====================================
        # Version
        # =====================================

        version = ctk.CTkLabel(
            self,
            text="InsightAI v1.0",
            font=("Arial", 11)
        )

        version.pack(
            pady=15
        )