from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import datetime
import os

def generate_receipt_pdf_and_barcode(receipt_data: dict, output_dir="receipts"):
    os.makedirs(output_dir, exist_ok=True)

    business = receipt_data.get("business", {})
    customer = receipt_data.get("customer", {})
    items = receipt_data.get("items", [])
    receipt_no = receipt_data.get("receipt_no", "RCP0001")
    seller = receipt_data.get("seller", "Cashier")
    payment_mode = receipt_data.get("payment_mode", "Cash")
    tax_rate = receipt_data.get("tax_rate", 0.075)  # 7.5%
    date = receipt_data.get("date", datetime.now().strftime("%Y-%m-%d"))

    total = sum(item["price"] * item["quantity"] for item in items)
    tax = total * tax_rate
    grand_total = total + tax

    # Generate Barcode
    barcode_path = os.path.join(output_dir, f"{receipt_no}_barcode.png")
    Code128(receipt_no, writer=ImageWriter()).write(open(barcode_path, "wb"))

    # PDF path
    pdf_path = os.path.join(output_dir, f"{receipt_no}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 30

    # Header: Business Info
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, business.get("name", "BUSINESS NAME").upper())
    c.setFont("Helvetica", 10)
    y -= 15
    c.drawCentredString(width / 2, y, f'{business.get("address", "Business Address")} · {business.get("phone", "Phone")}')
    y -= 15
    c.line(30, y, width - 30, y)

    # Customer Info and Receipt Details
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(30, y, f"Customer: {customer.get('name', 'N/A')}")
    c.drawRightString(width - 30, y, f"Receipt No: {receipt_no}")
    y -= 15
    c.drawString(30, y, f"Address: {customer.get('address', 'N/A')}")
    c.drawRightString(width - 30, y, f"Date: {date}")
    y -= 15
    c.drawString(30, y, f"Phone: {customer.get('phone', 'N/A')}")
    y -= 15
    c.line(30, y, width - 30, y)

    # Transaction Table
    y -= 20
    table_data = [["S/N", "Item", "Price", "Qty", "Subtotal"]]
    for idx, item in enumerate(items, start=1):
        subtotal = item["price"] * item["quantity"]
        table_data.append([
            str(idx),
            item["name"],
            f"₦{item['price']:.2f}",
            str(item["quantity"]),
            f"₦{subtotal:.2f}",
        ])

    table = Table(table_data, colWidths=[40, 180, 80, 50, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, y - 20 - 20 * len(items))

    y -= 40 + 20 * len(items)

    # Totals
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 30, y, f"TAX (7.5%):   ₦{tax:.2f}")
    y -= 15
    c.drawRightString(width - 30, y, f"TOTAL:        ₦{grand_total:.2f}")
    y -= 25
    c.line(30, y, width - 30, y)

    # Seller and Signatures
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(30, y, f"Seller: {seller}")
    y -= 20
    c.drawString(30, y, "Customer Signature: ______________________")
    y -= 20
    c.drawString(30, y, "Seller Signature:   ______________________")

    # Barcode
    c.drawImage(barcode_path, width / 2 - 70, y - 70, width=140, height=40, preserveAspectRatio=True)
    y -= 80

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, y, "THANK YOU FOR YOUR PURCHASE!")

    c.save()
    return pdf_path
