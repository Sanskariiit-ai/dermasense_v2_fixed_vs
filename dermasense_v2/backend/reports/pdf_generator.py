from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

DISCLAIMER = (
    "This report summarises what was discussed in a chat with DermaSense. It is not a medical diagnosis "
    "and does not replace examination by a qualified health professional."
)


def create_report(patient: dict, symptoms: list[dict], conditions: list[dict], transcript: list[dict]) -> bytes:
    """Build the PDF in memory and return its bytes. All user text is XML-escaped for reportlab."""
    buf = BytesIO()
    pdf = SimpleDocTemplate(buf, title="DermaSense report")
    styles = getSampleStyleSheet()
    p = lambda text, style="BodyText": Paragraph(escape(str(text)), styles[style])
    out = [p("DermaSense Report", "Title"), Spacer(1, 12)]
    out += [p(f"Patient: {patient.get('name', '')}"), p(f"Age: {patient.get('age', '')}"), p(f"Gender: {patient.get('gender', '')}")]
    out += [Spacer(1, 12), p("Symptoms mentioned", "Heading2")]
    out += [p(f"{s['symptom']} ({s.get('category', 'general')})") for s in symptoms] or [p("None recorded.")]
    out += [Spacer(1, 12), p("Possible conditions to discuss with a doctor", "Heading2")]
    for c in conditions:
        out.append(p(f"{c['condition']}: {c['description']}"))
        out += [p(f"- {r}") for r in c.get("recommendations", [])]
    if not conditions:
        out.append(p("None suggested."))
    out += [Spacer(1, 12), p("Conversation excerpt", "Heading2")]
    out += [p(f"{m['role'].title()}: {m['content']}") for m in transcript[-12:]] or [p("No messages.")]
    out += [Spacer(1, 18), p(DISCLAIMER, "Italic")]
    pdf.build(out)
    return buf.getvalue()
