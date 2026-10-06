import customtkinter as ctk
from tkinter import filedialog
from data.analyzer import DataAnalyzer
from data.charts import ChartGenerator

# ----------------------------
# App Settings
# ----------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

analyzer = DataAnalyzer()
chart_generator = ChartGenerator()
current_file = None
current_df = None

# ----------------------------
# Main Window
# ----------------------------
app = ctk.CTk()
app.title("InsightAI Offline")
app.geometry("1200x700")

# ----------------------------
# Sidebar
# ----------------------------
sidebar = ctk.CTkFrame(app, width=250)
sidebar.pack(side="left", fill="y")

title = ctk.CTkLabel(
    sidebar,
    text="InsightAI Offline",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)

# ----------------------------
# Main Content Area
# ----------------------------
content = ctk.CTkFrame(app)
content.pack(side="right", fill="both", expand=True)

# ----------------------------
# Worksheet Selector
# ----------------------------
sheet_label = ctk.CTkLabel(
    content,
    text="Worksheet"
)
sheet_label.pack(pady=(10, 0))

sheet_dropdown = ctk.CTkOptionMenu(
    content,
    values=["No Sheet Loaded"]
)
sheet_dropdown.pack(pady=5)

# ----------------------------
# KPI Section
# ----------------------------
kpi_frame = ctk.CTkFrame(content)
kpi_frame.pack(fill="x", padx=20, pady=10)

rows_card = ctk.CTkLabel(
    kpi_frame,
    text="Rows\n0",
    width=200,
    height=80,
    corner_radius=10,
    font=("Arial", 18)
)
rows_card.pack(side="left", padx=10, pady=10)

columns_card = ctk.CTkLabel(
    kpi_frame,
    text="Columns\n0",
    width=200,
    height=80,
    corner_radius=10,
    font=("Arial", 18)
)
columns_card.pack(side="left", padx=10, pady=10)

missing_card = ctk.CTkLabel(
    kpi_frame,
    text="Missing\n0",
    width=200,
    height=80,
    corner_radius=10,
    font=("Arial", 18)
)
missing_card.pack(side="left", padx=10, pady=10)


# ----------------------------
# Chart Controls
# ----------------------------
chart_frame = ctk.CTkFrame(content)
chart_frame.pack(fill="x", padx=20, pady=10)

x_dropdown = ctk.CTkOptionMenu(
    chart_frame,
    values=["Select X Column"]
)
x_dropdown.pack(side="left", padx=10)

y_dropdown = ctk.CTkOptionMenu(
    chart_frame,
    values=["Select Y Column"]
)
y_dropdown.pack(side="left", padx=10)

chart_dropdown = ctk.CTkOptionMenu(
    chart_frame,
    values=[
        "Bar Chart",
        "Column Chart",
        "Line Chart",
        "Pie Chart",
        "Histogram",
        "Scatter Plot"
    ]
)
chart_dropdown.set("Bar Chart")

chart_dropdown.pack(side="left", padx=10)

# ----------------------------
# Data Preview Area
# ----------------------------
preview_box = ctk.CTkTextbox(
    content,
    width=850,
    height=500
)
preview_box.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# ----------------------------
# Load Selected Sheet
# ----------------------------
def load_selected_sheet(choice):

    global current_file
    global current_df

    try:

        current_df = analyzer.load_file(
            current_file,
            sheet_name=choice
        )

        summary = analyzer.get_summary(
            current_df
        )
        columns = list(current_df.columns)

        x_dropdown.configure(
            values=columns
        )

        y_dropdown.configure(
            values=columns
        )

        if len(columns) > 0:
            x_dropdown.set(columns[0])

        if len(columns) > 1:
            y_dropdown.set(columns[1])

        rows_card.configure(
            text=f"Rows\n{summary['rows']}"
        )

        columns_card.configure(
            text=f"Columns\n{summary['columns']}"
        )

        missing_card.configure(
            text=f"Missing\n{summary['missing_values']}"
        )

        preview_box.delete(
            "1.0",
            "end"
        )

        sheet_name_display = (
            choice if choice else "CSV File"
        )

        preview_box.insert(
            "end",
            f"Worksheet: {sheet_name_display}\n\n"
        )

        preview_box.insert(
            "end",
            "Columns:\n"
        )

        preview_box.insert(
            "end",
            "\n".join(
                summary["column_names"]
            )
        )

        preview_box.insert(
            "end",
            "\n\nPreview (First 20 Rows):\n\n"
        )

        preview_box.insert(
            "end",
            str(
                current_df.head(20)
            )
        )

    except Exception as e:

        preview_box.delete(
            "1.0",
            "end"
        )

        preview_box.insert(
            "end",
            f"Error:\n{e}"
        )


