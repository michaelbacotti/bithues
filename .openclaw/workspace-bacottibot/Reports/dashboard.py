"""
Entity & Compliance Dashboard
Streamlit dashboard for Bacotti family business management
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Config
st.set_page_config(page_title="Bacotti Business Dashboard", layout="wide")

BASE_DIR = Path.home() / ".openclaw" / "workspace"
MEETINGS_FILE = BASE_DIR / "entity-meetings.json"

# Entity definitions
ENTITIES = {
    "bacotti-inc": {
        "name": "Bacotti Inc.",
        "ein": "86-2669759",
        "type": "NH C-Corp",
        "meetings_per_year": 14,
        "notes": "1 annual + 13 recurring meetings per year"
    },
    "dependability-holding-llc": {
        "name": "Dependability Holding, LLC",
        "ein": "86-2606053",
        "type": "WY LLC",
        "meetings_per_year": 1,
        "notes": "20% owned by Bacotti Inc."
    },
    "house-inc": {
        "name": "HOUSE Inc.",
        "ein": "87-1948148",
        "type": "501(c)(3) Nonprofit",
        "meetings_per_year": 2,
        "notes": "Las Vegas nonprofit"
    },
    "succession-holding": {
        "name": "Succession Holding, LLC",
        "ein": "N/A",
        "type": "WY LLC",
        "meetings_per_year": 1,
        "notes": "Holds Bacotti Inc. shares"
    }
}

def load_meetings():
    if MEETINGS_FILE.exists():
        with open(MEETINGS_FILE) as f:
            return json.load(f)
    return {}

def save_meetings(meetings):
    with open(MEETINGS_FILE, 'w') as f:
        json.dump(meetings, f, indent=2)

def load_notes(entity_id):
    notes_file = BASE_DIR / entity_id / "notes.md"
    if notes_file.exists():
        return notes_file.read_text()
    return ""

def save_notes(entity_id, content):
    notes_file = BASE_DIR / entity_id / "notes.md"
    notes_file.parent.mkdir(exist_ok=True)
    notes_file.write_text(content)

# Initialize session state
if 'meetings' not in st.session_state:
    st.session_state.meetings = load_meetings()

# Sidebar
st.sidebar.title("🏢 Bacotti Business")
st.sidebar.markdown("### Entities")
for entity_id, entity in ENTITIES.items():
    st.sidebar.markdown(f"**{entity['name']}**")
    st.sidebar.caption(f"{entity['type']} • EIN: {entity['ein']}")

# Main content
st.title("📊 Entity & Compliance Dashboard")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Entities", "📅 Meetings", "📝 Notes"])

with tab1:
    st.header("Family Entities")
    for entity_id, entity in ENTITIES.items():
        with st.expander(f"**{entity['name']}**", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("EIN", entity['ein'])
            with col2:
                st.metric("Type", entity['type'])
            with col3:
                st.metric("Meetings/Year", entity['meetings_per_year'])
            st.caption(entity['notes'])

with tab2:
    st.header("Meeting Tracker")
    
    # Add new meeting form
    with st.expander("➕ Add Meeting", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            entity_choice = st.selectbox("Entity", list(ENTITIES.keys()), format_func=lambda x: ENTITIES[x]['name'])
        with col2:
            meeting_date = st.date_input("Date", min_value=datetime.today())
        with col3:
            meeting_type = st.selectbox("Type", ["Annual", "Recurring", "Special"])
        
        if st.button("Add Meeting"):
            meeting_key = f"{entity_choice}_{meeting_date}"
            if meeting_key not in st.session_state.meetings:
                st.session_state.meetings[meeting_key] = {
                    "entity_id": entity_choice,
                    "date": str(meeting_date),
                    "type": meeting_type,
                    "completed": False
                }
                save_meetings(st.session_state.meetings)
                st.success("Meeting added!")
            else:
                st.warning("Meeting already exists")
    
    st.divider()
    
    # Show meetings
    st.subheader("Upcoming Meetings (Next 30 Days)")
    today = datetime.today().date()
    upcoming = []
    
    for key, meeting in st.session_state.meetings.items():
        meeting_date = datetime.strptime(meeting['date'], "%Y-%m-%d").date()
        if meeting_date >= today and meeting_date <= today + timedelta(days=30):
            upcoming.append((meeting_date, meeting))
    
    upcoming.sort(key=lambda x: x[0])
    
    if upcoming:
        for meeting_date, meeting in upcoming:
            entity = ENTITIES[meeting['entity_id']]
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    st.markdown(f"**{entity['name']}**")
                with col2:
                    st.markdown(f"📅 {meeting_date.strftime('%b %d, %Y')}")
                with col3:
                    st.markdown(f"🏷️ {meeting['type']}")
                with col4:
                    if st.checkbox("Done", meeting.get('completed', False), key=f"check_{key}"):
                        st.session_state.meetings[key]['completed'] = True
                        save_meetings(st.session_state.meetings)
                    else:
                        st.session_state.meetings[key]['completed'] = False
                        save_meetings(st.session_state.meetings)
    else:
        st.info("No meetings in the next 30 days")
    
    st.divider()
    
    # All meetings
    st.subheader("All Meetings")
    if st.session_state.meetings:
        for key, meeting in sorted(st.session_state.meetings.items(), key=lambda x: x[1]['date']):
            entity = ENTITIES[meeting['entity_id']]
            status = "✅" if meeting.get('completed') else "⏳"
            st.markdown(f"{status} **{entity['name']}** - {meeting['date']} ({meeting['type']})")
    else:
        st.info("No meetings scheduled yet")

with tab3:
    st.header("Entity Notes")
    
    selected_entity = st.selectbox("Select Entity", list(ENTITIES.keys()), format_func=lambda x: ENTITIES[x]['name'])
    
    # Load current notes
    current_notes = load_notes(selected_entity)
    
    # Editable text area
    new_notes = st.text_area("Notes", value=current_notes, height=300, 
                             placeholder="Enter notes for this entity...")
    
    if st.button("💾 Save Notes"):
        save_notes(selected_entity, new_notes)
        st.success("Notes saved!")
    
    # Show saved notes
    if current_notes:
        st.divider()
        st.subheader("Current Notes")
        st.markdown(current_notes)

# Footer
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")
