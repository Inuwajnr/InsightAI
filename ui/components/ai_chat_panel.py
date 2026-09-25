import customtkinter as ctk

from data.offline_ai import OfflineAIEngine


class AIChatPanel(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.title("🤖 AI Chat")
        self.geometry("950x700")
        self.minsize(750, 550)

        # Offline AI engine
        self.ai_engine = OfflineAIEngine()

        self._build_ui()

    # ==========================================================
    # Build UI
    # ==========================================================

    def _build_ui(self):

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        header = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="🤖 AI Chat",
            font=("Arial", 24, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Ask questions about your currently loaded dataset.",
            font=("Arial", 13)
        )

        subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # Dataset Status
        # ------------------------------------------------------

        status_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        status_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        if self.master.current_df is not None:

            rows = len(
                self.master.current_df
            )

            columns = len(
                self.master.current_df.columns
            )

            status_text = (
                f"📊 Dataset loaded  •  "
                f"{rows:,} rows  •  "
                f"{columns:,} columns"
            )

        else:

            status_text = (
                "⚠ No dataset loaded"
            )

        self.dataset_status = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=("Arial", 13, "bold")
        )

        self.dataset_status.pack(
            anchor="w",
            padx=20,
            pady=12
        )

        # ------------------------------------------------------
        # Chat Area
        # ------------------------------------------------------

        self.chat_box = ctk.CTkTextbox(
            self,
            wrap="word",
            font=("Arial", 13)
        )

        self.chat_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.chat_box.insert(
            "1.0",
            "🤖 InsightAI\n\n"
            "Hello! I can help you analyze your "
            "currently loaded dataset completely offline.\n\n"
            "Try asking:\n"
            "• How many rows are in the dataset?\n"
            "• How many columns are there?\n"
            "• Which columns have missing values?\n"
            "• What are the numeric columns?\n"
            "• What are the categorical columns?\n"
            "• What is the total billing amount?\n"
            "• What is the highest billing amount?\n"
            "• What is the most common condition?\n"
            "• How many males are there?\n"
            "• Show billing by hospital.\n"
        )

        self.chat_box.configure(
            state="disabled"
        )

        # ------------------------------------------------------
        # Input Area
        # ------------------------------------------------------

        input_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.question_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask InsightAI about your dataset...",
            height=42
        )

        self.question_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 10),
            pady=15
        )

        self.send_button = ctk.CTkButton(
            input_frame,
            text="Send ➤",
            width=120,
            command=self.send_question
        )

        self.send_button.pack(
            side="right",
            padx=(0, 15),
            pady=15
        )

        self.question_entry.bind(
            "<Return>",
            lambda event: self.send_question()
        )

        self.question_entry.focus()

    # ==========================================================
    # Send Question
    # ==========================================================

    def send_question(self):

        question = self.question_entry.get().strip()

        if not question:
            return

        # Show user's question
        self._add_message(
            "You",
            question
        )

        # Clear input
        self.question_entry.delete(
            0,
            "end"
        )

        # Get offline AI answer
        answer = self.answer_question(
            question
        )

        # Show AI response
        self._add_message(
            "InsightAI",
            answer
        )

    # ==========================================================
    # Add Chat Message
    # ==========================================================

    def _add_message(
        self,
        sender,
        message
    ):

        self.chat_box.configure(
            state="normal"
        )

        self.chat_box.insert(
            "end",
            f"\n{sender}:\n"
        )

        self.chat_box.insert(
            "end",
            f"{message}\n\n"
        )

        self.chat_box.see(
            "end"
        )

        self.chat_box.configure(
            state="disabled"
        )

    # ==========================================================
    # Answer Question
    # ==========================================================

    def answer_question(
        self,
        question
    ):

        df = self.master.current_df

        if df is None:

            return (
                "There is currently no dataset loaded. "
                "Please upload a dataset first."
            )

        # Send the question to the offline AI engine
        return self.ai_engine.answer(
            df,
            question
        )