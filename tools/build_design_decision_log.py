from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUTPUT = Path(r"C:\Users\MAW\source\repos\SentiLingo\SentiLingo_Design_Decision_Log.docx")

NAVY = "18324A"
PALE_BLUE = "EAF2F8"
PALE_GRAY = "F5F7F9"
BORDER = "D9D9D9"
TEXT = RGBColor(31, 41, 55)
MUTED = RGBColor(91, 102, 116)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_border(cell, color=BORDER, size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=110, start=130, bottom=110, end=130):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def keep_table_row_together(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def keep_with_next(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    keep = OxmlElement("w:keepNext")
    p_pr.append(keep)


def remove_paragraph_borders(paragraph_or_style):
    element = paragraph_or_style._element
    p_pr = element.get_or_add_pPr()
    border = p_pr.find(qn("w:pBdr"))
    if border is not None:
        p_pr.remove(border)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = " PAGE "
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char_begin)
    run._r.append(instr_text)
    run._r.append(fld_char_end)
    run.font.size = Pt(9)
    run.font.color.rgb = MUTED


def add_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    header = table.rows[0]
    set_repeat_table_header(header)
    keep_table_row_together(header)

    for idx, text in enumerate(headers):
        cell = header.cells[idx]
        cell.width = widths[idx]
        set_cell_shading(cell, NAVY)
        set_cell_border(cell)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        keep_with_next(p)
        r = p.add_run(text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    for row_idx, values in enumerate(rows):
        row = table.add_row()
        keep_table_row_together(row)
        fill = "FFFFFF" if row_idx % 2 == 0 else PALE_BLUE
        for idx, value in enumerate(values):
            cell = row.cells[idx]
            cell.width = widths[idx]
            set_cell_shading(cell, fill)
            set_cell_border(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(value)
            r.font.size = Pt(9.5)
            r.font.color.rgb = TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_labeled_paragraph(doc, label, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.12
    lead = p.add_run(label + " ")
    lead.bold = True
    lead.font.color.rgb = RGBColor(24, 50, 74)
    body = p.add_run(text)
    body.font.color.rgb = TEXT
    return p


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
normal.font.size = Pt(10.5)
normal.font.color.rgb = TEXT
normal.paragraph_format.space_after = Pt(7)
normal.paragraph_format.line_spacing = 1.12

title_style = styles["Title"]
title_style.font.name = "Aptos Display"
title_style._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
title_style._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
title_style.font.size = Pt(27)
title_style.font.bold = True
title_style.font.color.rgb = RGBColor(0, 0, 0)
remove_paragraph_borders(title_style)

for style_name, size, before, after in (
    ("Heading 1", 17, 15, 7),
    ("Heading 2", 13, 11, 5),
):
    style = styles[style_name]
    style.font.name = "Aptos Display"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True

footer = section.footer
footer_p = footer.paragraphs[0]
add_page_number(footer_p)

title = doc.add_paragraph(style="Title")
title.paragraph_format.space_after = Pt(8)
remove_paragraph_borders(title)
title.add_run("SentiLingo Design Decision Log")

subtitle = doc.add_paragraph()
subtitle.paragraph_format.space_after = Pt(18)
subtitle_run = subtitle.add_run("Capstone project decisions and accepted tradeoffs")
subtitle_run.font.size = Pt(13)
subtitle_run.font.color.rgb = MUTED

intro = doc.add_paragraph()
intro.paragraph_format.space_after = Pt(12)
intro.add_run(
    "This log records the choices agreed by the five-person official team, including the three core developers, the alternatives not selected, "
    "and the consequences of those tradeoffs. The purpose is to prevent scope drift during the five-week "
    "delivery period and to preserve the reasoning for the final report and presentation."
)

doc.add_heading("Current Project Constraints", level=1)
add_table(
    doc,
    ["Constraint", "Current position", "Planning effect"],
    [
        (
            "Presentation date",
            "4 December 2026",
            "A stable demonstration and presentation material must be ready before this date.",
        ),
        (
            "Submission deadline",
            "Not yet confirmed",
            "Do not assume that the presentation date is also the submission deadline. Confirm this separately.",
        ),
        (
            "Team availability",
            "Five official members; three core developers have full-time 9-to-5 jobs",
            "Assign one accountable owner per deliverable, plan evening and weekend work conservatively, and keep the first release narrow.",
        ),
        (
            "Delivery period",
            "Five weeks",
            "Prefer a complete, measurable minimum viable product over optional features that may remain unfinished.",
        ),
        (
            "Available local compute",
            "Core i7 laptop, 15.7 GB RAM, RTX 4050 Laptop GPU with 6 GB VRAM",
            "Use the laptop for development, classical models, inference, and transformer smoke tests; use hosted GPUs for the main transformer runs.",
        ),
    ],
    [Inches(1.45), Inches(2.0), Inches(3.45)],
)

doc.add_heading("Decision Index", level=1)
add_table(
    doc,
    ["ID", "Decision", "Status", "Agreed"],
    [
        ("DD 001", "Language scope", "Approved", "23 October 2026"),
        ("DD 002", "Sentiment labels", "Approved", "24 October 2026"),
        ("DD 003", "Classical model suite", "Approved", "24 October 2026"),
        ("DD 004", "TF IDF representation", "Approved", "24 October 2026"),
        ("DD 005", "Advanced model strategy", "Approved", "24 October 2026"),
        ("DD 006", "User interface architecture", "Approved", "24 October 2026"),
        ("DD 007", "Deployment strategy", "Approved", "24 October 2026"),
        ("DD 008", "Model selection metric", "Approved", "24 October 2026"),
        ("DD 009", "Training compute strategy", "Approved", "24 October 2026"),
        ("DD 010", "Database persistence architecture", "Approved", "2 November 2026"),
        ("DD 011", "Multi-page dashboard UI and UX", "Approved", "3 November 2026"),
    ],
    [Inches(0.8), Inches(3.2), Inches(1.3), Inches(1.6)],
)

doc.add_heading("DD 001 Language Scope", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "The first release will support English, Modern Standard Arabic, and Egyptian Arabic. Franco-Arabic is outside the core scope. Mixed Arabic-English text may be observed during testing but is not a required capability.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "These varieties match the project goal while remaining realistic for a five-person official team whose three core developers have full-time jobs. The scope still provides meaningful multilingual and dialectal challenges without adding another writing system.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Add Franco-Arabic",
            "It requires separate normalization for Latin letters and number substitutions, and suitable labelled data may be limited.",
            "The first model may misclassify or reject Arabizi such as 'el service 7elwa'. The limitation must be stated in the report and demo.",
        ),
        (
            "Support many Arabic dialects",
            "Each dialect adds vocabulary, spelling variation, data collection, and evaluation work.",
            "Performance outside Modern Standard Arabic and Egyptian Arabic will be unknown and should not be claimed.",
        ),
        (
            "Treat all Arabic as one variety",
            "This would hide differences between formal Arabic and Egyptian expressions during evaluation.",
            "The team must tag or infer the Arabic variety where possible and report results separately, even if one model serves both.",
        ),
    ],
    [Inches(1.45), Inches(2.6), Inches(2.85)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "Dataset discovery, manual inspection, preprocessing experiments, and evaluation must cover all three supported varieties. The team should maintain per-language or per-variety results so strong English performance cannot hide weak Arabic performance.",
)

doc.add_heading("DD 002 Sentiment Labels", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "The model will predict one of three sentiment labels: Positive, Neutral, or Negative.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "Three labels preserve neutral statements while keeping annotation, model training, evaluation, and demonstration manageable within five weeks.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Positive and Negative only",
            "A binary setup is simpler but forces factual or unclear statements into an opinion category.",
            "The project keeps a harder classification problem and must collect enough neutral examples. In return, neutral predictions remain useful and interpretable.",
        ),
        (
            "Five-level sentiment or star ratings",
            "Fine differences such as slightly positive versus very positive require more consistent labels and more data.",
            "The model will not estimate sentiment intensity. The interface and report must avoid claims such as 'very positive' unless added later.",
        ),
        (
            "Emotion detection",
            "Emotions such as joy, anger, sadness, and fear form a different multi-class or multi-label task.",
            "The model will identify overall opinion polarity, not the specific emotion behind the text.",
        ),
        (
            "Aspect-based sentiment",
            "A sentence may praise one aspect and criticize another, which requires aspect extraction and multiple predictions.",
            "The first release will return one overall label and may lose mixed opinions such as 'good quality but expensive'.",
        ),
    ],
    [Inches(1.45), Inches(2.6), Inches(2.85)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "Every dataset must be mapped consistently to the same three labels. The team must document how ambiguous, sarcastic, mixed-sentiment, and conflicting examples are handled during data review.",
)

doc.add_heading("DD 003 Classical Model Suite", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "The classical comparison will include a dummy classifier, Multinomial Naive Bayes, Logistic Regression, and Linear SVM.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "This set establishes a minimum score, covers distinct learning approaches, and provides credible text-classification baselines without spending time on algorithms that are poorly matched to sparse text features.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Dummy and Logistic Regression only",
            "This is fast but provides a limited comparison and less learning value.",
            "The selected plan requires more experiments but gives the team stronger evidence for model selection.",
        ),
        (
            "Broad algorithm search",
            "Random Forest, K nearest neighbors, and boosting add time and are not the first choice for high-dimensional sparse text.",
            "The report will not claim that every algorithm family was tested; it will justify the focused comparison instead.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "All four baselines must use the same data splits and evaluation policy. Linear SVM scores must not be presented as probabilities unless the model is calibrated.",
)

doc.add_heading("DD 004 TF IDF Representation", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "The team will test word TF-IDF, character TF-IDF, and a combined word and character representation.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "Word features preserve recognizable phrases, while character features help with Arabic morphology, dialectal spelling, and informal variation. Testing the three configurations shows whether the additional complexity improves validation performance.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Word features only",
            "They are easier to explain but more sensitive to spelling and word-form variation.",
            "The project accepts additional memory use to test whether character features improve Arabic performance.",
        ),
        (
            "Character features only",
            "They handle variation but are less interpretable and may lose useful word-level meaning.",
            "The project retains word-level evidence and will compare it fairly with character evidence.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "The combined representation is not assumed to win. The team will select it only if its validation improvement justifies its memory and latency cost.",
)

doc.add_heading("DD 005 Advanced Model Strategy", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "XLM-R Base is the required advanced model. MARBERT may be fine-tuned on the Arabic subset only after the classical baselines, XLM-R, and evaluation pipeline are stable. BiLSTM remains conditional on an instructor requirement.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "XLM-R provides one multilingual pipeline for English and Arabic. MARBERT creates a useful dialect-aware comparison without becoming a dependency for the finished application.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Separate required models by language",
            "Routing, deployment, and mixed-language handling would add significant complexity.",
            "The required application uses one multilingual model and may not reach the best possible score for every language.",
        ),
        (
            "Multilingual BERT as the main model",
            "It is a valid baseline, but XLM-R offers a stronger fit for the planned multilingual comparison.",
            "The project will not include an extra transformer unless an instructor requirement or clear research need appears.",
        ),
        (
            "MARBERT as a required model",
            "It does not cover English and would force a multi-model application architecture.",
            "MARBERT results may be absent if the required work consumes the available schedule.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "The team must define a checkpoint before starting MARBERT. Optional training stops if it threatens integration, evaluation, documentation, or rehearsal.",
)

doc.add_heading("DD 006 User Interface Architecture", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "A Streamlit application is required. A FastAPI inference service is optional and begins only after the local Streamlit workflow is reliable.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "Streamlit provides a practical interface for single-text and CSV prediction. FastAPI adds service separation and API experience without becoming a condition for a complete demonstration.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Notebook-only demonstration",
            "It is fragile during presentations and provides a weak user experience.",
            "The team accepts additional interface work to produce a portfolio-ready demonstration.",
        ),
        (
            "Gradio application",
            "It is effective for quick model demos, but Streamlit better supports the planned batch table and analysis views.",
            "The team will learn Streamlit rather than maintain two interface frameworks.",
        ),
        (
            "FastAPI required from the start",
            "It would add integration work before the prediction workflow is proven.",
            "The initial application may be less production-like, but it remains complete if the optional API is dropped.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "The prediction logic must remain separate from the Streamlit page so that FastAPI can reuse it later. The interface must support Arabic right-to-left display and explain confidence correctly.",
)

doc.add_heading("DD 007 Deployment Strategy", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "The required delivery is local-first. Docker and Azure deployment are stretch goals attempted only after the core pipeline, evaluation, demonstration, and documentation are stable.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "A reliable offline demonstration protects the presentation from internet, account, quota, and cloud-service failures while preserving a path to deployment experience.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Local delivery only",
            "It removes deployment risk but provides less cloud and container experience.",
            "The team keeps deployment available as a stretch goal rather than excluding it.",
        ),
        (
            "Public Streamlit hosting required",
            "Large model memory and changing service limits create delivery risk.",
            "Recruiters may not receive a permanent public demo link if Azure or other hosting is not completed.",
        ),
        (
            "Azure required from the start",
            "It adds cost, permissions, infrastructure work, and external dependencies before model quality is established.",
            "The project may finish without a live Azure endpoint unless the instructor makes it mandatory.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "The team will maintain documented local startup instructions and an offline presentation fallback even if cloud deployment succeeds.",
)

doc.add_heading("DD 008 Model Selection Metric", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "The primary validation score is the mean of the macro-F1 scores calculated separately for English, MSA, and Egyptian Arabic. Accuracy, overall macro-F1, weighted F1, per-class metrics, confusion matrices, latency, and model size remain supporting evidence.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "Equal language weighting prevents a large English subset from hiding weak Arabic performance. Macro-F1 within each language also gives Positive, Neutral, and Negative equal importance.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Accuracy",
            "A majority class or language can make a weak model appear strong.",
            "Accuracy remains in the report but cannot decide the winner by itself.",
        ),
        (
            "Weighted F1",
            "Frequent classes receive more influence and may hide minority-class failure.",
            "The result may look lower than weighted F1, but it is more aligned with the stated scope.",
        ),
        (
            "Overall macro F1 only",
            "It balances sentiment labels but may still be dominated by the largest language subset.",
            "The project uses a custom selection score that must be defined clearly in the report and presentation.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "Model and hyperparameter choices use validation data only. The frozen test set is evaluated once after the full configuration is locked.",
)

doc.add_heading("DD 009 Training Compute Strategy", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "Use local CPU resources for data work and classical models, the RTX 4050 laptop GPU for transformer smoke tests and inference, and Kaggle or Colab GPUs for the main XLM-R and optional MARBERT runs. Azure compute remains optional.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "The laptop is a strong development machine, but its 6 GB of GPU memory constrains full transformer experiments. The hybrid approach uses hosted GPU memory when it provides the most value.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "Local CPU only",
            "Transformer fine-tuning would be too slow for repeated experiments.",
            "The project depends on at least one GPU environment for practical transformer training.",
        ),
        (
            "Local GPU only",
            "Six GB of VRAM may force very small batches and create out-of-memory failures.",
            "Training requires consistent environments and disciplined transfer of datasets, checkpoints, and results.",
        ),
        (
            "Azure training required",
            "It may create cost, quota, and account dependencies that are unnecessary for the core learning objective.",
            "Azure training experience may be omitted if free or student credits are unavailable.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "Every experiment record must include the data version, split version, model, tokenizer, hyperparameters, seed, hardware, duration, metrics, and checkpoint location.",
)

doc.add_heading("DD 010 Database Persistence Architecture", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "Use a minimal, vendor-neutral experiment and model registry with four logical tables: dataset versions, experiment runs, metric results, and artifacts. SQLite is the preferred local implementation if persistence is added. Raw feedback, user accounts, credentials, and prediction history are not stored.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "The registry makes experiments traceable and demonstrates database design while remaining compatible with a local, offline capstone demonstration and the five-week schedule.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "No operational database",
            "Files alone are simple but provide weaker integrity constraints and make cross-run audit queries harder.",
            "The team accepts a small persistence task and must keep the schema narrow and well tested.",
        ),
        (
            "Full application database",
            "Accounts, authentication, prediction history, and analytics would consume time needed for data quality and model evaluation.",
            "The first release is local and single-team, with no sign-in, personal history, or multi-user concurrency.",
        ),
        (
            "Cloud-managed database",
            "It adds credentials, networking, cost, and availability risks without improving the required offline demonstration.",
            "Cloud database operations will not appear in the first release, although the logical schema remains portable.",
        ),
        (
            "Store model binaries in the database",
            "Large binary objects make backups and transfers unnecessarily heavy.",
            "Model files require organised external storage; the registry keeps their paths, checksums, and metadata.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "Every selected model must be traceable to one run, one immutable dataset version, its language-scoped metrics, and its referenced artifacts. Prediction logging remains disabled unless a later privacy review approves it.",
)

doc.add_heading("DD 011 Multi Page Dashboard UI and UX", level=1)
add_labeled_paragraph(
    doc,
    "Decision.",
    "Use a multi-page local Streamlit dashboard with Overview, Analyze Text, Analyze CSV, Results, Model Performance, Experiment Registry, and Help pages. Prediction results remain in the current session; the history view contains model experiments only.",
)
add_labeled_paragraph(
    doc,
    "Reason.",
    "The architecture separates business workflows from technical evidence, supports Arabic and batch analysis, and produces a portfolio-ready demonstration without reversing the approved privacy and database boundaries.",
)
doc.add_heading("Alternatives Not Selected", level=2)
add_table(
    doc,
    ["Alternative", "Why it was not selected", "Consequence of skipping it"],
    [
        (
            "One combined page",
            "It is quickest to build but crowds text input, file upload, results, model evidence, and guidance into one long screen.",
            "The selected architecture requires more navigation and integration testing but gives each user goal a clearer workspace.",
        ),
        (
            "Two analysis tabs only",
            "It handles prediction but provides limited space for analytics, evaluation evidence, experiment traceability, and portfolio storytelling.",
            "The team accepts a larger interface surface and must reuse shared components and state consistently.",
        ),
        (
            "Persistent prediction history",
            "It would store customer text or derived records, expand the database, and require retention, access control, and privacy decisions.",
            "Users cannot reopen previous prediction sessions; they export the current batch when results must be retained.",
        ),
        (
            "User and role administration",
            "Authentication and permissions are not required for the local capstone demonstration and would displace model-quality work.",
            "The first release is a single-team local tool rather than a multi-tenant production service.",
        ),
    ],
    [Inches(1.65), Inches(2.65), Inches(2.6)],
)
add_labeled_paragraph(
    doc,
    "Implementation consequence.",
    "The team must define a shared prediction result contract before building pages, design every empty and error state, test Arabic direction and keyboard use, and stop optional visual polish if it threatens evaluation, documentation, or rehearsal.",
)

doc.add_heading("Pending Decisions", level=1)
pending_intro = doc.add_paragraph(
    "The following choices are intentionally open. They should be agreed before implementation expands beyond data discovery and manual inspection."
)
pending_intro.paragraph_format.space_after = Pt(9)
add_table(
    doc,
    ["Decision needed", "Why it matters"],
    [
        ("Exact submission deadline", "Controls the true freeze date for the report, code, and demonstration."),
        ("Instructor Azure requirement", "If Azure is mandatory, cloud work must move from stretch scope into the required schedule."),
        ("Instructor BiLSTM requirement", "If BiLSTM is mandatory, it must be scheduled as a controlled comparison rather than an optional experiment."),
    ],
    [Inches(2.35), Inches(4.55)],
)

doc.add_heading("How the Team Will Maintain This Log", level=1)
for text in (
    "Add a decision only after the team agrees to it.",
    "Record the rejected alternatives and their consequences at the same time as the decision.",
    "If a decision changes, keep the old entry, mark it superseded, and add the replacement decision with the new reason.",
    "Review the log at the start of each week and before adding a feature that changes scope.",
):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    p.add_run(text)

doc.core_properties.title = "SentiLingo Design Decision Log"
doc.core_properties.subject = "Capstone project decisions, alternatives, and consequences"
doc.core_properties.author = "SentiLingo Team"
doc.core_properties.keywords = "SentiLingo, capstone, design decisions, sentiment analysis"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)
