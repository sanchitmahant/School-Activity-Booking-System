"""
Professional Prospectus Generator - World-Class Design
Enhanced with premium layout, professional imagery references, and elite school branding
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas

def add_header_footer(canvas_obj, doc):
    """Add professional header and footer to each page"""
    canvas_obj.saveState()
    width, height = A4
    
    # Footer
    canvas_obj.setFillColor(colors.HexColor('#002E5D'))
    canvas_obj.rect(0, 0, width, 0.5*inch, fill=True, stroke=False)
    
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(colors.HexColor('#D4AF37'))
    canvas_obj.drawCentredString(width/2, 0.2*inch, 
        "Greenwood International School | Henley-on-Thames, Oxfordshire | www.greenwood.edu")
    
    # Page number
    canvas_obj.setFillColor(colors.white)
    canvas_obj.drawRightString(width - 0.75*inch, 0.2*inch, str(doc.page))
    
    canvas_obj.restoreState()

def generate_prospectus():
    """Generate Professional Greenwood International School Prospectus PDF"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        topMargin=0.75*inch, 
        bottomMargin=0.75*inch,
        leftMargin=1*inch, 
        rightMargin=1*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # PROFESSIONAL CUSTOM STYLES
    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=42,
        textColor=colors.HexColor('#002E5D'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=48
    )
    
    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Heading2'],
        fontSize=24,
        textColor=colors.HexColor('#0DA49F'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=30
    )
    
    motto_style = ParagraphStyle(
        'Motto',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#D4AF37'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique',
        spaceBefore=20,
        spaceAfter=20,
        leading=20
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#002E5D'),
        spaceBefore=25,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#D4AF37'),
        borderPadding=10,
        backColor=colors.HexColor('#F8F9FA')
    )
    
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=14,
        leading=17,
        textColor=colors.HexColor('#333333')
    )
    
    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#0DA49F'),
        leftIndent=40,
        rightIndent=40,
        spaceBefore=15,
        spaceAfter=15,
        leading=18
    )
    
    # ==================== COVER PAGE ====================
    elements.append(Spacer(1, 1*inch))
    
    # School Crest/Logo (represented by decorative border)
    elements.append(Paragraph("🏛️", ParagraphStyle('crest', alignment=TA_CENTER, fontSize=48, spaceAfter=20)))
    
    elements.append(Paragraph("GREENWOOD", cover_title))
    elements.append(Paragraph("INTERNATIONAL SCHOOL", cover_subtitle))
    
    # Decorative line
    elements.append(Spacer(1, 0.3*inch))
    line_data = [['']]
    line_table = Table(line_data, colWidths=[5*inch], rowHeights=[0.05*inch])
    line_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#D4AF37')),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("PROSPECTUS 2025-2026", motto_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Excellence • Tradition • Innovation", quote_style))
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("EST. 1950 | HENLEY-ON-THAMES, OXFORDSHIRE", 
        ParagraphStyle('est', parent=body_text, alignment=TA_CENTER, fontSize=10, textColor=colors.HexColor('#666666'))))
    
    elements.append(PageBreak())
    
    # ==================== TABLE OF CONTENTS ====================
    elements.append(Paragraph("Contents", section_heading))
    elements.append(Spacer(1, 0.2*inch))
    
    toc_data = [
        ['Welcome from the Headmaster', '3'],
        ['About Greenwood International', '4'],
        ['Academic Excellence', '5'],
        ['Beyond the Classroom', '6'],
        ['World-Class Facilities', '7'],
        ['Pastoral Care & Wellbeing', '8'],
        ['Admissions Process', '9'],
        ['Contact Us', '10']
    ]
    
    toc_table = Table(toc_data, colWidths=[4.5*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#002E5D')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#0DA49F')),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(toc_table)
    
    elements.append(PageBreak())
    
    # ==================== WELCOME FROM HEADMASTER ====================
    elements.append(Paragraph("Welcome from the Headmaster", section_heading))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph(
        """<i>"A Greenwood education is transformative, nurturing academic excellence, character, 
        and a lifelong love of learning."</i>""",
        quote_style
    ))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        """Dear Prospective Families,<br/><br/>
        It is my great pleasure to welcome you to Greenwood International School. For over seven decades, 
        Greenwood has stood as a beacon of educational excellence in the heart of Oxfordshire, combining 
        the rich traditions of British independent education with innovative pedagogical approaches.<br/><br/>
        
        At Greenwood, we believe that education extends far beyond examination results. While we are 
        immensely proud of our outstanding academic achievements—consistently placing us among the top 
        independent schools in the United Kingdom—we are equally committed to developing well-rounded 
        individuals who will make meaningful contributions to society.<br/><br/>
        
        Our dedicated faculty, world-class facilities, and vibrant international community create an 
        environment where every student is challenged, supported, and inspired to reach their fullest 
        potential. Whether in the classroom, on the sports field, in the concert hall, or through our 
        extensive extracurricular programmes, Greenwood students are encouraged to discover their passions 
        and develop the skills they need to thrive in an ever-changing world.<br/><br/>
        
        I invite you to explore this prospectus, visit our magnificent campus, and discover what makes 
        Greenwood truly extraordinary. We look forward to welcoming you to our community.<br/><br/>""",
        body_text
    ))
    
    elements.append(Paragraph(
        """<b>Dr. Arthur J. Pendelton, DPhil (Oxon)</b><br/>
        Headmaster<br/>
        <i>Fellow of the Royal Society of Arts</i>""",
        body_text
    ))
    
    elements.append(PageBreak())
    
    # ==================== ABOUT GREENWOOD ====================
    elements.append(Paragraph("About Greenwood International School", section_heading))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        """Founded in 1950 in the aftermath of World War II, Greenwood International School was 
        established with a vision: to create an educational institution that would prepare young people 
        to build a better, more peaceful world. Today, that founding mission continues to guide us as 
        we educate students from over 40 countries.<br/><br/>
        
        Our historic 150-acre campus on the banks of the River Thames combines stunning Victorian 
        architecture with cutting-edge modern facilities. From our Grade II listed Main Hall to our 
        state-of-the-art Science and Technology Centre, Greenwood provides an inspiring setting for 
        learning and personal growth.<br/><br/>
        
        <b>Our Values:</b><br/>
        • <b>Excellence:</b> Pursuing the highest standards in all endeavors<br/>
        • <b>Integrity:</b> Acting with honesty, fairness, and respect<br/>
        • <b>Compassion:</b> Caring for others and serving our community<br/>
        • <b>Curiosity:</b> Maintaining a lifelong love of learning<br/>
        • <b>Courage:</b> Taking risks and embracing challenges<br/><br/>""",
        body_text
    ))
    
    # Key Statistics
    elements.append(Spacer(1, 0.3*inch))
    stats_data = [
        ['Founded', '1950', 'Day & Boarding', 'Ages 3-18'],
        ['Total Students', '850', 'Student-Teacher Ratio', '8:1'],
        ['International Students', '40+ Countries', 'Average Class Size', '12 pupils'],
        ['University Progression', '100%', 'Oxbridge Success (2024)', '15 offers'],
    ]
    
    stats_table = Table(stats_data, colWidths=[2.2*inch]*2 + [2.2*inch]*2)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, -1), colors.HexColor('#002E5D')),
        ('BACKGROUND', (2, 0), (3, -1), colors.HexColor('#0DA49F')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(stats_table)
    
    elements.append(PageBreak())
    
    # ==================== ACADEMIC EXCELLENCE ====================
    elements.append(Paragraph("Academic Excellence", section_heading))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        """<b>Our Curriculum</b><br/>
        Greenwood follows an enhanced version of the English National Curriculum, enriched with 
        international perspectives and advanced academic challenges. Our rigorous programme prepares 
        students for success at the world's leading universities.<br/><br/>
        
        <b>Pre-Preparatory (Ages 3-7)</b><br/>
        Our youngest students benefit from a play-based approach that establishes strong foundations 
        in literacy, numeracy, and social development. Small class sizes ensure individual attention.<br/><br/>
        
        <b>Preparatory School (Ages 7-11)</b><br/>
        The curriculum broadens to include specialist teaching in Sciences, Modern Languages, Music, 
        Art, and Physical Education, fostering independence and critical thinking.<br/><br/>
        
        <b>Senior School (Ages 11-16)</b><br/>
        Students follow a comprehensive GCSE programme with outstanding results: 75% of grades 9-7 (A*-A) 
        in 2024. Core subjects are complemented by extensive options in Humanities, Languages, and Arts.<br/><br/>
        
        <b>Sixth Form (Ages 16-18)</b><br/>
        Our Sixth Form offers 25 A-Level subjects, with exceptional teaching leading to remarkable results: 
        92% A*/A grades in 2024. Students receive dedicated university guidance, including specialized 
        support for Oxbridge and Russell Group applications.<br/><br/>""",
        body_text
    ))
    
    # Results Table
    results_data = [
        ['Examination', '2024 Results', 'UK Average'],
        ['GCSE 9-7 (A*-A)', '75%', '21%'],
        ['A-Level A*/A', '92%', '28%'],
        ['IB Average Points', '38', '30'],
    ]
    
    results_table = Table(results_data, colWidths=[2*inch, 2*inch, 1.5*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002E5D')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(results_table)
    
    elements.append(PageBreak())
    
   # ==================== BEYOND THE CLASSROOM ====================
    elements.append(Paragraph("Beyond the Classroom", section_heading))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        """<b>Extracurricular Excellence</b><br/>
        Education at Greenwood extends far beyond the classroom. Our extensive programme of over 35 
        extracurricular activities ensures that every student discovers their passions and develops 
        new skills.<br/><br/>
        
        <b>Activity Booking Portal:</b> Parents can easily browse and book activities through our 
        innovative online platform, with instant confirmations and automated calendar integration.<br/><br/>
        
        <b>Our Programmes Include:</b><br/>
        • <b>STEM & Innovation:</b> Robotics, Coding, Mathematics Challenge, Science Club<br/>
        • <b>Sports:</b> Rugby, Football, Tennis, Swimming, Athletics, Rowing<br/>
        • <b>Creative Arts:</b> Drama, Music (Orchestra & Ensembles), Fine Arts, Photography<br/>
        • <b>Languages:</b> French, Spanish, Mandarin, German, Latin<br/>
        • <b>Leadership:</b> Duke of Edinburgh Award, Model UN, Debating Society<br/>
        • <b>Community Service:</b> Charity initiatives, volunteer programmes<br/><br/>
        
        <b>Music at Greenwood:</b> Over 60% of students learn a musical instrument, with opportunities 
        to perform in our Chamber Orchestra, Chapel Choir, Jazz Band, or Rock School.<br/><br/>
        
        <b>Sports Achievement:</b> Our teams regularly compete at national level, with recent successes 
        including U16 Rugby National Champions and County Champions in Swimming.<br/><br/>""",
        body_text
    ))
    
    elements.append(PageBreak())
    
    # ==================== FACILITIES ====================
    elements.append(Paragraph("World-Class Facilities", section_heading))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        """Our £30 million investment in facilities over the past decade has created an outstanding 
        learning environment:<br/><br/>
        
        <b>Academic Facilities:</b><br/>
        • New Science Centre with 12 specialist laboratories<br/>
        • Technology Hub featuring 3D printers, laser cutters, and robotics lab<br/>
        • Library with 50,000 volumes and digital research center<br/>
        • Modern Language Centre with cultural immersion rooms<br/>
        • Art School with ceramics, textiles, and printmaking studios<br/><br/>
        
        <b>Sports Complex:</b><br/>
        • Olympic-standard 25m swimming pool<br/>
        • Full-size artificial turf pitch<br/>
        • Eight tennis courts and sports hall<br/>
        • Fitness centre and dance studio<br/>
        • 150-acre grounds with rugby, cricket, and athletics facilities<br/><br/>
       
        <b>Performing Arts:</b><br/>
        • 500-seat theatre with professional lighting and sound<br/>
        • Music School with 20 practice rooms and recording studio<br/>
        • Drama studios and rehearsal spaces<br/><br/>
        
        <b>Boarding Houses:</b><br/>
        Four comfortable boarding houses providing home-away-from-home for 200 boarders, 
        with dedicated housemasters/mistresses and full pastoral support.<br/><br/>""",
        body_text
    ))
    
    elements.append(PageBreak())
    
    # ==================== ADMISSIONS ====================
    elements.append(Paragraph("Admissions Information", section_heading))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        """<b>How to Apply:</b><br/>
        1. Submit online inquiry form via our website or contact our Admissions Office<br/>
        2. Attend an Open Morning or arrange a personal tour<br/>
        3. Complete the application form and pay registration fee (£150)<br/>
        4. Sit entrance assessments (age-appropriate)<br/>
        5. Interview with Head of Section or Headmaster<br/>
        6. Receive offer decision within two weeks<br/><br/>
        
        <b>Important Dates 2025-2026:</b><br/>
        • Open Mornings: 15th March, 10th May, 20th September 2025<br/>
        • Year 7 Entry Application Deadline: 15th October 2025<br/>
        • Sixth Form Application Deadline: 1st December 2025<br/>
        • Entrance Examinations: January 2026<br/>
        • Offer Letters: March 2026<br/><br/>""",
        body_text
    ))
    
    # Fees Table
    fees_data = [
        ['Year Group', 'Day Fees (per term)', 'Boarding Fees (per term)'],
        ['Reception - Year 2', '£5,200', 'N/A'],
        ['Years 3-6', '£6,800', '£10,400'],
        ['Years 7-11', '£8,500', '£13,800'],
        ['Sixth Form (Years 12-13)', '£9,200', '£14,500'],
    ]
    
    fees_table = Table(fees_data, colWidths=[2*inch, 2*inch, 2*inch])
    fees_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002E5D')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
        ('FONT', (0, 0), (-1,0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(fees_table)
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        """<i>Note: Three terms per academic year. Fees include curriculum materials, lunch, and most activities. 
        Music tuition and some specialist activities are charged separately.<br/><br/>
        Scholarships and bursaries available up to 50% of fees based on academic merit and financial need.</i>""",
        ParagraphStyle('note', parent=body_text, fontSize=9, textColor=colors.HexColor('#666666'))
    ))
    
    elements.append(PageBreak())
    
    # ==================== CONTACT ====================
    elements.append(Paragraph("Contact Us", section_heading))
    elements.append(Spacer(1, 0.3*inch))
    
    contact_box_data = [[
        Paragraph("""<b>Greenwood International School</b><br/>
        Greenwood Hall<br/>
        Henley-on-Thames<br/>
        Oxfordshire RG9 1AA<br/>
        United Kingdom<br/><br/>
        
        <b>Telephone:</b> +44 (0) 1491 570000<br/>
        <b>Email:</b> admissions@greenwood.edu<br/>
        <b>Website:</b> www.greenwood.edu<br/><br/>
        
        <b>Admissions Office:</b><br/>
        admissions@greenwood.edu<br/>
        +44 (0) 1491 570001<br/><br/>
        
        <i>We warmly welcome visitors throughout the year. Please contact our Admissions Office 
        to arrange a personal tour of our magnificent campus.</i><br/><br/>
        
        <b>Registered Charity No. 123456</b><br/>
        Company Number: 9876543 (England & Wales)""", body_text)
    ]]
    
    contact_box = Table(contact_box_data, colWidths=[5.5*inch])
    contact_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F8FF')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#002E5D')),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    elements.append(contact_box)
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        """<i>"Where tradition meets innovation, and every student is empowered to excel."</i>""",
        quote_style
    ))
    
    # Build PDF with custom page template
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    buffer.seek(0)
    return buffer

if __name__ == '__main__':
    print("=" * 80)
    print("GENERATING PROFESSIONAL PROSPECTUS")
    print("=" * 80)
    pdf = generate_prospectus()
    with open('Greenwood_Prospectus_2025-2026.pdf', 'wb') as f:
        f.write(pdf.read())
    print("✅ World-class prospectus generated: Greenwood_Prospectus_2025-2026.pdf")
    print("   - Professional design with branded headers/footers")
    print("   - Table of contents")
    print("   - Enhanced typography and layout")
    print("   - Comprehensive content and statistics")
    print("=" * 80)
