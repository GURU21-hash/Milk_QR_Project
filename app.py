import streamlit as st
import gspread
import qrcode

from google.oauth2.service_account import Credentials
from io import BytesIO
from datetime import datetime


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Milk Distribution System",
    page_icon="🥛",
    layout="centered"
)


# ==========================================================
# GOOGLE SHEETS CONNECTION
# ==========================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(credentials)


# IMPORTANT:
# Put your Google Sheet ID here.
#
# Example Google Sheet URL:
# https://docs.google.com/spreadsheets/d/ABC123XYZ/edit
#
# The ID is:
# ABC123XYZ

SHEET_ID = "1ABCxyz123456789"

sheet = client.open_by_key(SHEET_ID).sheet1


# ==========================================================
# GET WEBSITE URL AUTOMATICALLY
# ==========================================================

BASE_URL = st.context.url.split("?")[0].rstrip("/")


# ==========================================================
# QR CODE CREATOR
# ==========================================================

def make_qr(url):

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


# ==========================================================
# READ MILK TYPE FROM QR
# ==========================================================

milk = st.query_params.get("milk")


if milk == "1L":

    milk_type = "1 Liter"
    quantity = 1.0

elif milk == "500ml":

    milk_type = "500 ml"
    quantity = 0.5

elif milk == "250ml":

    milk_type = "250 ml"
    quantity = 0.25

else:

    milk_type = None
    quantity = 0


# ==========================================================
# HEADER
# ==========================================================

st.title("🥛 Milk Distribution System")

st.write(
    "Scan the QR code, enter your name, and record your milk."
)

st.divider()


# ==========================================================
# QR CODE LINKS
# ==========================================================

qr_1L_url = BASE_URL + "/?milk=1L"

qr_500ml_url = BASE_URL + "/?milk=500ml"

qr_250ml_url = BASE_URL + "/?milk=250ml"


# ==========================================================
# CREATE QR CODES
# ==========================================================

qr_1L = make_qr(qr_1L_url)

qr_500ml = make_qr(qr_500ml_url)

qr_250ml = make_qr(qr_250ml_url)


# ==========================================================
# QR CODE DISPLAY
# ==========================================================

st.header("📱 Milk QR Codes")

col1, col2, col3 = st.columns(3)


with col1:

    st.image(
        qr_1L,
        width=180
    )

    st.subheader("🥛 1 Liter")

    st.download_button(
        "Download QR",
        qr_1L,
        "milk_1_liter.png",
        "image/png"
    )


with col2:

    st.image(
        qr_500ml,
        width=180
    )

    st.subheader("🥛 500 ml")

    st.download_button(
        "Download QR",
        qr_500ml,
        "milk_500ml.png",
        "image/png"
    )


with col3:

    st.image(
        qr_250ml,
        width=180
    )

    st.subheader("🥛 250 ml")

    st.download_button(
        "Download QR",
        qr_250ml,
        "milk_250ml.png",
        "image/png"
    )


st.divider()


# ==========================================================
# SELECTED MILK
# ==========================================================

if milk_type:

    st.success(
        f"🥛 Selected: {milk_type}"
    )

    st.write(
        f"Quantity: **{quantity} Liter**"
    )

else:

    st.info(
        "Please scan a milk QR code."
    )


# ==========================================================
# CUSTOMER NAME
# ==========================================================

st.header("👤 Customer")

name = st.text_input(
    "Enter your name",
    placeholder="Example: Kumar"
)


# ==========================================================
# SUBMIT
# ==========================================================

if st.button(
    "✅ Record Milk",
    use_container_width=True
):

    if not milk_type:

        st.error(
            "Please scan a milk QR code first."
        )

    elif not name.strip():

        st.error(
            "Please enter your name."
        )

    else:

        now = datetime.now()

        date = now.strftime(
            "%d/%m/%Y"
        )

        time = now.strftime(
            "%I:%M:%S %p"
        )

        # Save to Google Sheet

        sheet.append_row(
            [
                date,
                time,
                name.strip(),
                milk_type,
                quantity
            ]
        )

        st.success(
            f"✅ {quantity} Liter recorded for {name.strip()}."
        )

        st.balloons()
