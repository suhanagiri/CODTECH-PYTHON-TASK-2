import pandas as pd
from fpdf import FPDF

# Load the CSV file
df = pd.read_csv("sales_data.csv")
df['Revenue'] = df['Units Sold'] * df['Unit Price']

# Summary statistics
total_units = df['Units Sold'].sum()
total_revenue = df['Revenue'].sum()
avg_units = df['Units Sold'].mean()
avg_revenue = df['Revenue'].mean()

# PDF Generation
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Sales Report", ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f"Page {self.page_no()}", align='C')

    def add_summary(self, total_units, total_revenue, avg_units, avg_revenue):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Total Units Sold: {total_units}", ln=True)
        self.cell(0, 10, f"Total Revenue: ₹{total_revenue}", ln=True)
        self.cell(0, 10, f"Average Units per Day: {avg_units:.2f}", ln=True)
        self.cell(0, 10, f"Average Revenue per Day: ₹{avg_revenue:.2f}", ln=True)
        self.ln(10)

    def add_table(self, df):
        self.set_font("Arial", 'B', 12)
        col_widths = [40, 40, 30, 30, 30]
        headers = ['Date', 'Product', 'Units Sold', 'Unit Price', 'Revenue']
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1)
        self.ln()

        self.set_font("Arial", "", 12)
        for _, row in df.iterrows():
            self.cell(col_widths[0], 10, row['Date'], border=1)
            self.cell(col_widths[1], 10, row['Product'], border=1)
            self.cell(col_widths[2], 10, str(row['Units Sold']), border=1)
            self.cell(col_widths[3], 10, f"₹{row['Unit Price']}", border=1)
            self.cell(col_widths[4], 10, f"₹{row['Revenue']:.2f}", border=1)
            self.ln()

# Generate PDF
pdf = PDFReport()
pdf.add_page()
pdf.add_summary(total_units, total_revenue, avg_units, avg_revenue)
pdf.add_table(df)
pdf.output("output_report.pdf")
