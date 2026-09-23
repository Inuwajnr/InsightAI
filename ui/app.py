import customtkinter as ctk
from tkinter import filedialog, messagebox
from data.analyzer import DataAnalyzer
from data.cleaning import DataCleaner
from data.statistics import StatisticsEngine
from data.charts import ChartGenerator
from data.profile import DatasetProfile
from data.quality import DataQuality
from data.correlation import CorrelationAnalyzer
from ui.components.merge_panel import MergePanel
from core.merge_engine import MergeEngine
from ui.components.pivot_window import PivotWindow
from ui.components.correlation_window import CorrelationWindow
from ui.components.data_analysis_panel import DataAnalysisPanel
import pandas as pd
from data.smart_kpi import SmartKPIEngine
from data.pivot import PivotEngine
from ui.components.statistics_panel import StatisticsPanel
from analysis import DataAnalysisEngine
from ui.sidebar import Sidebar
from ui.pages.dashboard import Dashboard


class InsightAIApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =====================================
        # Window
        # =====================================

        self.title("InsightAI Offline")
        self.geometry("1400x800")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # =====================================
        # Engines
        # =====================================

        self.datasets = {}
        self.analyzer = DataAnalyzer()
        self.cleaner = DataCleaner()
        self.statistics = StatisticsEngine()
        self.quality = DataQuality()
        self.correlation = CorrelationAnalyzer()
        self.chart_generator = ChartGenerator()
        self.profile = DatasetProfile()
        self.merge_engine = MergeEngine()
        self.pivot_engine = PivotEngine()
        self.smart_kpi = SmartKPIEngine()
        self.analysis = DataAnalysisEngine()
        

        # =====================================
        # Current Dataset
        # =====================================

        self.current_file = None
        self.current_df = None

        # =====================================
        # UI
        # =====================================

        self.sidebar = Sidebar(self)
        self.dashboard = Dashboard(self)

        # =====================================
        # Connect Buttons
        # =====================================

        self.dashboard.chart_controls.generate_btn.configure(
            command=self.generate_chart
        )

        self.dashboard.chart_controls.export_btn.configure(
            command=self.export_chart
        )
    # ==================================
    # Display Pivot Table
    # ==================================

    def display_pivot(self, pivot_df):

        self.result_box.configure(state="normal")

        self.result_box.delete("1.0", "end")

        self.result_box.insert(
            "1.0",
            pivot_df.to_string(index=False)
        )

        self.result_box.configure(state="disabled")


    # ======================================================
    # Show Pivot Table Builder
    # ======================================================

    def show_pivot(self):

        if self.current_df is None:

            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )
            return

        PivotWindow(
            self,
            self.current_df,
            self.pivot_engine
        )

    # ======================================================
    # Upload Dataset
    # ======================================================

    def upload_file(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("CSV Files", "*.csv")
            ]
        )

        if not file_path:
            return

        self.current_file = file_path

        try:

            if file_path.lower().endswith(".csv"):

                self.dashboard.sheet_dropdown.configure(
                    values=["CSV File"]
                )

                self.dashboard.sheet_dropdown.set(
                    "CSV File"
                )

                self.load_selected_sheet(None)

            else:

                sheets = self.analyzer.get_sheet_names(
                    file_path
                )

                self.dashboard.sheet_dropdown.configure(
                    values=sheets,
                    command=self.load_selected_sheet
                )

                self.dashboard.sheet_dropdown.set(
                    sheets[0]
                )

                self.load_selected_sheet(
                    sheets[0]
                )

        except Exception as e:

            messagebox.showerror(
                "Upload Error",
                str(e)
            )

    # ======================================================
    # Load Worksheet
    # ======================================================

    def load_selected_sheet(self, sheet_name):

        # =====================================
        # Load Dataset
        # =====================================

        self.current_df = self.analyzer.load_file(
            self.current_file,
            sheet_name
        )
        import os

        dataset_name = os.path.splitext(
            os.path.basename(self.current_file)
        )[0]

        if sheet_name:
            dataset_name = f"{dataset_name} - {sheet_name}"

        self.datasets[dataset_name] = self.current_df

        self.current_dataset_name = dataset_name


        print("\n========== DATASETS ==========")

        for name in self.datasets:
            print(name)

        # =====================================
        # Dataset Summary
        # =====================================

        self.refresh_dashboard()
        
        self.dashboard.status_bar.set_status(
            "Dataset Loaded Successfully"
        )

        # =====================================
        # Populate Chart Controls
        # =====================================

        controls = self.dashboard.chart_controls

        all_columns = list(self.current_df.columns)

        numeric_columns = self.analyzer.get_numeric_columns(
            self.current_df
        )

        categorical_columns = self.analyzer.get_categorical_columns(
            self.current_df
        )

        controls.x_dropdown.configure(
            values=all_columns
        )

        controls.y_dropdown.configure(
            values=all_columns
        )

        # Smart Default Selection

        if categorical_columns:
            controls.x_dropdown.set(
                categorical_columns[0]
            )
        else:
            controls.x_dropdown.set(
                all_columns[0]
            )

        if numeric_columns:
            controls.y_dropdown.set(
                numeric_columns[0]
            )
        else:
            controls.y_dropdown.set(
                all_columns[0]
            )

        controls.chart_dropdown.set(
            "Bar Chart"
        )

        controls.set_recommendation(
            f"Recommended: Bar Chart ({controls.y_dropdown.get()} by {controls.x_dropdown.get()})"
        )

        # =====================================
        # Status
        # =====================================

        self.dashboard.status_bar.set_status(
            "Dataset Loaded Successfully"
        )
    # ======================================================
    # Generate Chart
    # ======================================================

    def generate_chart(self):

        if self.current_df is None:

            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )
            return

        controls = self.dashboard.chart_controls

        chart = controls.chart_dropdown.get()
        x_col = controls.x_dropdown.get()
        y_col = controls.y_dropdown.get()
        top_n = controls.top_dropdown.get()

        # ===============================
        # DEBUG INFORMATION
        # ===============================

        print("\n==============================")
        print("Chart Type :", chart)
        print("X Column   :", x_col)
        print("Y Column   :", y_col)
        print("==============================")

        print("\nUnique X Values:")
        print(self.current_df[x_col].value_counts(dropna=False))

        print("\nFirst 10 Records:")
        print(self.current_df[[x_col, y_col]].head(10))

        if chart in ["Bar Chart", "Column Chart", "Line Chart"]:

            debug_df = self.current_df.copy()

            debug_df[y_col] = pd.to_numeric(
                debug_df[y_col],
                errors="coerce"
            )

            debug_df = debug_df.dropna(
                subset=[x_col, y_col]
            )

            grouped = (
                debug_df.groupby(x_col)[y_col]
                .sum()
                .sort_values(ascending=False)
            )

            print("\nGrouped Result")
            print(grouped)

        # ===============================
        # DRAW CHART
        # ===============================

        chart_view = self.dashboard.chart_view

        chart_view.clear()

        try:

            if chart == "Bar Chart":

                self.chart_generator.bar_chart(
                    chart_view.ax,
                    self.current_df,
                    x_col,
                    y_col,
                    top_n
                )

            elif chart == "Column Chart":

                self.chart_generator.column_chart(
                    chart_view.ax,
                    self.current_df,
                    x_col,
                    y_col,
                    top_n
                )

            elif chart == "Line Chart":

                self.chart_generator.line_chart(
                    chart_view.ax,
                    self.current_df,
                    x_col,
                    y_col,
                    top_n

                )

            elif chart == "Scatter Plot":

                self.chart_generator.scatter_plot(
                    chart_view.ax,
                    self.current_df,
                    x_col,
                    y_col,
                )

            elif chart == "Pie Chart":

                self.chart_generator.pie_chart(
                    chart_view.ax,
                    self.current_df,
                    x_col
                )

            elif chart == "Histogram":

                self.chart_generator.histogram(
                    chart_view.ax,
                    self.current_df,
                    x_col
                )

            chart_view.draw()

            self.dashboard.status_bar.set_status(
                "Chart Generated Successfully"
            )

        except Exception as e:

            messagebox.showerror(
                "Chart Error",
                str(e)
            )

    # ======================================================
    # Export Current Chart
    # ======================================================

    def export_chart(self):

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png")
            ]
        )

        if not filename:
            return

        try:

            self.dashboard.chart_view.save_chart(
                filename
            )

            self.dashboard.status_bar.set_status(
                "Chart Exported Successfully"
            )

            messagebox.showinfo(
                "Export Complete",
                "Chart exported successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )
    # ======================================================
    # Refresh Dashboard
    # ======================================================

    
    # ======================================================
    # Clean Dataset
    # ======================================================

    def clean_data(self):

        if self.current_df is None:

            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )
            return

        try:

            # --------------------------------
            # Clean Dataset
            # --------------------------------

            self.current_df, report = self.cleaner.clean_dataset(
                self.current_df
            )

            # Update the currently selected dataset
            if hasattr(self, "current_dataset_name"):
                self.datasets[self.current_dataset_name] = self.current_df

            # --------------------------------
            # Refresh Entire Dashboard
            # --------------------------------

            self.refresh_dashboard()

            # --------------------------------
            # Success Status
            # --------------------------------

            self.dashboard.status_bar.set_status(
                "Dataset Cleaned Successfully"
            )

            # --------------------------------
            # Cleaning Report
            # --------------------------------

            messagebox.showinfo(
                "Cleaning Complete",
                f"""
    Rows Before: {report['original_rows']}

    Rows After: {report['final_rows']}

    Duplicates Removed: {report['duplicates_removed']}

    Missing Values Before: {report['missing_before']}

    Missing Values After: {report['missing_after']}
    """
            )

        except Exception as e:

            messagebox.showerror(
                "Cleaning Error",
                str(e)
            )

    # ======================================================
    # Dataset Statistics
    # ======================================================

    def show_statistics(self):

        if self.current_df is None:

            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )

            return

        try:

            summary = self.statistics.dataset_summary(
                self.current_df
            )

            descriptive = self.current_df.describe(include="all")

            missing = self.statistics.missing_values(
                self.current_df
            )

            data_types = self.statistics.data_types(
                self.current_df
            )

            numeric_columns = self.statistics.numeric_columns(
                self.current_df
            )

            categorical_columns = self.statistics.categorical_columns(
                self.current_df
            )

            self.statistics_window = StatisticsPanel(
                self,
                summary,
                descriptive,
                missing,
                data_types,
                numeric_columns,
                categorical_columns
            )

            self.dashboard.status_bar.set_status(
                "Statistics Generated"
            )

        except Exception as e:

            messagebox.showerror(
                "Statistics Error",
                str(e)
            )
    # ======================================================
    # Merge Window
    # ======================================================

    def open_merge_panel(self):

        if len(self.datasets) < 2:

            messagebox.showwarning(
                "Merge Data",
                "Please load at least two datasets before merging."
            )

            return
        
        self.merge_window = MergePanel(self)

        self.merge_window.merge_button.configure(
            command=self.execute_merge
        )

        dataset_names = list(self.datasets.keys())

        self.merge_window.left_dataset.configure(
            values=dataset_names
        )

        self.merge_window.right_dataset.configure(
            values=dataset_names
        )

        self.merge_window.load_dataset_columns(
            self.datasets
        )

        self.merge_window.left_dataset.set(
            dataset_names[0]
        )

        self.merge_window.right_dataset.set(
            dataset_names[1]
        )

        self.merge_window.update_left_columns(
            dataset_names[0]
        )

        self.merge_window.update_right_columns(
            dataset_names[1]
        )

    def execute_merge(self):

        panel = self.merge_window

        left_name = panel.left_dataset.get()
        right_name = panel.right_dataset.get()

        left_key = panel.left_key.get()
        right_key = panel.right_key.get()

        join_type = panel.join_type.get()

        left_df = self.datasets[left_name]
        right_df = self.datasets[right_name]

        merged_df = self.merge_engine.merge(
            left_df,
            right_df,
            left_key,
            right_key,
            join_type
        )

        dataset_name = f"{left_name}_{right_name}_Merged"

        self.datasets[dataset_name] = merged_df

        self.current_df = merged_df

        self.current_dataset_name = dataset_name

        self.refresh_dashboard()
        
        self.dashboard.status_bar.set_status(
            "Datasets Merged Successfully"
        )

        panel.destroy()


    def refresh_dashboard(self):

        summary = self.analyzer.get_summary(
            self.current_df
        )
        # -----------------------------
        # Smart KPI cards
        # -----------------------------

        kpis = self.smart_kpi.generate(
            self.current_df
        )

        print("\n===== GENERATED KPIs =====")
        print(kpis)

        self.dashboard.smart_kpi_panel.update_cards(
            kpis
        )

        self.dashboard.rows_card.update_value(summary["rows"])

        self.dashboard.columns_card.update_value(summary["columns"])

        self.dashboard.missing_card.update_value(
            summary["missing_values"]
        )

        self.dashboard.memory_card.update_value(
            f"{summary['memory']} KB"
        )

        self.dashboard.data_grid.load_dataframe(
            self.current_df
        )

        profile = self.profile.generate_profile(
            self.current_df
        )

        self.dashboard.profile_panel.update_profile(
            profile
        )
        print("\n===== MERGED DATASET =====")
        print(self.current_df.head())
        print(self.current_df.shape)

        profile = self.profile.generate_profile(self.current_df)

        print("\n===== PROFILE =====")
        print(profile)

        quality = self.quality.evaluate(
            self.current_df
        )

        self.dashboard.quality_panel.update_quality(
            quality
        )

        controls = self.dashboard.chart_controls

        columns = list(self.current_df.columns)

        controls.x_dropdown.configure(values=columns)
        controls.y_dropdown.configure(values=columns)

        if columns:

            controls.x_dropdown.set(columns[0])
            controls.y_dropdown.set(columns[0])

        self.dashboard.status_bar.set_status(
            "Datasets merged successfully."
        )

    # ======================================================
    # Correlation Analysis
    # ======================================================

    def show_correlation(self):

        if self.current_df is None:

            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )

            return

        try:

            corr = self.statistics.correlation_matrix(
                self.current_df
            )

            if corr is None or corr.shape[1] < 2:

                messagebox.showwarning(
                    "Correlation",
                    "Dataset requires at least two numeric columns."
                )

                return

            CorrelationWindow(
                self,
                corr
            )

            self.dashboard.status_bar.set_status(
                "Correlation Analysis Generated"
            )

        except Exception as e:

            messagebox.showerror(
                "Correlation Error",
                str(e)
            )

    # ======================================================
    # Data Analysis
    # ======================================================

    def show_data_analysis(self):

        if self.current_df is None:
            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )
            return

        try:

            self.analysis_window = DataAnalysisPanel(
                self
            )

            self.dashboard.status_bar.set_status(
                "Data Analysis Opened"
            )

        except Exception as e:

            messagebox.showerror(
                "Data Analysis Error",
                str(e)
            )
    # ======================================================
    # Run Application
    # ======================================================

    def run(self):
        self.mainloop()