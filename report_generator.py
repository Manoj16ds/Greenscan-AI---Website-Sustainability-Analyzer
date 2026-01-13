from fpdf import FPDF
import os
from datetime import datetime

def sanitize_text(text):
    replacements = {
        '–': '-', '—': '-', '•': '*', '“': '"', '”': '"',
        '‘': "'", '’': "'", '…': '...', '🌐': '', '🧠': '',
        '✅': '', '🖼️': '', '🔗': '', '📄': '', '♻️': '', '🔹': '', '🛠️': ''
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text.encode('latin-1', errors='ignore').decode('latin-1')

class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "GreenScan AI - Website Sustainability Report", 0, 1, "C")
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
        self.cell(0, 10, f"Page {self.page_no()}  -  Generated on {date_str}", 0, 0, "C")

def generate_pdf_report(filename, url, total_images, page_size_kb, carbon, classification,
                        suggestions_dict, optimized_size_kb, optimized_carbon, num_pages):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 1️⃣ Cover Page
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 15, sanitize_text("GreenScan AI"), ln=True, align='C')
    pdf.set_font("Arial", "", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, sanitize_text("Eco-Friendly Website Analysis Report"), ln=True, align='C')
    pdf.ln(15)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, sanitize_text(
        f"Website Analyzed: {url}\nDate: {datetime.now().strftime('%d %B %Y')}\nPages Scanned: {num_pages}\n\n"
        f"This report analyzes the environmental impact of this website based on image usage, page size, and CO2 emissions. "
        f"AI-based suggestions are provided for improving sustainability."
    ))
    pdf.ln(10)
    pdf.cell(0, 10, sanitize_text("Prepared using GreenScan AI - Developed by Manoj D S & Aruneswar Meera S"), ln=True, align='C')

    # 2️⃣ Summary Page
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, sanitize_text(f"Website: {url}"))
    pdf.cell(0, 10, sanitize_text(f"Pages Scanned: {num_pages}"), ln=1)
    pdf.cell(0, 10, sanitize_text(f"Images Found: {total_images}"), ln=1)
    pdf.cell(0, 10, sanitize_text(f"Page Size (Original): {page_size_kb} KB"), ln=1)
    pdf.cell(0, 10, sanitize_text(f"CO2 Emissions (Original): {carbon} kg/month"), ln=1)
    pdf.cell(0, 10, sanitize_text(f"Page Size (Optimized): {optimized_size_kb} KB"), ln=1)
    pdf.cell(0, 10, sanitize_text(f"CO2 Emissions (Optimized): {optimized_carbon} kg/month"), ln=1)

    # 3️⃣ Image Classification
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, sanitize_text("Image Classification:"), ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, sanitize_text(f"  * Essential Images: {len(classification['essential'])}"), ln=1)
    pdf.cell(0, 10, sanitize_text(f"  * Decorative Images: {len(classification['decorative'])}"), ln=1)

    # 4️⃣ Page wise Suggestions
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, sanitize_text("Page-wise Suggested Improvements:"), ln=1)
    pdf.set_font("Arial", "", 12)

    for page_url, tips in suggestions_dict.items():
        pdf.ln(3)
        pdf.multi_cell(0, 10, sanitize_text(f"📄 {page_url}"))
        for tip in tips:
            pdf.multi_cell(0, 10, sanitize_text(f"   🔹 {tip}"))

    # 5️⃣ Visual Charts
    chart_files = [
        ("Image Classification", "classification_pie.png"),
        ("Page Size vs CO2 Emission", "carbon_vs_size.png"),
        ("Emission Comparison", "emission_comparison.png")
    ]

    for title, img_path in chart_files:
        if os.path.exists(img_path):
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, sanitize_text(title), ln=1)
            pdf.image(img_path, w=180)

    # ✅ Save the PDF
    pdf.output(filename)
