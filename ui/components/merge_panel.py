import customtkinter as ctk


class MergePanel(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.datasets = {}

        self.title("Merge Datasets")
        self.geometry("520x520")
        self.resizable(False, False)

        # ==================================
        # Left Dataset
        # ==================================

        ctk.CTkLabel(
            self,
            text="Left Dataset"
        ).pack(
            pady=(20, 5)
        )

        self.left_dataset = ctk.CTkOptionMenu(
            self,
            values=["No Dataset"],
            command=self.update_left_columns
        )

        self.left_dataset.pack(
            padx=20,
            fill="x"
        )

        # ==================================
        # Left Key
        # ==================================

        ctk.CTkLabel(
            self,
            text="Left Key"
        ).pack(
            pady=(15, 5)
        )

        self.left_key = ctk.CTkOptionMenu(
            self,
            values=["Select Dataset First"]
        )

        self.left_key.pack(
            padx=20,
            fill="x"
        )

        # ==================================
        # Right Dataset
        # ==================================

        ctk.CTkLabel(
            self,
            text="Right Dataset"
        ).pack(
            pady=(15, 5)
        )

        self.right_dataset = ctk.CTkOptionMenu(
            self,
            values=["No Dataset"],
            command=self.update_right_columns
        )

        self.right_dataset.pack(
            padx=20,
            fill="x"
        )

        # ==================================
        # Right Key
        # ==================================

        ctk.CTkLabel(
            self,
            text="Right Key"
        ).pack(
            pady=(15, 5)
        )

        self.right_key = ctk.CTkOptionMenu(
            self,
            values=["Select Dataset First"]
        )

        self.right_key.pack(
            padx=20,
            fill="x"
        )

        # ==================================
        # Join Type
        # ==================================

        ctk.CTkLabel(
            self,
            text="Join Type"
        ).pack(
            pady=(15, 5)
        )

        self.join_type = ctk.CTkOptionMenu(
            self,
            values=[
                "left",
                "right",
                "inner",
                "outer"
            ]
        )

        self.join_type.pack(
            padx=20,
            fill="x"
        )

        # ==================================
        # Merge Button
        # ==================================

        self.merge_button = ctk.CTkButton(
            self,
            text="Merge Datasets"
        )

        self.merge_button.pack(
            pady=30
        )

    # ==========================================
    # Store Loaded Datasets
    # ==========================================

    def load_dataset_columns(self, datasets):

        self.datasets = datasets

    # ==========================================
    # Update Left Columns
    # ==========================================

    def update_left_columns(self, dataset_name):

        if dataset_name not in self.datasets:
            return

        columns = list(
            self.datasets[dataset_name].columns
        )

        self.left_key.configure(
            values=columns
        )

        if columns:
            self.left_key.set(columns[0])
            self.auto_detect_keys()

    # ==========================================
    # Update Right Columns
    # ==========================================

    def update_right_columns(self, dataset_name):

        if dataset_name not in self.datasets:
            return

        columns = list(
            self.datasets[dataset_name].columns
        )

        self.right_key.configure(
            values=columns
        )

        if columns:
            self.right_key.set(columns[0])
            self.auto_detect_keys()

    # ==========================================
    # Auto Detect Matching Keys
    # ==========================================

    def auto_detect_keys(self):

        left_dataset = self.left_dataset.get()
        right_dataset = self.right_dataset.get()

        if left_dataset not in self.datasets:
            return

        if right_dataset not in self.datasets:
            return

        left_columns = list(
            self.datasets[left_dataset].columns
        )

        right_columns = list(
            self.datasets[right_dataset].columns
        )

        # Find matching column names
        matches = [
            col for col in left_columns
            if col in right_columns
        ]

        if matches:

            self.left_key.set(matches[0])

            self.right_key.set(matches[0])