import os
import customtkinter as ctk
from tkinter import filedialog, messagebox


class DocumentAssistantPanel(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.current_file = None
        self.document_text = ""
        self.document_page_count = 0

        self.title("📄 Document Assistant")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self._build_ui()

    # ==========================================================
    # UI
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
            text="📄 Document Assistant",
            font=("Arial", 24, "bold")
        )
        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Open and inspect documents locally and offline.",
            font=("Arial", 13)
        )
        subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # File controls
        # ------------------------------------------------------

        controls = ctk.CTkFrame(
            self,
            corner_radius=10
        )
        controls.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.open_button = ctk.CTkButton(
            controls,
            text="📂 Open Document",
            width=160,
            command=self.open_document
        )
        self.open_button.pack(
            side="left",
            padx=(15, 10),
            pady=15
        )

        self.file_label = ctk.CTkLabel(
            controls,
            text="No document loaded",
            anchor="w"
        )
        self.file_label.pack(
            side="left",
            padx=10,
            pady=15
        )


        # ------------------------------------------------------
        # Document Information
        # ------------------------------------------------------

        self.info_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        self.info_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.info_title = ctk.CTkLabel(
            self.info_frame,
            text="📊 Document Information",
            font=("Arial", 15, "bold")
        )

        self.info_title.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=15,
            pady=(10, 5),
            sticky="w"
        )

        self.file_type_label = ctk.CTkLabel(
            self.info_frame,
            text="Type: —"
        )

        self.file_type_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        self.file_size_label = ctk.CTkLabel(
            self.info_frame,
            text="Size: —"
        )

        self.file_size_label.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        self.words_label = ctk.CTkLabel(
            self.info_frame,
            text="Words: —"
        )

        self.words_label.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        self.characters_label = ctk.CTkLabel(
            self.info_frame,
            text="Characters: —"
        )

        self.characters_label.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        self.lines_label = ctk.CTkLabel(
            self.info_frame,
            text="Lines: —"
        )

        self.lines_label.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        self.pages_label = ctk.CTkLabel(
            self.info_frame,
            text="Pages: —"
        )

        self.pages_label.grid(
            row=2,
            column=1,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        self.status_label = ctk.CTkLabel(
            self.info_frame,
            text="Status: No document loaded"
        )

        self.status_label.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=15,
            pady=(0, 10),
            sticky="w"
        )

        # ------------------------------------------------------
        # Main content area
        # ------------------------------------------------------

        content = ctk.CTkFrame(
            self,
            corner_radius=10
        )
        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # Left tools panel
        # ------------------------------------------------------

        tools = ctk.CTkFrame(
            content,
            width=220,
            corner_radius=10
        )
        tools.pack(
            side="left",
            fill="y",
            padx=(10, 5),
            pady=10
        )

        tools.pack_propagate(False)

        tools_title = ctk.CTkLabel(
            tools,
            text="Document Tools",
            font=("Arial", 17, "bold")
        )
        tools_title.pack(
            pady=(20, 20)
        )

        self.search_button = ctk.CTkButton(
            tools,
            text="🔎 Search",
            state="disabled",
            command=self.search_document
        )
        self.search_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.summary_button = ctk.CTkButton(
            tools,
            text="📝 Summarize",
            state="disabled",
            command=self.summarize_document
        )
        self.summary_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.question_button = ctk.CTkButton(
            tools,
            text="❓ Ask Question",
            state="disabled",
            command=self.ask_question
        )
        self.question_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.export_button = ctk.CTkButton(
            tools,
            text="💾 Export",
            state="disabled",
            command=self.export_document
        )
        self.export_button.pack(
            fill="x",
            padx=20,
            pady=8
        )

        # ------------------------------------------------------
        # Document preview
        # ------------------------------------------------------

        preview = ctk.CTkFrame(
            content,
            corner_radius=10
        )
        preview.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 10),
            pady=10
        )

        preview_title = ctk.CTkLabel(
            preview,
            text="Document Preview",
            font=("Arial", 17, "bold")
        )
        preview_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        self.text_box = ctk.CTkTextbox(
            preview,
            wrap="word",
            font=("Consolas", 13)
        )
        self.text_box.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.text_box.insert(
            "1.0",
            "Open a document to view its contents here."
        )

    # ==========================================================
    # Open Document
    # ==========================================================

    def open_document(self):

        file_path = filedialog.askopenfilename(
            title="Open Document",
            filetypes=[
                (
                    "Supported Documents",
                    "*.txt *.docx *.pdf"
                ),
                (
                    "Text Files",
                    "*.txt"
                ),
                (
                    "Word Documents",
                    "*.docx"
                ),
                (
                    "PDF Documents",
                    "*.pdf"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            extension = os.path.splitext(
                file_path
            )[1].lower()

            if extension == ".txt":
                text = self._read_txt(file_path)

            elif extension == ".docx":
                text = self._read_docx(file_path)

            elif extension == ".pdf":
                text = self._read_pdf(file_path)

            else:
                messagebox.showwarning(
                    "Unsupported File",
                    "Please select a TXT, DOCX, or PDF file."
                )
                return

            self.current_file = file_path
            self.document_text = text

            self.update_document_information(
                file_path
            )

            self.file_label.configure(
                text=os.path.basename(file_path)
            )

            self.text_box.delete(
                "1.0",
                "end"
            )

            self.text_box.insert(
                "1.0",
                text
            )

            self.search_button.configure(
                state="normal"
            )

            self.export_button.configure(
                state="normal"
            )

            self.summary_button.configure(
                state="normal"
            )

            self.question_button.configure(
                state="normal"
            )

        except Exception as e:

            messagebox.showerror(
                "Document Error",
                f"Unable to open document.\n\n{e}"
            )

    # ==========================================================
    # TXT
    # ==========================================================

    def _read_txt(self, file_path):

        self.document_page_count = 0

        encodings = [
            "utf-8",
            "utf-8-sig",
            "latin-1"
        ]

        for encoding in encodings:

            try:

                with open(
                    file_path,
                    "r",
                    encoding=encoding
                ) as file:

                    return file.read()

            except UnicodeDecodeError:
                continue

        raise ValueError(
            "Unable to decode the text file."
        )

    # ==========================================================
    # DOCX
    # ==========================================================

    def _read_docx(self, file_path):

        self.document_page_count = 0

        try:

            from docx import Document

        except ImportError:

            raise ImportError(
                "python-docx is not installed.\n\n"
                "Install it with:\n"
                "pip install python-docx"
            )

        document = Document(
            file_path
        )

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n\n".join(
            paragraphs
        )

    # ==========================================================
    # PDF
    # ==========================================================

    def _read_pdf(self, file_path):

        try:

            import pypdf

        except ImportError:

            raise ImportError(
                "pypdf is not installed.\n\n"
                "Install it with:\n"
                "pip install pypdf"
            )

        reader = pypdf.PdfReader(
            file_path
        )

        self.document_page_count = len(
            reader.pages
        )

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(
            pages
        )

    def summarize_document(self):

        if not self.document_text.strip():
            messagebox.showwarning(
                "Summarize Document",
                "Please open a document first."
            )
            return

        text = self.document_text.strip()

        # ----------------------------------------------------------
        # Split document into sentences
        # ----------------------------------------------------------

        import re
        from collections import Counter

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        sentences = [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

        if not sentences:
            messagebox.showwarning(
                "Summarize Document",
                "No readable text was found in the document."
            )
            return

        # ----------------------------------------------------------
        # Very short document
        # ----------------------------------------------------------

        if len(sentences) <= 5:

            summary = "\n\n".join(sentences)

            self._show_summary_window(
                summary,
                len(sentences)
            )

            return

        # ----------------------------------------------------------
        # Word frequency
        # ----------------------------------------------------------

        stop_words = {
            "the", "a", "an", "and", "or", "but",
            "if", "then", "than", "is", "are", "was",
            "were", "be", "been", "being", "to",
            "of", "in", "on", "for", "with", "as",
            "by", "at", "from", "this", "that",
            "these", "those", "it", "its", "they",
            "their", "them", "he", "she", "his",
            "her", "we", "our", "you", "your",
            "i", "me", "my", "not", "can", "will",
            "would", "should", "could", "has",
            "have", "had", "do", "does", "did",
            "which", "who", "what", "when", "where",
            "why", "how"
        }

        words = re.findall(
            r'\b[a-zA-Z]{3,}\b',
            text.lower()
        )

        words = [
            word
            for word in words
            if word not in stop_words
        ]

        frequencies = Counter(words)

        if not frequencies:
            messagebox.showwarning(
                "Summarize Document",
                "There was not enough readable text to summarize."
            )
            return

        # ----------------------------------------------------------
        # Score sentences
        # ----------------------------------------------------------

        scored_sentences = []

        for index, sentence in enumerate(sentences):

            sentence_words = re.findall(
                r'\b[a-zA-Z]{3,}\b',
                sentence.lower()
            )

            score = sum(
                frequencies.get(word, 0)
                for word in sentence_words
                if word not in stop_words
            )

            # Slight preference for earlier sentences
            # because introductions often contain useful context.
            position_bonus = max(
                0,
                5 - index
            )

            score += position_bonus

            scored_sentences.append(
                (
                    score,
                    index,
                    sentence
                )
            )

        # ----------------------------------------------------------
        # Select summary size
        # ----------------------------------------------------------

        summary_count = max(
            3,
            min(
                8,
                len(sentences) // 5
            )
        )

        selected = sorted(
            scored_sentences,
            key=lambda item: item[0],
            reverse=True
        )[:summary_count]

        # Restore original document order
        selected = sorted(
            selected,
            key=lambda item: item[1]
        )

        summary = "\n\n".join(
            sentence
            for _, _, sentence in selected
        )

        # ----------------------------------------------------------
        # Display summary
        # ----------------------------------------------------------

        self._show_summary_window(
            summary,
            len(sentences)
        )

    def _show_summary_window(self, summary, sentence_count):

        summary_window = ctk.CTkToplevel(
            self
        )

        summary_window.title(
            "📝 Document Summary"
        )

        summary_window.geometry(
            "850x650"
        )

        summary_window.minsize(
            700,
            500
        )

        # ----------------------------------------------------------
        # Header
        # ----------------------------------------------------------

        header = ctk.CTkLabel(
            summary_window,
            text="📝 Document Summary",
            font=("Arial", 22, "bold")
        )

        header.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        info = ctk.CTkLabel(
            summary_window,
            text=f"Generated from {sentence_count:,} sentences.",
            font=("Arial", 12)
        )

        info.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # ----------------------------------------------------------
        # Summary text
        # ----------------------------------------------------------

        summary_box = ctk.CTkTextbox(
            summary_window,
            wrap="word",
            font=("Arial", 14)
        )

        summary_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        summary_box.insert(
            "1.0",
            summary
        )

        # ----------------------------------------------------------
        # Close
        # ----------------------------------------------------------

        close_button = ctk.CTkButton(
            summary_window,
            text="Close",
            command=summary_window.destroy
        )

        close_button.pack(
            pady=(0, 20)
        )
    def search_document(self):

        if not self.document_text:
            return

        search_window = ctk.CTkToplevel(self)

        search_window.title("🔎 Search Document")
        search_window.geometry("700x500")
        search_window.minsize(600, 400)

        # ==========================================================
        # Search Header
        # ==========================================================

        header = ctk.CTkFrame(
            search_window,
            corner_radius=10
        )
        header.pack(
            fill="x",
            padx=15,
            pady=15
        )

        search_entry = ctk.CTkEntry(
            header,
            width=450,
            placeholder_text="Enter a word or phrase..."
        )
        search_entry.pack(
            side="left",
            padx=(15, 10),
            pady=15
        )

        search_button = ctk.CTkButton(
            header,
            text="🔎 Search",
            width=120
        )
        search_button.pack(
            side="left",
            padx=10,
            pady=15
        )

        # ==========================================================
        # Result Information
        # ==========================================================

        result_label = ctk.CTkLabel(
            search_window,
            text="Enter a search term.",
            font=("Arial", 13)
        )
        result_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # ==========================================================
        # Results
        # ==========================================================

        results_box = ctk.CTkTextbox(
            search_window,
            wrap="word",
            font=("Arial", 13)
        )
        results_box.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ==========================================================
        # Search Function
        # ==========================================================

        def perform_search():

            term = search_entry.get().strip()

            if not term:
                result_label.configure(
                    text="Please enter a search term."
                )

                results_box.delete(
                    "1.0",
                    "end"
                )

                return

            # Clear previous results
            results_box.delete(
                "1.0",
                "end"
            )

            lines = self.document_text.splitlines()

            matches = []

            for line_number, line in enumerate(lines, start=1):

                if term.lower() in line.lower():

                    matches.append(
                        (
                            line_number,
                            line.strip()
                        )
                    )

            # ======================================================
            # No Results
            # ======================================================

            if not matches:

                result_label.configure(
                    text=f'No matches found for "{term}".'
                )

                results_box.insert(
                    "1.0",
                    "No matching text was found in the document."
                )

                return

            # ======================================================
            # Result Count
            # ======================================================

            result_label.configure(
                text=f'Found {len(matches):,} matching line(s) for "{term}".'
            )

            # ======================================================
            # Display Results
            # ======================================================

            for line_number, line in matches:

                results_box.insert(
                    "end",
                    f"Line {line_number}: {line}\n\n"
                )

        # ==========================================================
        # Button / Enter Key
        # ==========================================================

        search_button.configure(
            command=perform_search
        )

        search_entry.bind(
            "<Return>",
            lambda event: perform_search()
        )

        search_entry.focus()


    def ask_question(self):

        if not self.document_text.strip():
            messagebox.showwarning(
                "Ask Question",
                "Please open a document first."
            )
            return

        question_window = ctk.CTkToplevel(self)

        question_window.title("❓ Ask Question")
        question_window.geometry("850x650")
        question_window.minsize(700, 500)

        # ==========================================================
        # Header
        # ==========================================================

        title = ctk.CTkLabel(
            question_window,
            text="❓ Ask a Question",
            font=("Arial", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        description = ctk.CTkLabel(
            question_window,
            text="Ask a question about the currently loaded document.",
            font=("Arial", 12)
        )

        description.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # ==========================================================
        # Question Input
        # ==========================================================

        question_entry = ctk.CTkEntry(
            question_window,
            placeholder_text="Example: What is this document about?",
            height=40
        )

        question_entry.pack(
            fill="x",
            padx=25,
            pady=(0, 10)
        )

        ask_button = ctk.CTkButton(
            question_window,
            text="🔎 Find Answer",
            width=150
        )

        ask_button.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # ==========================================================
        # Answer
        # ==========================================================

        answer_label = ctk.CTkLabel(
            question_window,
            text="Answer",
            font=("Arial", 16, "bold")
        )

        answer_label.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        answer_box = ctk.CTkTextbox(
            question_window,
            wrap="word",
            font=("Arial", 13)
        )

        answer_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # ==========================================================
        # Question Processing
        # ==========================================================

        def normalize_word(word):

            word = word.lower().strip()

            # Simple plural handling
            if word.endswith("ies") and len(word) > 4:
                word = word[:-3] + "y"

            elif word.endswith("es") and len(word) > 4:
                word = word[:-2]

            elif word.endswith("s") and len(word) > 3:
                word = word[:-1]

            return word

        # ==========================================================
        # Find Answer
        # ==========================================================

        def find_answer():

            question = question_entry.get().strip()

            if not question:

                messagebox.showwarning(
                    "Ask Question",
                    "Please enter a question."
                )

                return

            import re

            # ------------------------------------------------------
            # Stop words
            # ------------------------------------------------------

            stop_words = {
                "the", "a", "an", "and", "or",
                "but", "if", "then", "than",
                "is", "are", "was", "were",
                "be", "been", "being", "to",
                "of", "in", "on", "for",
                "with", "as", "by", "at",
                "from", "this", "that",
                "these", "those", "it",
                "its", "they", "their",
                "them", "he", "she",
                "his", "her", "we",
                "our", "you", "your",
                "i", "me", "my",
                "what", "which", "who",
                "when", "where", "why",
                "how", "does", "do",
                "did", "can", "could",
                "would", "should",
                "please", "tell", "explain",
                "give", "describe"
            }

            # ------------------------------------------------------
            # Extract question keywords
            # ------------------------------------------------------

            question_words = re.findall(
                r"\b[a-zA-Z]{3,}\b",
                question.lower()
            )

            keywords = [
                normalize_word(word)
                for word in question_words
                if word not in stop_words
            ]

            keywords = list(
                dict.fromkeys(keywords)
            )

            if not keywords:

                answer_box.delete(
                    "1.0",
                    "end"
                )

                answer_box.insert(
                    "1.0",
                    "I could not identify useful keywords "
                    "from your question."
                )

                return

            # ------------------------------------------------------
            # Split document into sentences
            # ------------------------------------------------------

            sentences = re.split(
                r"(?<=[.!?])\s+",
                self.document_text
            )

            sentences = [
                sentence.strip()
                for sentence in sentences
                if sentence.strip()
            ]

            if not sentences:

                answer_box.delete(
                    "1.0",
                    "end"
                )

                answer_box.insert(
                    "1.0",
                    "The document does not contain enough "
                    "readable text to answer this question."
                )

                return

            # ------------------------------------------------------
            # Score each sentence
            # ------------------------------------------------------

            scored = []

            for index, sentence in enumerate(sentences):

                sentence_words = re.findall(
                    r"\b[a-zA-Z]{3,}\b",
                    sentence.lower()
                )

                normalized_sentence_words = [
                    normalize_word(word)
                    for word in sentence_words
                    if word not in stop_words
                ]

                if not normalized_sentence_words:
                    continue

                score = 0
                matched_keywords = []

                for keyword in keywords:

                    occurrences = normalized_sentence_words.count(
                        keyword
                    )

                    if occurrences > 0:

                        matched_keywords.append(
                            keyword
                        )

                        # More occurrences = slightly higher relevance
                        score += min(
                            occurrences,
                            3
                        )

                if not matched_keywords:
                    continue

                # --------------------------------------------------
                # Coverage bonus
                # --------------------------------------------------

                coverage = (
                    len(set(matched_keywords))
                    / len(keywords)
                )

                score += coverage * 3

                scored.append(
                    (
                        score,
                        index,
                        sentence,
                        matched_keywords
                    )
                )

            # ------------------------------------------------------
            # No answer found
            # ------------------------------------------------------

            if not scored:

                answer_box.delete(
                    "1.0",
                    "end"
                )

                answer_box.insert(
                    "1.0",
                    "I couldn't find information in the "
                    "document that directly matches your question."
                )

                return

            # ------------------------------------------------------
            # Sort by relevance
            # ------------------------------------------------------

            scored.sort(
                key=lambda item: item[0],
                reverse=True
            )

            # Keep only the strongest passages
            best_results = scored[:5]

            # Restore original document order
            best_results.sort(
                key=lambda item: item[1]
            )

            # ------------------------------------------------------
            # Build response
            # ------------------------------------------------------

            answer = (
                "Based on the loaded document, "
                "the most relevant information I found is:\n\n"
            )

            for _, _, sentence, _ in best_results:

                answer += (
                    f"• {sentence}\n\n"
                )

            answer += (
                "────────────────────────────\n"
                f"Relevant passages found: {len(best_results)}\n\n"
                "This answer is based only on information "
                "found in the loaded document."
            )

            # ------------------------------------------------------
            # Display
            # ------------------------------------------------------

            answer_box.delete(
                "1.0",
                "end"
            )

            answer_box.insert(
                "1.0",
                answer
            )

        # ==========================================================
        # Button
        # ==========================================================

        ask_button.configure(
            command=find_answer
        )

        question_entry.bind(
            "<Return>",
            lambda event: find_answer()
        )

        question_entry.focus()



    def update_document_information(self, file_path):

        if not file_path:
            return

        file_size = os.path.getsize(file_path)

        if file_size < 1024:
            size_text = f"{file_size:,} B"

        elif file_size < 1024 * 1024:
            size_text = f"{file_size / 1024:.2f} KB"

        else:
            size_text = f"{file_size / (1024 * 1024):.2f} MB"

        words = len(
            self.document_text.split()
        )

        characters = len(
            self.document_text
        )

        lines = len(
            self.document_text.splitlines()
        )

        extension = os.path.splitext(
            file_path
        )[1].lower()

        file_type = {
            ".txt": "Text File",
            ".docx": "Word Document",
            ".pdf": "PDF Document"
        }.get(
            extension,
            extension.upper()
        )

        self.file_type_label.configure(
            text=f"Type: {file_type}"
        )

        self.file_size_label.configure(
            text=f"Size: {size_text}"
        )

        self.words_label.configure(
            text=f"Words: {words:,}"
        )

        self.characters_label.configure(
            text=f"Characters: {characters:,}"
        )

        self.lines_label.configure(
            text=f"Lines: {lines:,}"
        )

        if extension == ".pdf":
            self.pages_label.configure(
                text=f"Pages: {self.document_page_count:,}"
            )
        else:
            self.pages_label.configure(
                text="Pages: N/A"
            )

        self.status_label.configure(
            text="Status: ✓ Document loaded"
        )
    # ==========================================================
    # Export
    # ==========================================================

    def export_document(self):

        if not self.document_text:
            return

        file_path = filedialog.asksaveasfilename(
            title="Export Document Text",
            defaultextension=".txt",
            filetypes=[
                (
                    "Text File",
                    "*.txt"
                )
            ]
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    self.document_text
                )

            messagebox.showinfo(
                "Export Complete",
                "Document text exported successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )