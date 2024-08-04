import streamlit as st

from forms.contact import contact_form


@st.dialog("Contact Me")
def show_contact_form():
    contact_form()


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_image.png", width=230)

with col2:
    st.title("Himanshu Masani", anchor=False)
    st.write(
        "FPL Admin for Fantasy Kings 2024-25"
    )
    if st.button("✉️ Contact Me"):
        show_contact_form()


# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - Over 10 years of experience playing FPL
    - Good analytical skills with regards to player selection
    - Runners Up in last season's Fantasy Kings mini-league
    """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming: Python, SQL, AWS
    - Data Visualization: PowerBi, Tableau, Plotly
    - Databases: Postgres, MongoDB, MySQL
    """
)