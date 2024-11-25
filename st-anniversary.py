# ./st-anniversary.py

# Third-party imports
import os
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Local application imports

st.set_page_config(
    page_title="Anniversary Calculator",
    page_icon=":material/celebration:",
    layout="wide",
    )

DEFAULT_ANNIVERSARY_TYPES = ["1 Year", "5 Years", "10 Years", "15 Years", "25 Years", "30 Years", "40 Years", "50 Years"]

def filter_anniversaries(df, calc_date, anniversary_types):
    """
    Filter anniversaries based on calculation date and anniversary types.
    Returns DataFrame of matching anniversaries.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    if isinstance(calc_date, str):
        calc_date = pd.to_datetime(calc_date)
    
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    
    anniversary_years = {int(ann.split()[0]): ann for ann in anniversary_types}
    results = []

    for _, row in df.iterrows():
        name = row['Name']
        start_date = pd.to_datetime(row['Start Date'])
        
        for years, ann_type in anniversary_years.items():
            # Calculate the anniversary date for this year interval
            try:
                # First find the target year for the anniversary
                target_year = start_date.year + years
                
                # Create the anniversary date using the same month and day
                anniversary_date = datetime(
                    year=target_year,
                    month=start_date.month,
                    day=start_date.day
                )
                
                # Check if this anniversary falls in our target month/year
                if (anniversary_date.month == calc_date.month and 
                    anniversary_date.year == calc_date.year):
                    results.append({
                        'name': name,
                        'anniversary_date': anniversary_date.date(),
                        'anniversary_type': ann_type,
                        'years': years
                    })
            except ValueError as e:
                st.error(f"Error calculating anniversary for {name}: {str(e)}")
                continue

    return pd.DataFrame(results)

def update_calc_date(new_date):
    """
    Update the calculation date and rerun the app to ensure UI synchronization
    """
    st.session_state.calc_date = new_date
    # Force a rerun to update all UI elements
    st.rerun()

# Initialize session state
if "people" not in st.session_state:
    st.session_state.people = {}
if "anniversary_types" not in st.session_state:
    st.session_state.anniversary_types = DEFAULT_ANNIVERSARY_TYPES
if "calc_date" not in st.session_state:
    st.session_state.calc_date = datetime.now().replace(day=1)
if "displayed_anniversaries" not in st.session_state:
    st.session_state.displayed_anniversaries = {}

st.title(":material/celebration: Anniversary Calculator")
st.header("Easily calculate people's anniversaries!")

anniversary_types = st.multiselect(
    "Select anniversary types:",
    options=DEFAULT_ANNIVERSARY_TYPES,
    default=st.session_state.anniversary_types
)

with st.container(key="main"):
    left_main, right_main = st.columns([2, 1])

    with right_main:
        st.subheader("Add people here:")
        with st.form("Add Date", border=True, clear_on_submit=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                name = st.text_input(":material/person_add: Name*", placeholder="Name")
            with col2: 
                start_date = st.date_input(":material/event: Start Date*", datetime.now())
                
            if st.form_submit_button("Add", type="primary", icon=":material/add:", use_container_width=True):
                if not name:
                    st.error("Name is required")
                elif not start_date:
                    st.error("Start Date is required")
                if st.session_state.people is None:
                    st.session_state.people = {}
                start_date_iso = start_date.isoformat()
                st.session_state.people[name] = {"start_date": start_date_iso}
                st.success(f"Added {name} with a start date of {start_date_iso}")

        with st.container(key="uploader", border=True):
            uploaded_file = st.file_uploader("Choose a file", type=["csv"])
            if uploaded_file is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_file)
                    for _, row in uploaded_df.iterrows():
                        st.session_state.people[row['Name']] = {
                            "start_date": pd.to_datetime(row['Start Date']).isoformat()
                        }
                    st.success(f"Uploaded {len(uploaded_df)} anniversaries")
                except Exception as e:
                    st.exception(f"An error occurred: {e}")
    
    with left_main:
        with st.container(key="anniversaries"):
            display_month = st.session_state.calc_date.strftime('%B %Y')
            st.subheader(f"Showing anniversaries for: {display_month}")
            with st.container(key="anniversary_calendar", border=True):

                col3, col3_5, col4, col4_5, col5 = st.columns([2, 1, 2, 1, 2])
                with col3:
                    if st.button("Prev. Month", icon=":material/arrow_back:", use_container_width=True):
                        new_date = st.session_state.calc_date = (
                            st.session_state.calc_date - relativedelta(months=1)
                        ).replace(day=1)
                        update_calc_date(new_date)
                with col4:
                    if st.button("Current Month", icon=":material/today:", use_container_width=True):
                        new_date = st.session_state.calc_date = datetime.now().replace(day=1)
                        update_calc_date(new_date)
                with col5:
                    if st.button("Next Month", icon=":material/arrow_forward:", use_container_width=True):
                        new_date = st.session_state.calc_date = (
                            st.session_state.calc_date + relativedelta(months=1)
                        ).replace(day=1)
                        update_calc_date(new_date)

                # Create DataFrame from people in session state
                if st.session_state.people:
                    people_df = pd.DataFrame(
                        data=[(name, data['start_date']) for name, data in st.session_state.people.items()],
                        columns=["Name", "Start Date"]
                    )
                    
                    # Filter anniversaries for current calculation date
                    filtered_anniversaries = filter_anniversaries(
                        people_df,
                        st.session_state.calc_date,
                        st.session_state.anniversary_types
                    )

                    st.session_state.displayed_anniversaries = filtered_anniversaries.to_dict(orient="records")

                    if not filtered_anniversaries.empty:
                        column_config = {
                            "name": "Name",
                            "anniversary_date": st.column_config.DateColumn("Anniversary Date", format="MMMM DD, YYYY"),
                            "anniversary_type": "Anniversary Type",
                            "years": st.column_config.NumberColumn(
                                "Years",
                                help="Number of years for this anniversary"
                            )
                        }
                        st.dataframe(
                            filtered_anniversaries,
                            use_container_width=True,
                            hide_index=True,
                            column_config=column_config
                        )
                        st.balloons()
                    else:
                        st.info("No anniversaries this month.")
                else:
                    st.warning("No people added. Add a person above or upload a CSV file.")

with st.expander(expanded=False, label="People"):
    if st.session_state.people:
        people_df = pd.DataFrame(
            data=[(name, data['start_date']) for name, data in st.session_state.people.items()],
            columns=["Name", "Start Date"]
        )
        st.dataframe(people_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No people added. Add a person above or upload a CSV file.")

with st.expander(label="Debug"):
    st.json(st.session_state)
