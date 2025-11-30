import markdown
import os
from pathlib import Path

# Try using reportlab which we already have installed
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO

def markdown_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF using reportlab"""
    print(f"Converting {md_file} to {pdf_file}...")
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Process HTML content
    lines = md_content.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            # H1
            style = ParagraphStyle('CustomH1', parent=styles['Heading1'],
                                 fontSize=24, spaceAfter=12, textColor='#002E5D')
            story.append(Paragraph(line.replace('# ', ''), style))
        elif line.startswith('## '):
            # H2
            style = ParagraphStyle('CustomH2', parent=styles['Heading2'],
                                 fontSize=18, spaceAfter=10, textColor='#0DA49F')
            story.append(Paragraph(line.replace('## ', ''), style))
        elif line.startswith('### '):
            # H3
            style = ParagraphStyle('CustomH3', parent=styles['Heading3'],
                                 fontSize=14, spaceAfter=8)
            story.append(Paragraph(line.replace('### ', ''), style))
        elif line.strip() and not line.startswith('```'):
            # Regular text
            try:
                story.append(Paragraph(line, styles['Normal']))
            except:
                pass
        
        if line.strip() == '---':
            story.append(Spacer(1, 12))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ Created: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

# Convert all markdown files
doc_dir = Path("Documentation")
md_files = list(doc_dir.glob("*.md"))

print(f"Found {len(md_files)} markdown files\n")

for md_file in md_files:
    pdf_file = doc_dir / (md_file.stem + ".pdf")
    markdown_to_pdf(str(md_file), str(pdf_file))

print("\n✅ All conversions complete!")
