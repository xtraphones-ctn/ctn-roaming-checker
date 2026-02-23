"""
Generate 5 corrected PDF files for Compare The Networks / Xtra Phones UK Ltd.
All prices exclude VAT. Modern clean design matching the web pages.
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ──────────────────────────────────────────────────────────────────────
# Colour palette — matches the website design
# ──────────────────────────────────────────────────────────────────────
O2_BLUE     = (0, 160, 225)
VF_RED      = (230, 0, 0)
DARK_BG     = (26, 43, 74)
WHITE       = (255, 255, 255)
BLACK       = (30, 30, 30)
GREY_TEXT   = (100, 100, 100)
LIGHT_BG    = (248, 249, 251)
ROW_ALT     = (243, 245, 249)
BORDER      = (220, 225, 235)
ACCENT      = (0, 102, 204)
GREEN       = (10, 138, 62)

FONT_DIR = "C:/Windows/Fonts/"
FONT = "Arial"
DATE_STR = "February 2026"
COMPANY = "Compare The Networks"
LEGAL = "Xtra Phones UK Ltd"


class CTNDoc(FPDF):
    def __init__(self, title, network="both", date=DATE_STR):
        super().__init__()
        self.doc_title = title
        self.network = network
        self.date_str = date
        self.set_auto_page_break(auto=True, margin=22)
        self.add_font(FONT, "",  f"{FONT_DIR}arial.ttf")
        self.add_font(FONT, "B", f"{FONT_DIR}arialbd.ttf")
        self.add_font(FONT, "I", f"{FONT_DIR}ariali.ttf")
        self.add_font(FONT, "BI", f"{FONT_DIR}arialbi.ttf")

    def header(self):
        # Pick colour based on network
        if self.network == "o2":
            bar_color = O2_BLUE
        elif self.network == "vf":
            bar_color = VF_RED
        else:
            bar_color = DARK_BG

        # Full-width colour bar
        self.set_fill_color(*bar_color)
        self.rect(0, 0, 210, 42, "F")

        # Title
        self.set_font(FONT, "B", 20)
        self.set_text_color(*WHITE)
        self.set_xy(15, 8)
        self.cell(180, 10, self.doc_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Subtitle line with date + company
        self.set_font(FONT, "", 11)
        self.set_text_color(255, 255, 255)
        self.set_xy(15, 22)

        network_label = ""
        if self.network == "o2":
            network_label = "O2 Network"
        elif self.network == "vf":
            network_label = "Vodafone Network"
        else:
            network_label = "O2 & Vodafone"

        self.cell(180, 8, f"{COMPANY}  |  {network_label}  |  {self.date_str}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_y(48)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)
        self.set_font(FONT, "", 7)
        self.set_text_color(*GREY_TEXT)
        self.cell(90, 4, f"\u00a9 {self.date_str} {COMPANY} \u2013 {LEGAL}",
                  new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(0, 4, f"All prices exclude VAT   |   Page {self.page_no()}/{{nb}}",
                  align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def section(self, text):
        self.ln(2)
        self.set_font(FONT, "B", 13)
        self.set_text_color(*DARK_BG)
        self.cell(0, 9, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.6)
        y = self.get_y()
        self.line(15, y, 80, y)
        self.ln(4)

    def tbl_head(self, widths, headers):
        self.set_font(FONT, "B", 9)
        self.set_fill_color(*DARK_BG)
        self.set_text_color(*WHITE)
        self.set_draw_color(*DARK_BG)
        x_start = 15
        self.set_x(x_start)
        for i, (w, h) in enumerate(zip(widths, headers)):
            last = i == len(headers) - 1
            self.cell(w, 8, f"  {h}", border=1, fill=True, align="L",
                      new_x=XPos.LMARGIN if last else XPos.RIGHT,
                      new_y=YPos.NEXT if last else YPos.TOP)

    def tbl_row(self, widths, values, shade=False, bold_last=False):
        self.set_font(FONT, "", 9)
        self.set_text_color(*BLACK)
        self.set_fill_color(*(ROW_ALT if shade else WHITE))
        self.set_draw_color(*BORDER)
        x_start = 15
        self.set_x(x_start)
        for i, (w, v) in enumerate(zip(widths, values)):
            last = i == len(values) - 1
            if last and bold_last:
                self.set_font(FONT, "B", 9)
                self.set_text_color(*ACCENT)
            self.cell(w, 7, f"  {v}", border="LRB", fill=True,
                      align="L",
                      new_x=XPos.LMARGIN if last else XPos.RIGHT,
                      new_y=YPos.NEXT if last else YPos.TOP)
            if last and bold_last:
                self.set_font(FONT, "", 9)
                self.set_text_color(*BLACK)

    def info_box(self, text):
        self.ln(3)
        self.set_fill_color(240, 247, 255)
        self.set_draw_color(*ACCENT)
        self.set_font(FONT, "", 8)
        self.set_text_color(*DARK_BG)
        x = self.get_x()
        y = self.get_y()
        self.set_x(15)
        self.multi_cell(180, 5, text, border=1, fill=True)
        self.ln(2)

    def green_badge(self, text):
        self.set_font(FONT, "B", 9)
        self.set_text_color(*GREEN)
        self.cell(0, 6, f">> {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*BLACK)


# ======================================================================
# PDF 1 -- O2 Out Of Bundle Charges
# ======================================================================
def generate_o2_oob():
    pdf = CTNDoc("Out of Bundle Rates", network="o2")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Bolt-Ons
    pdf.section("O2 Bolt-Ons")
    cw = [95, 40, 45]
    pdf.tbl_head(cw, ["Bolt-On", "Allowance", "Price/mo (ex VAT)"])
    bolt_ons = [
        ("Data Top Up",           "5 GB",      "\u00a35.50"),
        ("Data Top Up",           "10 GB",     "\u00a38.00"),
        ("Data Top Up",           "20 GB",     "\u00a313.50"),
        ("Int Caller Add-On",     "\u2014",    "\u00a33.50"),
        ("Int Minutes Europe",    "500 mins",  "\u00a35.50"),
        ("Int Minutes Europe",    "1,000 mins","\u00a310.00"),
        ("Int Minutes Worldwide", "500 mins",  "\u00a330.00"),
        ("Int Minutes Worldwide", "1,000 mins","\u00a348.00"),
        ("Int SMS",               "250 texts", "\u00a36.00"),
        ("Int SMS",               "500 texts", "\u00a312.00"),
        ("Non-Geo Minutes",       "300 mins",  "\u00a33.50"),
        ("Ireland Plus",          "\u2014",    "\u00a33.50"),
        ("Roaming Mins & Data",   "250",       "\u00a360.00"),
        ("Roaming Mins & Data",   "500",       "\u00a390.00"),
        ("Roaming Mins & Data",   "1,000",     "\u00a3120.00"),
    ]
    for i, (n, a, p) in enumerate(bolt_ons):
        pdf.tbl_row(cw, [n, a, p], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # OOB Charges
    pdf.section("Out of Bundle Call Charges")
    cw2 = [110, 70]
    pdf.tbl_head(cw2, ["Charge Type", "Rate (ex VAT)"])
    oob = [
        ("UK Calls (all types)",                    "65p/min"),
        ("Voicemail",                               "65p/min"),
        ("SMS",                                     "Included in bundle"),
        ("MMS (picture/video)",                     "66p/msg"),
        ("International Calls \u2013 Europe",       "\u00a31.25/min"),
        ("International Calls \u2013 Rest of World","\u00a32.50/min"),
        ("International SMS",                       "15p/msg"),
        ("Non-Geo Access (084/087/09/118)",         "79p/min + service charge"),
        ("Freephone (0800/0808)",                   "Free"),
        ("Data (exceeding allowance)",              "2.6p/MB (\u00a326.62/GB)"),
    ]
    for i, (d, r) in enumerate(oob):
        pdf.tbl_row(cw2, [d, r], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # Roaming
    pdf.section("Roaming")
    pdf.tbl_head(cw2, ["Zone", "Daily Charge"])
    pdf.tbl_row(cw2, ["EU / EEA", "Included \u2013 no extra charge"], shade=True, bold_last=True)
    pdf.tbl_row(cw2, ["Worldwide (all other countries)", "\u00a35.00/day"], shade=False, bold_last=True)

    pdf.info_box("Roaming is only charged on days you use your phone abroad. EU roaming is included at no extra cost.\nFor a full country lookup visit: ctn-roaming-checker.pages.dev")

    pdf.output("C:/Users/key_e/Out-Of-Bundle-Charges-O2-updated.pdf")
    print("[OK] O2 OOB PDF saved")


# ======================================================================
# PDF 2 -- Vodafone Out Of Bundle Charges
# ======================================================================
def generate_vf_oob():
    pdf = CTNDoc("Out of Bundle Rates", network="vf")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Bolt-Ons
    pdf.section("Vodafone Bolt-Ons")
    cw = [95, 40, 45]
    pdf.tbl_head(cw, ["Bolt-On", "Allowance", "Price/mo (ex VAT)"])
    bolt_ons = [
        ("Data Top Up",    "5 GB",      "\u00a36.50"),
        ("Data Top Up",    "10 GB",     "\u00a39.00"),
        ("Data Top Up",    "20 GB",     "\u00a315.00"),
        ("Int Saver",      "100 mins",  "\u00a33.50"),
        ("Int Saver",      "500 mins",  "\u00a37.00"),
        ("Int World",      "100 mins",  "\u00a322.00"),
        ("Int World",      "500 mins",  "\u00a370.00"),
        ("Int World",      "1,000 mins","\u00a3140.00"),
        ("Int SMS",        "100 texts", "\u00a33.50"),
        ("Roaming Worldwide","250 MB",  "\u00a342.00"),
        ("Roaming Worldwide","500 MB",  "\u00a378.00"),
        ("Roaming Worldwide","1 GB",    "\u00a3140.00"),
    ]
    for i, (n, a, p) in enumerate(bolt_ons):
        pdf.tbl_row(cw, [n, a, p], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # OOB Charges
    pdf.section("Out of Bundle Call Charges")
    cw2 = [110, 70]
    pdf.tbl_head(cw2, ["Charge Type", "Rate (ex VAT)"])
    oob = [
        ("UK Calls (all types)",                    "65p/min"),
        ("Voicemail",                               "65p/min"),
        ("SMS",                                     "Included in bundle"),
        ("MMS (picture/video)",                     "66p/msg"),
        ("International Calls \u2013 Europe",       "\u00a31.25/min"),
        ("International Calls \u2013 Rest of World","\u00a32.50/min"),
        ("International SMS",                       "15p/msg"),
        ("Non-Geo Access (084/087/09/118)",         "79p/min + service charge"),
        ("Freephone (0800/0808)",                   "Free"),
        ("Data (exceeding allowance)",              "2.6p/MB (\u00a326.62/GB)"),
    ]
    for i, (d, r) in enumerate(oob):
        pdf.tbl_row(cw2, [d, r], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # Roaming
    pdf.section("Roaming")
    pdf.tbl_head(cw2, ["Zone", "Daily Charge"])
    pdf.tbl_row(cw2, ["EU / EEA", "Included \u2013 no extra charge"], shade=True, bold_last=True)
    pdf.tbl_row(cw2, ["Worldwide (all other countries)", "\u00a35.00/day"], shade=False, bold_last=True)

    pdf.info_box("Roaming is only charged on days you use your phone abroad. EU roaming is included at no extra cost.\nFor a full country lookup visit: ctn-roaming-checker.pages.dev")

    pdf.output("C:/Users/key_e/Vodafone-Out-Of-Bundle-Charges-Updated.pdf")
    print("[OK] Vodafone OOB PDF saved")


# ======================================================================
# PDF 3 -- Additional Charges O2
# ======================================================================
def generate_o2_additional():
    pdf = CTNDoc("Additional Charges", network="o2")
    pdf.alias_nb_pages()
    pdf.add_page()

    cw = [110, 70]

    # UK
    pdf.section("UK Calls, Data & Messaging")
    pdf.tbl_head(cw, ["Service", "Charge (ex VAT)"])
    rows = [
        ("UK Calls (exceeding allowance)",  "65p/min"),
        ("Data (exceeding allowance)",      "2.6p/MB (\u00a326.62/GB)"),
        ("MMS (picture/video)",             "66p/msg"),
        ("SMS",                             "Included in bundle"),
        ("Non-Geo Access (084/087/09/118)", "79p/min + service charge"),
        ("Freephone (0800/0808)",           "Free"),
    ]
    for i, (s, c) in enumerate(rows):
        pdf.tbl_row(cw, [s, c], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # International
    pdf.section("International Calls & Texts")
    pdf.tbl_head(cw, ["Service", "Charge (ex VAT)"])
    rows = [
        ("International Calls \u2013 Europe",       "\u00a31.25/min"),
        ("International Calls \u2013 Rest of World","\u00a32.50/min"),
        ("International SMS",                        "15p/msg"),
    ]
    for i, (s, c) in enumerate(rows):
        pdf.tbl_row(cw, [s, c], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # Roaming
    pdf.section("Roaming")
    pdf.tbl_head(cw, ["Zone", "Daily Charge"])
    pdf.tbl_row(cw, ["EU / EEA", "Included \u2013 no extra charge"], shade=True, bold_last=True)
    pdf.tbl_row(cw, ["Worldwide (all other countries)", "\u00a35.00/day"], shade=False, bold_last=True)

    pdf.green_badge("EU roaming included at no extra cost")

    pdf.info_box("The daily worldwide roaming charge only applies on days you use your phone abroad.\nFor a full country lookup visit: ctn-roaming-checker.pages.dev")

    pdf.output("C:/Users/key_e/Additional-Charges-O2.pdf")
    print("[OK] O2 Additional Charges PDF saved")


# ======================================================================
# PDF 4 -- Additional Charges Vodafone
# ======================================================================
def generate_vf_additional():
    pdf = CTNDoc("Additional Charges", network="vf")
    pdf.alias_nb_pages()
    pdf.add_page()

    cw = [110, 70]

    # UK
    pdf.section("UK Calls, Data & Messaging")
    pdf.tbl_head(cw, ["Service", "Charge (ex VAT)"])
    rows = [
        ("UK Calls (exceeding allowance)",  "65p/min"),
        ("Data (exceeding allowance)",      "2.6p/MB (\u00a326.62/GB)"),
        ("MMS (picture/video)",             "66p/msg"),
        ("SMS",                             "Included in bundle"),
        ("Non-Geo Access (084/087/09/118)", "79p/min + service charge"),
        ("Freephone (0800/0808)",           "Free"),
    ]
    for i, (s, c) in enumerate(rows):
        pdf.tbl_row(cw, [s, c], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # International
    pdf.section("International Calls & Texts")
    pdf.tbl_head(cw, ["Service", "Charge (ex VAT)"])
    rows = [
        ("International Calls \u2013 Europe",       "\u00a31.25/min"),
        ("International Calls \u2013 Rest of World","\u00a32.50/min"),
        ("International SMS",                        "15p/msg"),
    ]
    for i, (s, c) in enumerate(rows):
        pdf.tbl_row(cw, [s, c], shade=(i % 2 == 0), bold_last=True)

    pdf.ln(4)

    # Roaming
    pdf.section("Roaming")
    pdf.tbl_head(cw, ["Zone", "Daily Charge"])
    pdf.tbl_row(cw, ["EU / EEA", "Included \u2013 no extra charge"], shade=True, bold_last=True)
    pdf.tbl_row(cw, ["Worldwide (all other countries)", "\u00a35.00/day"], shade=False, bold_last=True)

    pdf.green_badge("EU roaming included at no extra cost")

    pdf.info_box("The daily worldwide roaming charge only applies on days you use your phone abroad.\nFor a full country lookup visit: ctn-roaming-checker.pages.dev")

    pdf.output("C:/Users/key_e/Additional-Charges-Vodafone.pdf")
    print("[OK] Vodafone Additional Charges PDF saved")


# ======================================================================
# PDF 5 -- Roaming Zones
# ======================================================================
def generate_roaming():
    pdf = CTNDoc("Roaming Zones & Charges", network="both")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Summary box
    pdf.section("At a Glance")
    cw = [90, 90]
    pdf.tbl_head(cw, ["Zone", "What You Pay"])
    pdf.tbl_row(cw, ["EU / EEA (30 countries)", "Included \u2013 no extra charge"], shade=True, bold_last=True)
    pdf.tbl_row(cw, ["Worldwide (all other countries)", "\u00a35.00/day (ex VAT)"], shade=False, bold_last=True)

    pdf.info_box("The daily charge only applies on days you actually use your phone abroad (calls, texts, or data). EU roaming is always included at no extra cost under fair-use policy.")

    # EU countries
    pdf.section("EU / EEA Countries \u2013 No Extra Charge")

    eu_countries = [
        "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
        "Czech Republic", "Denmark", "Estonia", "Finland", "France",
        "Germany", "Greece", "Hungary", "Iceland", "Ireland",
        "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
        "Malta", "Netherlands", "Norway", "Poland", "Portugal",
        "Romania", "Slovakia", "Slovenia", "Spain", "Sweden",
    ]

    col_w = 60
    x_start = 15
    cols = 3
    for idx, country in enumerate(eu_countries):
        col = idx % cols
        row_num = idx // cols
        x = x_start + col * col_w
        shade = row_num % 2 == 0

        pdf.set_font(FONT, "", 9)
        pdf.set_text_color(*BLACK)
        pdf.set_fill_color(*(ROW_ALT if shade else WHITE))
        pdf.set_draw_color(*BORDER)
        pdf.set_x(x)

        last_col = col == cols - 1
        pdf.cell(col_w, 6, f"  {country}", border="LRB", fill=True,
                 new_x=XPos.LMARGIN if last_col else XPos.RIGHT,
                 new_y=YPos.NEXT if last_col else YPos.TOP)

    pdf.ln(4)
    pdf.green_badge("All 30 EU/EEA countries included \u2013 use your UK allowance abroad")

    pdf.ln(4)

    # Worldwide
    pdf.section("Worldwide \u2013 \u00a35.00/day")

    pdf.set_font(FONT, "", 9)
    pdf.set_text_color(*BLACK)
    pdf.set_x(15)
    pdf.multi_cell(
        180, 5.5,
        "All countries outside the EU/EEA are covered by a flat daily rate of "
        "\u00a35.00 per day (excluding VAT). You are only charged on days when "
        "you use your device abroad.\n\n"
        "Popular destinations: USA, Canada, Australia, New Zealand, South Africa, "
        "UAE, Japan, South Korea, China, India, Brazil, Mexico, Turkey, "
        "Switzerland, and 140+ more."
    )

    pdf.ln(4)
    pdf.section("Full Country Lookup")
    pdf.set_font(FONT, "B", 10)
    pdf.set_text_color(*ACCENT)
    pdf.set_x(15)
    pdf.cell(180, 7, "ctn-roaming-checker.pages.dev",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(FONT, "", 8)
    pdf.set_text_color(*GREY_TEXT)
    pdf.set_x(15)
    pdf.cell(180, 5, "Search any country to see exact charges and recommended bolt-ons.",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output("C:/Users/key_e/Roaming-Zones-June-22.pdf")
    print("[OK] Roaming Zones PDF saved")


# ======================================================================
if __name__ == "__main__":
    generate_o2_oob()
    generate_vf_oob()
    generate_o2_additional()
    generate_vf_additional()
    generate_roaming()
    print("\nAll 5 PDFs generated successfully.")
