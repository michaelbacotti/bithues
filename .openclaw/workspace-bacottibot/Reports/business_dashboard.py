import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Bacotti Family Business Dashboard",
    page_icon="🏢",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("🏢 Entities")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Bacotti Inc.", "Dependability Holding", "HOUSE Inc.", "Succession Holding", "Trust"]
)

# Data
entities = {
    "Bacotti Inc.": {"ein": "86-2669759", "type": "NH C-Corp", "purpose": "Family office", "meetings": "14/year", "status": "Active"},
    "Dependability Holding, LLC": {"ein": "86-2606053", "type": "WY LLC", "purpose": "Proprietary trading company", "meetings": "1/year", "status": "Active"},
    "HOUSE Inc.": {"ein": "87-1948148", "type": "501(c)(3) Nonprofit (Nevada)", "purpose": "Drug/alcohol-free shared housing", "meetings": "2/year", "status": "Active"},
    "Succession Holding, LLC": {"ein": "N/A", "type": "WY LLC", "purpose": "Holds Bacotti Inc. shares", "meetings": "1/year", "status": "Active"},
}

family_members = [
    {"name": "Michael J. Bacotti Sr.", "dob": "05/09/1979", "role": "Chairperson, President, Executive Director"},
    {"name": "Michaella L. Bacotti", "dob": "07/09/1982", "role": "Beneficiary / Member"},
    {"name": "Michael J. Bacotti Jr.", "dob": "11/17/2010", "role": "Beneficiary"},
    {"name": "Mason A. Bacotti", "dob": "06/18/2012", "role": "Beneficiary"},
]

subsidiaries = [
    "Ashuelot Cabin, LLC (NH)",
    "Blackhawk Ranch, LLC (CO)",
    "CO City Lots, LLC (CO)",
    "Costilla Acres, LLC (CO)",
    "Eagle River Home, LLC (CO)",
    "Hawthorne Acres, LLC (CO)",
    "Sweetwater Acres, LLC (CO)",
]

# Page Content
if page == "Overview":
    st.title("🏠 Bacotti Family Business Dashboard")
    st.markdown("---")
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Entities", len(entities))
    with col2:
        st.metric("Active Entities", sum(1 for e in entities.values() if e["status"] == "Active"))
    with col3:
        st.metric("Dissolved Entities", 0)
    with col4:
        st.metric("Family Members", len(family_members))
    
    st.markdown("---")
    
    # Entity Overview Table
    st.subheader("📋 Entity Overview")
    df = pd.DataFrame([
        {"Entity": name, "EIN": data["ein"], "Type": data["type"], "Status": data["status"]}
        for name, data in entities.items()
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Meeting Requirements
    st.subheader("📅 Meeting Requirements Summary")
    meeting_data = [
        {"Entity": name, "Meetings/Year": data["meetings"]}
        for name, data in entities.items()
    ]
    st.dataframe(pd.DataFrame(meeting_data), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Family Members
    st.subheader("👨‍👩‍👧‍👦 Family Members")
    fm_df = pd.DataFrame(family_members)
    st.dataframe(fm_df, use_container_width=True, hide_index=True)

elif page == "Bacotti Inc.":
    st.title("🏢 Bacotti Inc.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("EIN", "86-2669759")
    with col2:
        st.metric("Entity Type", "NH C-Corp")
    
    st.subheader("📝 Details")
    st.write("**Purpose:** Family office")
    st.write("**Meetings:** 14/year")
    st.write("**Status:** Active")
    
    st.markdown("---")
    st.subheader("📂 References")
    st.info("Link to references would go here")

elif page == "Dependability Holding":
    st.title("📈 Dependability Holding, LLC")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("EIN", "86-2606053")
    with col2:
        st.metric("Entity Type", "WY LLC")
    
    st.subheader("📝 Details")
    st.write("**Purpose:** Proprietary trading company")
    st.write("**Ownership:** 20% owned by Bacotti Inc.")
    st.write("**GP Fee:** $1,000/month")
    st.write("**Profit Share:** 20%")
    st.write("**Meetings:** 1/year")
    st.write("**Status:** Active")
    
    st.markdown("---")
    st.subheader("💰 P/L Tracker")
    st.info("Link to P/L tracker would go here")

elif page == "HOUSE Inc.":
    st.title("🏠 HOUSE Inc.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("EIN", "87-1948148")
    with col2:
        st.metric("Entity Type", "501(c)(3) Nonprofit (Nevada)")
    
    st.subheader("📍 Address")
    st.write("3225 McLeod Dr, Suite 100")
    st.write("Las Vegas, NV 89121")
    
    st.subheader("📞 Contact")
    st.write("Phone: 702-871-8535")
    
    st.subheader("📝 Details")
    st.write("**Purpose:** Drug/alcohol-free shared housing")
    st.write("**Meetings:** 2/year")
    st.write("**Status:** Active")
    
    st.markdown("---")
    
    st.subheader("👔 Leadership")
    st.write("**Michael Sr.** - Chairperson, President, Executive Director")

elif page == "Succession Holding":
    st.title("🔄 Succession Holding, LLC")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Entity Type", "WY LLC")
    with col2:
        st.metric("Status", "Active")
    
    st.subheader("📝 Details")
    st.write("**Purpose:** Holds Bacotti Inc. shares")
    st.write("**Meetings:** 1/year")
    
    st.markdown("---")
    
    st.subheader("🏔️ Subsidiaries (7)")
    for sub in subsidiaries:
        st.write(f"• {sub}")

elif page == "Trust":
    st.title("🔐 Bacotti Family Trust")
    st.markdown("---")
    
    st.subheader("📝 Trust Details")
    st.write("**Name:** Bacotti Family Trust")
    st.write("**Status:** Active")
    
    st.markdown("---")
    
    st.subheader("👥 Beneficiaries")
    for member in family_members:
        st.write(f"• {member['name']} - {member['role']}")