# ----------------------------
# Generate Chart
# ----------------------------
def generate_chart():

    global current_df

    if current_df is None:
        return

    chart_type = chart_dropdown.get()
    x_col = x_dropdown.get()
    y_col = y_dropdown.get()

    try:

        if chart_type == "Bar Chart":

            chart_generator.bar_chart(
                current_df,
                x_col,
                y_col
            )

        elif chart_type == "Column Chart":

            chart_generator.column_chart(
                current_df,
                x_col,
                y_col
            )

        elif chart_type == "Scatter Plot":

            chart_generator.scatter_plot(
                current_df,
                x_col,
                y_col
            )

        elif chart_type == "Line Chart":

            chart_generator.line_chart(
                current_df,
                x_col,
                y_col
            )

        elif chart_type == "Pie Chart":

            chart_generator.pie_chart(
                current_df,
                x_col
            )

        elif chart_type == "Histogram":

            chart_generator.histogram(
                current_df,
                x_col
            )

    except Exception as e:

        preview_box.insert(
            "end",
            f"\n\nChart Error:\n{e}"
        )

generate_btn = ctk.CTkButton(
    chart_frame,
    text="Generate Chart",
    command=generate_chart
)

generate_btn.pack(
    side="left",
    padx=10
)

# ----------------------------
# Upload File
# ----------------------------
def upload_file():

    global current_file

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Excel Files", "*.xlsx"),
            ("CSV Files", "*.csv")
        ]
    )

    if not file_path:
        return

    current_file = file_path

    try:

        # CSV
        if file_path.endswith(".csv"):

            sheet_dropdown.configure(
                values=["CSV File"]
            )

            sheet_dropdown.set(
                "CSV File"
            )

            load_selected_sheet(
                None
            )

        # Excel
        elif file_path.endswith(".xlsx"):

            sheets = analyzer.get_sheet_names(
                file_path
            )

            sheet_dropdown.configure(
                values=sheets,
                command=load_selected_sheet
            )

            sheet_dropdown.set(
                sheets[0]
            )

            load_selected_sheet(
                sheets[0]
            )

    except Exception as e:

        preview_box.delete(
            "1.0",
            "end"
        )

        preview_box.insert(
            "end",
            f"Error loading file:\n\n{e}"
        )

# ----------------------------
# Sidebar Buttons
# ----------------------------
upload_btn = ctk.CTkButton(
    sidebar,
    text="📂 Upload Dataset",
    command=upload_file
)
upload_btn.pack(
    pady=20,
    padx=20
)

data_btn = ctk.CTkButton(
    sidebar,
    text="📊 Data Analysis"
)
data_btn.pack(
    pady=10,
    padx=20
)

docs_btn = ctk.CTkButton(
    sidebar,
    text="📄 Document Assistant"
)
docs_btn.pack(
    pady=10,
    padx=20
)

chat_btn = ctk.CTkButton(
    sidebar,
    text="🤖 AI Chat"
)
chat_btn.pack(
    pady=10,
    padx=20
)

# ----------------------------
# Run App
# ----------------------------
app.mainloop()