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

        self.dataset_status = ctk.CTkLabel(
            status_frame,
            text="",
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

        # ------------------------------------------------------
        # Load current dataset information
        # ------------------------------------------------------

        self.refresh_dataset_context(
            show_welcome=True
        )

    # ==========================================================
    # Refresh Dataset Context
    # ==========================================================

    def refresh_dataset_context(
        self,
        show_welcome=False
    ):
        """
        Refresh the dataset information and suggested questions.

        This allows the AI Chat window to update when the user
        loads a different dataset.
        """

        df = self.master.current_df

        # ------------------------------------------------------
        # No dataset
        # ------------------------------------------------------

        if df is None:

            self.dataset_status.configure(
                text="⚠ No dataset loaded"
            )

            if show_welcome:

                self._replace_chat_content(
                    "🤖 InsightAI\n\n"
                    "Hello! I can help you analyze your "
                    "dataset completely offline.\n\n"
                    "Please upload a dataset first."
                )

            return

        # ------------------------------------------------------
        # Dataset information
        # ------------------------------------------------------

        rows = len(df)

        columns = len(
            df.columns
        )

        status_text = (
            f"📊 Dataset loaded  •  "
            f"{rows:,} rows  •  "
            f"{columns:,} columns"
        )

        self.dataset_status.configure(
            text=status_text
        )

        # ------------------------------------------------------
        # Generate dataset-aware suggestions
        # ------------------------------------------------------

        suggestions = self._generate_suggestions(
            df
        )

        welcome_text = (
            "🤖 InsightAI\n\n"
            "Hello! I can help you analyze your "
            "currently loaded dataset completely offline.\n\n"
            "Try asking:\n"
            + "\n".join(
                f"• {question}"
                for question in suggestions
            )
        )

        if show_welcome:

            self._replace_chat_content(
                welcome_text
            )

        else:

            # When dataset changes, refresh the
            # suggestion section without deleting
            # previous conversation messages.
            self._replace_suggestions(
                suggestions
            )

    # ==========================================================
    # Generate Dynamic Suggestions
    # ==========================================================

    def _generate_suggestions(
        self,
        df
    ):
        """
        Generate useful questions based on the actual
        columns in the currently loaded dataset.
        """

        suggestions = []

        columns = list(
            df.columns
        )

        numeric_columns = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        categorical_columns = list(
            df.select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            ).columns
        )

        # ------------------------------------------------------
        # Always useful
        # ------------------------------------------------------

        suggestions.append(
            "How many rows are in the dataset?"
        )

        suggestions.append(
            "What are the columns in this dataset?"
        )

        # ------------------------------------------------------
        # Missing values
        # ------------------------------------------------------

        if df.isna().sum().sum() > 0:

            suggestions.append(
                "Which columns have missing values?"
            )

        else:

            suggestions.append(
                "Does this dataset contain any missing values?"
            )

        # ------------------------------------------------------
        # Numeric columns
        # ------------------------------------------------------

        if numeric_columns:

            numeric_col = str(
                numeric_columns[0]
            )

            suggestions.append(
                f"What is the total {numeric_col}?"
            )

            suggestions.append(
                f"What is the highest {numeric_col}?"
            )

            if len(numeric_columns) >= 2:

                suggestions.append(
                    f"What is the correlation between "
                    f"{numeric_columns[0]} and "
                    f"{numeric_columns[1]}?"
                )

        # ------------------------------------------------------
        # Categorical columns
        # ------------------------------------------------------

        if categorical_columns:

            category_col = str(
                categorical_columns[0]
            )

            suggestions.append(
                f"What are the most common values in "
                f"{category_col}?"
            )

            suggestions.append(
                f"Show me the number of records for each "
                f"{category_col}."
            )

        # ------------------------------------------------------
        # Group analysis
        # ------------------------------------------------------

        if categorical_columns and numeric_columns:

            group_col = str(
                categorical_columns[0]
            )

            value_col = str(
                numeric_columns[0]
            )

            suggestions.append(
                f"Which {group_col} has the highest "
                f"{value_col}?"
            )

        # ------------------------------------------------------
        # General AI question
        # ------------------------------------------------------

        suggestions.append(
            "What stands out in this dataset?"
        )

        # ------------------------------------------------------
        # Remove duplicates
        # ------------------------------------------------------

        unique_suggestions = []

        for question in suggestions:

            if question not in unique_suggestions:

                unique_suggestions.append(
                    question
                )

        # Keep the panel readable.
        return unique_suggestions[:9]

    # ==========================================================
    # Replace Entire Chat Content
    # ==========================================================

    def _replace_chat_content(
        self,
        content
    ):

        self.chat_box.configure(
            state="normal"
        )

        self.chat_box.delete(
            "1.0",
            "end"
        )

        self.chat_box.insert(
            "1.0",
            content
        )

        self.chat_box.configure(
            state="disabled"
        )

        self.chat_box.see(
            "1.0"
        )

    # ==========================================================
    # Replace Suggestions
    # ==========================================================

    def _replace_suggestions(
        self,
        suggestions
    ):
        """
        Refresh only the suggestion area.

        If the user already has a conversation open, we don't
        erase the conversation.
        """

        self.chat_box.configure(
            state="normal"
        )

        content = self.chat_box.get(
            "1.0",
            "end"
        )

        marker = "Try asking:\n"

        if marker in content:

            before = content.split(
                marker,
                1
            )[0]

            new_content = (
                before
                + marker
                + "\n".join(
                    f"• {question}"
                    for question in suggestions
                )
                + "\n"
            )

            self.chat_box.delete(
                "1.0",
                "end"
            )

            self.chat_box.insert(
                "1.0",
                new_content
            )

        self.chat_box.configure(
            state="disabled"
        )

    # ==========================================================
    # Send Question
    # ==========================================================

    def send_question(self):

        question = (
            self.question_entry
            .get()
            .strip()
        )

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