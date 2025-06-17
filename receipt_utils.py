from fpdf import FPDF
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io
import tempfile
import os

def generate_receipt_pdf_and_barcode(
    receipt_no,
    timestamp,
    customer_name,
    customer_address,
    customer_phone,
    sales_rep,
    business,
    product,
    quantity,
    total
):
    # Generate barcode
    barcode_io = io.BytesIO()
    ean = barcode.get('code128', receipt_no, writer=ImageWriter())
    ean.write(barcode_io)
    barcode_io.seek(0)

    # Save barcode to temp file
    barcode_img = Image.open(barcode_io)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        barcode_path = tmp_file.name
        barcode_img.save(barcode_path)

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ✅ Business Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, business.name or "No Name", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Address: {business.address or 'N/A'}", ln=True, align="C")
    pdf.cell(0, 8, f"Phone: {business.phone or 'N/A'}", ln=True, align="C")
    pdf.cell(0, 8, f"Account No: {business.account_number or 'N/A'}", ln=True, align="C")

    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Receipt info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Receipt #: {receipt_no}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 8, f"Sales Rep: {sales_rep}", ln=True)
    pdf.ln(5)

    # Customer info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Customer Details", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Name: {customer_name}", ln=True)
    pdf.cell(0, 8, f"Address: {customer_address}", ln=True)
    pdf.cell(0, 8, f"Phone: {customer_phone}", ln=True)
    pdf.ln(5)

    # Product info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Purchase Summary", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Product: {product.name}", ln=True)
    pdf.cell(0, 8, f"Quantity: {quantity}", ln=True)
    pdf.cell(0, 8, f"Unit Price: ${product.price:.2f}", ln=True)
    pdf.cell(0, 8, f"Total: ${total:.2f}", ln=True)
    pdf.ln(10)

    # Barcode
    pdf.image(barcode_path, x=60, w=90)
    pdf.ln(5)
    pdf.cell(0, 10, "Thank you for your purchase!", ln=True, align="C")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    os.remove(barcode_path)

    return pdf_bytes, barcode_io.getvalue()
