from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Türkçe Destekli Font Kaydı (Linux Sistemleri İçin)
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

def generate_pdf_report(filename="IT_Audit_Executive_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='DejaVu-Bold',
        fontSize=18,
        textColor=colors.HexColor("#1F497D"),
        spaceAfter=12
    )
    
    sub_title = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='DejaVu',
        fontSize=10,
        textColor=colors.gray,
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        'BodyTR',
        parent=styles['Normal'],
        fontName='DejaVu',
        fontSize=10,
        leading=14
    )

    story.append(Paragraph("IT AUDIT EXECUTIVE REPORT", title_style))
    story.append(Paragraph("Denetim Kapsamı: Active Directory & Linux Sistem Güvenliği | Tarih: 2026-08-28", sub_title))
    story.append(Spacer(1, 10))

    summary_text = """
    <b>Özet Değerlendirme:</b> Yapılan otomatik denetim çalışmalarında 19.223 güvenlik olayı taranmış, 
    sistem üzerinde <b>2 adet Kritik</b> ve <b>1 adet Orta</b> seviye güvenlik riski tespit edilmiştir. 
    Özellikle UID 0 yetkili ek kullanıcılar ve parolasız hesaplar acil müdahale gerektirmektedir.
    """
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 15))

    table_data = [
        ["Kullanıcı", "Risk", "ISO 27001", "Bulgu Özeti"],
        ["hacker_test", "Kritik", "A.9.2.3", "UID 0 (Root) yetkili yetkisiz hesap."],
        ["nopass_user", "Kritik", "A.9.4.3", "Aktif hesabın parolası boş."],
        ["S-1-5-18", "Orta", "A.12.4.1", "10 dk içinde 8 başarısız giriş denemesi."]
    ]

    t = Table(table_data, colWidths=[90, 60, 70, 280])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F497D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, 2), colors.HexColor("#FFC7CE")),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#FFEB9C")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    story.append(t)
    doc.build(story)
    print(f"[+] Düzeltilmiş PDF Raporu Başarıyla Oluşturuldu: {filename}")

if __name__ == "__main__":
    generate_pdf_report()
