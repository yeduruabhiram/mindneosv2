#!/usr/bin/env python3
"""
Generate PDF from MindNeox AI Features Documentation
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import re

def create_pdf():
    """Create professional PDF from markdown"""
    
    # Read markdown file
    with open('MINDNEOX_AI_FEATURES_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    pdf_filename = 'MindNeox_AI_Features_Documentation.pdf'
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#8b5cf6'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        leftIndent=20,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#1f2937'),
        backColor=colors.HexColor('#f3f4f6'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=10
    )
    
    # Parse markdown and add to PDF
    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            elements.append(Spacer(1, 6))
            continue
        
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_lines)
                elements.append(Paragraph(code_text, code_style))
                code_lines = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # Title (# )
        if line.startswith('# ') and not line.startswith('##'):
            text = line[2:].strip()
            # Remove emojis for PDF
            text = re.sub(r'[^\w\s\-.,!?():]', '', text)
            elements.append(Paragraph(text, title_style))
            elements.append(Spacer(1, 12))
            continue
        
        # Heading 1 (##)
        if line.startswith('## ') and not line.startswith('###'):
            text = line[3:].strip()
            text = re.sub(r'[^\w\s\-.,!?():]', '', text)
            elements.append(Paragraph(text, heading1_style))
            continue
        
        # Heading 2 (###)
        if line.startswith('### ') and not line.startswith('####'):
            text = line[4:].strip()
            text = re.sub(r'[^\w\s\-.,!?():]', '', text)
            elements.append(Paragraph(text, heading2_style))
            continue
        
        # Heading 3 (####)
        if line.startswith('#### '):
            text = line[5:].strip()
            text = re.sub(r'[^\w\s\-.,!?():]', '', text)
            elements.append(Paragraph(text, heading3_style))
            continue
        
        # Horizontal rule
        if line.startswith('---'):
            elements.append(Spacer(1, 12))
            continue
        
        # Bullet points
        if line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # Remove markdown formatting
            text = text.replace('**', '').replace('*', '').replace('`', '')
            text = re.sub(r'[^\w\s\-.,!?():\/]', '', text)
            elements.append(Paragraph(f'• {text}', bullet_style))
            continue
        
        # Checkboxes
        if line.startswith('- [ ]') or line.startswith('- [x]') or line.startswith('- [✅]'):
            checked = '[x]' in line or '[✅]' in line or '✅' in line
            text = line.split(']', 1)[1].strip() if ']' in line else line
            text = text.replace('**', '').replace('*', '').replace('`', '')
            text = re.sub(r'[^\w\s\-.,!?():\/]', '', text)
            symbol = '☑' if checked else '☐'
            elements.append(Paragraph(f'{symbol} {text}', bullet_style))
            continue
        
        # Regular paragraph
        text = line
        # Remove markdown formatting
        text = text.replace('**', '<b>').replace('**', '</b>')
        text = text.replace('*', '<i>').replace('*', '</i>')
        text = text.replace('`', '<font name="Courier">')
        text = text.replace('`', '</font>')
        # Remove remaining emojis
        text = re.sub(r'[^\w\s\-.,!?():<>/]', '', text)
        
        if text:
            elements.append(Paragraph(text, body_style))
    
    # Build PDF
    doc.build(elements)
    print(f'✅ PDF created successfully: {pdf_filename}')
    return pdf_filename

if __name__ == '__main__':
    try:
        pdf_file = create_pdf()
        print(f'\n📄 PDF Location: {pdf_file}')
        print(f'📊 Document contains all MindNeox AI features')
        print(f'🎉 Ready to share!')
    except Exception as e:
        print(f'❌ Error creating PDF: {e}')
        import traceback
        traceback.print_exc()
