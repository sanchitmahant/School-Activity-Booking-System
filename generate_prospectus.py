"""
Generate School Prospectus PDF
Professional prospectus for Greenwood International School
"""
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

def generate_prospectus():
    """Generate Greenwood International School Prospectus PDF"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#002E5D'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#0DA49F'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#002E5D'),
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    # Cover Page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("GREENWOOD", title_style))
    elements.append(Paragraph("INTERNATIONAL SCHOOL", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Prospectus 2025-2026", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Excellence • Tradition • Innovation", body_style))
    
    elements.append(PageBreak())
    
    # Welcome from Headmaster
    elements.append(Paragraph("Welcome from the Headmaster", heading_style))
    elements.append(Paragraph(
        """Dear Prospective Families,<br/><br/>
        Welcome to Greenwood International School. For over 75 years, we have been at the forefront 
        of educational excellence in the United Kingdom. Our mission is to provide a holistic education 
        that empowers students to thrive in a rapidly changing world.<br/><br/>
        At Greenwood, we pride ourselves on our inclusive community, our outstanding pastoral care, 
        and our commitment to academic rigour. Our dedicated staff work tirelessly to ensure that 
        every student reaches their full potential, both inside and outside the classroom.<br/><br/>
        We invite you to explore this prospectus and discover what makes Greenwood truly special.
        """,
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("<i>Dr. Arthur Pendelton, PhD</i><br/>Headmaster", body_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # About Us
    elements.append(Paragraph("About Greenwood", heading_style))
    elements.append(Paragraph(
        """Founded in 1950, Greenwood International School is located in the heart of beautiful 
        Oxfordshire. Our historic campus combines traditional architecture with state-of-the-art 
        facilities, providing an inspiring environment for learning and growth.<br/><br/>
        We are proud of our diverse international community, welcoming students from over 40 countries. 
        This rich cultural tapestry enhances the educational experience for all our students, 
        preparing them for success in an increasingly globalized world.""",
        body_style
    ))
    
    # Key Facts Table
    elements.append(Spacer(1, 0.3*inch))
    key_facts_data = [
        ['Founded', '1950'],
        ['Student-Teacher Ratio', '8:1'],
        ['University Entry Rate', '100%'],
        ['International Students', '40+ Countries'],
        ['Extracurricular Activities', '35+ Clubs'],
        ['Average Class Size', '12 Students']
    ]
    
    key_facts_table = Table(key_facts_data, colWidths=[3*inch, 2*inch])
    key_facts_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#002E5D')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#0DA49F')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(key_facts_table)
    
    elements.append(PageBreak())
    
    # Academic Excellence
    elements.append(Paragraph("Academic Excellence", heading_style))
    elements.append(Paragraph(
        """Our curriculum is designed to challenge and inspire. We offer a broad range of subjects 
        at GCSE and A-Level, with exceptional results year after year. Our students consistently 
        achieve top grades and progress to the world's leading universities, including Oxford, 
        Cambridge, Imperial College London, and prestigious institutions worldwide.<br/><br/>
        <b>Recent Achievements:</b><br/>
        • 92% A*/A grades at A-Level (2024)<br/>
        • 15 students to Oxford/Cambridge (2024)<br/>
        • Top 10 UK independent school ranking<br/>
        • Outstanding Ofsted rating""",
        body_style
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Extracurricular Activities
    elements.append(Paragraph("Beyond the Classroom", heading_style))
    elements.append(Paragraph(
        """Education at Greenwood extends far beyond academics. We offer an extensive programme 
        of extracurricular activities designed to develop well-rounded individuals. From robotics 
        to rugby, from music to mathematics challenges, there's something for every student.<br/><br/>
        <b>Our Activity Booking Portal</b> allows parents to easily browse and book activities 
        for their children, with instant confirmations and automated calendar invites. Activities 
        include:<br/>
        • STEM & Robotics<br/>
        • Sports (Rugby, Football, Tennis, Swimming)<br/>
        • Creative Arts (Drama, Music, Fine Arts)<br/>
        • Languages & Culture<br/>
        • Leadership & Community Service""",
        body_style
    ))
    
    elements.append(PageBreak())
    
    # Facilities
    elements.append(Paragraph("World-Class Facilities", heading_style))
    elements.append(Paragraph(
        """Our campus features:<br/>
        • Modern Science Laboratories<br/>
        • Olympic-Standard Sports Complex<br/>
        • State-of-the-Art Theatre (500 seats)<br/>
        • Professional Music Studios<br/>
        • Extensive Library (50,000+ volumes)<br/>
        • Technology Centre with 3D Printers & Robotics Lab<br/>
        • Beautiful Boarding Houses<br/>
        • Organic School Farm""",
        body_style
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Admissions
    elements.append(Paragraph("Admissions Information", heading_style))
    elements.append(Paragraph(
        """<b>How to Apply:</b><br/>
        1. Submit online inquiry form via our website<br/>
        2. Schedule a campus visit<br/>
        3. Complete application form<br/>
        4. Sit entrance assessments<br/>
        5. Interview with Headmaster<br/><br/>
        <b>Key Dates:</b><br/>
        • Open Day: Saturday, 15th March 2025<br/>
        • Application Deadline: 1st May 2025<br/>
        • Entrance Exams: June 2025<br/>
        • Results: July 2025<br/><br/>
        <b>Fees (2025-2026):</b><br/>
        • Day Students: £25,000 per annum<br/>
        • Boarders: £42,000 per annum<br/>
        • Scholarship opportunities available""",
        body_style
    ))
    
    elements.append(PageBreak())
    
    # Contact Information
    elements.append(Paragraph("Visit Us", heading_style))
    elements.append(Paragraph(
        """<b>Greenwood International School</b><br/>
        Greenwood Hall<br/>
        Henley-on-Thames<br/>
        Oxfordshire, RG9 1AA<br/>
        United Kingdom<br/><br/>
        <b>Email:</b> greenwoodinternationaluk@gmail.com<br/>
        <b>Phone:</b> +44 20 7123 4567<br/>
        <b>Website:</b> www.greenwood.edu.uk<br/><br/>
        <i>We look forward to welcoming you to the Greenwood family.</i>""",
        body_style
    ))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

if __name__ == '__main__':
    print("Generating prospectus...")
    pdf = generate_prospectus()
    with open('Greenwood_Prospectus_2025-2026.pdf', 'wb') as f:
        f.write(pdf.read())
    print("✅ Prospectus generated: Greenwood_Prospectus_2025-2026.pdf")
