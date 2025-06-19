import streamlit as st
import pandas as pd
import altair as alt # Using altair for potentially nicer looking charts, though st.bar_chart is simpler.

# --- Page Configuration ---
st.set_page_config(
    page_title="Library Knowledge Management Expert System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Hardcoded Data for Resources (for search results) ---
# Added 'Status' and 'Format' columns as requested
resources_data = [
    {"ID": "R001", "Title": "Artificial Intelligence Basics", "Author": "J. Doe", "Subject": "Artificial Intelligence", "Type": "E-book", "Language": "English", "Click Count": 150, "Annual Loan Count": 75, "Status": "available", "Format": "PDF"},
    {"ID": "R002", "Title": "Climate Change Impacts", "Author": "A. Smith", "Subject": "Environmental Science", "Type": "Journal Article", "Language": "English", "Click Count": 90, "Annual Loan Count": 40, "Status": "available", "Format": "EPUB"},
    {"ID": "R003", "Title": "Python Programming Guide", "Author": "B. Gates", "Subject": "Computer Science", "Type": "E-book", "Language": "English", "Click Count": 210, "Annual Loan Count": 110, "Status": "on-loan", "Format": "PDF"},
    {"ID": "R004", "Title": "Sejarah Malaysia", "Author": "C. Lim", "Subject": "History", "Type": "Physical Book", "Language": "Malay", "Click Count": 50, "Annual Loan Count": 20, "Status": "available", "Format": "Hardcover"},
    {"ID": "R005", "Title": "Ethical AI Development", "Author": "L. Brown", "Subject": "Artificial Intelligence", "Type": "Journal Article", "Language": "English", "Click Count": 120, "Annual Loan Count": 60, "Status": "restrictedForLoan", "Format": "PDF"},
    {"ID": "R006", "Title": "Machine Learning in Practice", "Author": "S. Gupta", "Subject": "Computer Science", "Type": "E-book", "Language": "English", "Click Count": 250, "Annual Loan Count": 130, "Status": "available", "Format": "EPUB"},
    {"ID": "R007", "Title": "Geological Formations", "Author": "K. Lee", "Subject": "Geology", "Type": "Physical Book", "Language": "English", "Click Count": 40, "Annual Loan Count": 15, "Status": "available", "Format": "Hardcover"},
    {"ID": "R008", "Title": "Advanced Calculus", "Author": "M. Chen", "Subject": "Mathematics", "Type": "E-book", "Language": "English", "Click Count": 180, "Annual Loan Count": 90, "Status": "on-loan", "Format": "PDF"},
    {"ID": "R009", "Title": "Basic Malay Phrases", "Author": "R. Singh", "Subject": "Language", "Type": "Audio", "Language": "Malay", "Click Count": 70, "Annual Loan Count": 30, "Status": "available", "Format": "MP3"},
    {"ID": "R010", "Title": "The Future of Quantum Computing", "Author": "Z. Ahmed", "Subject": "Physics", "Type": "Journal Article", "Language": "English", "Click Count": 160, "Annual Loan Count": 85, "Status": "restrictedForLoan", "Format": "PDF"},
]
df_resources = pd.DataFrame(resources_data)

# --- Hardcoded Filter Options ---
keywords_options = ["Artificial Intelligence", "Environmental Science", "Computer Science", "History", "Ethics", "Geology", "Mathematics", "Language", "Physics"]
resource_type_options = ["All", "E-book", "Journal Article", "Physical Book", "Video", "Audio"]
language_options = ["All", "English", "Malay", "Chinese", "Tamil"]

# --- Main Page Layout ---
st.title("Library Knowledge Management Expert System")

st.markdown("---")

# --- User Role Selection ---
user_role = st.radio(
    "Select Your Role:",
    ("Student", "Librarian"),
    horizontal=True,
    key="role_selector"
)

st.markdown("---")

# --- Dynamic Content Based on Role ---
col1, col2 = st.columns([1, 2]) # Left and Right panels

# --- Student Case ---
if user_role == "Student":
    with col1: # Left Panel for Student Details (Undergraduate/Postgraduate)
        st.header("My Student Details")
        student_type = st.radio(
            "Select Student Type:",
            ("Undergraduate Student", "Postgraduate Student"),
            key="student_type"
        )
        st.subheader("Borrowing Rules:")
        if student_type == "Undergraduate Student":
            st.markdown(
                """
                **Rule:**
                `IF user role is STUDENT`
                `AND is UNDERGRADUATE STUDENT`
                `THEN the loan resource duration is up to 7 days.`
                """
            )
        elif student_type == "Postgraduate Student":
            st.markdown(
                """
                **Rule:**
                `IF user role is STUDENT`
                `AND is POSTGRADUATE STUDENT`
                `THEN the loan resource duration is up to 10 days.`
                """
            )

    with col2: # Right Panel for Student Permissions & Search
        st.header("The Permissions & Rules")
        st.markdown(
            """
            **Permission:** `SEARCH`
            **Rule:**
            `IF user role is STUDENT`
            `THEN has the permission to SEARCH.`
            """
        )

        st.subheader("Search Resources")
        selected_keyword = st.selectbox("Select Keyword:", ["All"] + keywords_options, key="student_keyword")
        selected_resource_type = st.selectbox("Select Resource Type:", resource_type_options, key="student_resource_type")
        selected_language = st.selectbox("Select Language:", language_options, key="student_language")

        search_button = st.button("Search", key="student_search_button")

        if search_button:
            st.subheader("Search Results:")
            filtered_df = df_resources.copy()
            if selected_keyword != "All":
                filtered_df = filtered_df[filtered_df['Subject'].str.contains(selected_keyword, case=False, na=False)]
            if selected_resource_type != "All":
                filtered_df = filtered_df[filtered_df['Type'] == selected_resource_type]
            if selected_language != "All":
                filtered_df = filtered_df[filtered_df['Language'] == selected_language]

            if not filtered_df.empty:
                # Add 'Status' and 'Format' to student search results display
                st.dataframe(filtered_df[['Title', 'Author', 'Subject', 'Type', 'Language', 'Status', 'Format']])
            else:
                st.info("No resources found matching your criteria.")

# --- Librarian Case ---
elif user_role == "Librarian":
    with col1: # Left Panel for Librarian Tools
        st.header("Librarian Tools & Actions")
        
        # Buttons to navigate the Right Panel content
        action = st.radio(
            "Select an Action:",
            ("Upload Resource", "Update Resource", "Delete Resource", "Advanced Search"),
            key="librarian_action"
        )
        st.markdown(
            """
            **Rule:**
            `IF user role is LIBRARIAN`
            `THEN you can Search, Advanced View, Update, Delete and Upload.`
            """
        )
        st.markdown("---") # Separator between general and specific actions
        
        # --- Display type-specific rules ---
        st.subheader("Librarian Type-Specific Rules:")
        # --- Librarian Type Selection ---
        librarian_type = st.radio(
            "Select Librarian Type:",
            ("CollectionManagementLibrarian", "CirculationManagementLibrarian", "SystemLibrarian"),
            key="librarian_type_selector"
        )
        if librarian_type == "CollectionManagementLibrarian":
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND librarian type is CollectionManagementLibrarian`
                `THEN you are authorized to select and acquire new materials`
                """
            )
            st.markdown(
                """
                **Recommend:**
                Select and acquire new materials [weekly task]
                """
            )
            st.markdown(
                '<ul>'
                    '<li>Review users request (through Click Count or Annual Loan Count)</li>'
                    '<li>Identify academic requirements</li>'
                    '<li>Keep up-to-todate with new releases from various publishers</li>'
                '</ul>'
                , unsafe_allow_html=True)
        elif librarian_type == "CirculationManagementLibrarian":
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND librarian type is CirculationManagementLibrarian`
                `THEN you must manage the LoanRule.`
                """
            )
            st.markdown(
                """
                **Recommend:**
                """
            )
            st.markdown(
                '<ul>'
                    '<li>Loan Rule [look at Student role panel]</li>'
                    '<li>Shelf Management & Reshelving</li>'
                    '<li>Category damage [MINOR_DAMAGE - repair || MAJOR DAMAGE - withdraw or replacement]</li>'
                '</ul>'
                , unsafe_allow_html=True)
        elif librarian_type == "SystemLibrarian":
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND librarian type is SystemLibrarian`
                `THEN you must manage the ResourceManagementRule AND RecommendationRule.`
                """
            )
            st.markdown(
                """
                **Recommend:**
                """
            )
            st.markdown(
                '<ul>'
                    '<li>Manage user permissions [keep confidential information from public]</li>'
                    '<li>Hardware maintainance</li>'
                    '<li>Web system review [daily]</li>'
                '</ul>'
                , unsafe_allow_html=True)

    with col2: # Right Panel for Librarian Permissions & Rules
        st.header("The Permissions & Rules")

        if action == "Upload Resource":
            st.subheader("UPLOAD Permission Rules:")
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND permission is UPLOAD`
                `THEN you must ensure all necessary copyright permissions or licenses are secured and documented`
                `AND must input all mandatory metadata fields.`
                """
            )
            st.markdown(
                """
                **Upload Rules:**\n
                Please check the **copyright permission and licenses** are available before you upload a new resource.\n
                The metadata that needed for uploading a resource:
                """
            )
            st.markdown('<ul><li>Title</li><li>Resources Type</li><li>Keywords</li></ul>', unsafe_allow_html=True)
            st.subheader("Upload New Resource")
            with st.form("upload_form"):
                uploaded_file = st.file_uploader("Choose a file to upload", type=['pdf', 'docx', 'txt'])
                title = st.text_input("Title (Mandatory):")
                author = st.text_input("Author (Mandatory):")
                subject = st.text_input("Subject Tags (e.g., 'AI, Computer Science') (Mandatory):")
                license_info = st.text_area("Copyright/License Information:")
                # Add Status and Format selection for upload
                status_options = ['available', 'on-loan', 'restrictedForLoan']
                format_options = ['PDF', 'EPUB', 'Hardcover', 'Softcover', 'MP3', 'MP4']
                selected_status = st.selectbox("Status:", status_options, key="upload_status")
                selected_format = st.selectbox("Format:", format_options, key="upload_format")

                submitted = st.form_submit_button("Submit Upload")
                if submitted:
                    if uploaded_file and title and author and subject:
                        # In a real system, you'd add the new resource to df_resources
                        st.success(f"Resource '{title}' uploaded successfully. (Prototype action only)")
                        st.info("Verification of copyright and mandatory metadata input enforced by this rule.")
                    else:
                        st.error("Please fill in all mandatory fields and select a file.")

        elif action == "Update Resource":
            st.subheader("UPDATE Permission Rules:")
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND permission is UPDATE`
                `THEN you must verify the updated information against authoritative sources.`
                """
            )
            st.markdown(
                """
                **Update Rules:**\n
                Please confirm the **authoritative** changes before update 
                """
            )
            st.subheader("Find Resource to Update")
            update_search_query = st.text_input("Search by Title or ID to Update:", key="update_search")
            if st.button("Find Resource", key="find_update_button"):
                found_resources = df_resources[
                    df_resources['Title'].str.contains(update_search_query, case=False, na=False) |
                    df_resources['ID'].str.contains(update_search_query, case=False, na=False)
                ]
                if not found_resources.empty:
                    # Add 'Status' and 'Format' to librarian update search results display
                    st.dataframe(found_resources[['ID', 'Title', 'Author', 'Subject', 'Status', 'Format']])
                    st.info("In a real system, you'd select an item here to open an update form.")
                else:
                    st.info("No resources found for update.")

        elif action == "Delete Resource":
            st.subheader("DELETE Permission Rules:")
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND permission is DELETE`
                `THEN you must verify that the resource is not currently on loan, in process or required for current academic programs.`
                """
            )
            st.markdown(
                """
                **Checklist** before you delete: \n
                """
            )
            st.markdown(
                "<ul><li>Is the resource still on loan?</li><li>Is the resource still in use for current academic programs?</li></ul>",
                unsafe_allow_html= True
            )
            st.subheader("Find Resource to Delete")
            delete_search_query = st.text_input("Search by Title or ID to Delete:", key="delete_search")
            if st.button("Find Resource", key="find_delete_button"):
                found_resources = df_resources[
                    df_resources['Title'].str.contains(delete_search_query, case=False, na=False) |
                    df_resources['ID'].str.contains(delete_search_query, case=False, na=False)
                ]
                if not found_resources.empty:
                    # Add 'Status' and 'Format' to librarian delete search results display
                    st.dataframe(found_resources[['ID', 'Title', 'Author', 'Subject', 'Status', 'Format']])
                    st.warning("In a real system, a delete button with confirmation would appear here.")
                    st.info("Verification of loan status and academic need enforced by this rule.")
                else:
                    st.info("No resources found for deletion.")

        elif action == "Advanced Search":
            st.subheader("ADVANCED SEARCH Permission Rules:")
            st.markdown(
                """
                **Rule:**
                `IF user role is LIBRARIAN`
                `AND permission is ADVANCED SEARCH`
                `THEN you can discover available resources within the library’s collection`
                `AND view the Click Count of a resource.`
                `AND view the Annual Loan Count of a resource.`
                """
            )
            st.markdown(
                """
                **SEARCH** the resource to know the Click Count, the Annual Loan Count and where the resource placed.
                """
            )
            st.subheader("Advanced Search Resources")
            adv_search_query = st.text_input("Enter keywords for Advanced Search:", key="adv_search_query")
            adv_selected_resource_type = st.selectbox("Select Resource Type:", resource_type_options, key="adv_resource_type")
            adv_selected_language = st.selectbox("Select Language:", language_options, key="adv_language")

            adv_search_button = st.button("Perform Advanced Search", key="adv_search_button")

            if adv_search_button:
                st.subheader("Advanced Search Results (with Admin Metrics):")
                filtered_df_adv = df_resources.copy()
                if adv_search_query: # Simple keyword search on Title/Subject for demo
                    filtered_df_adv = filtered_df_adv[
                        filtered_df_adv['Title'].str.contains(adv_search_query, case=False, na=False) |
                        filtered_df_adv['Subject'].str.contains(adv_search_query, case=False, na=False)
                    ]
                if adv_selected_resource_type != "All":
                    filtered_df_adv = filtered_df_adv[filtered_df_adv['Type'] == adv_selected_resource_type]
                if adv_selected_language != "All":
                    filtered_df_adv = filtered_df_adv[filtered_df_adv['Language'] == adv_selected_language]

                if not filtered_df_adv.empty:
                    # Displaying Click Count and Annual Loan Count, Status, and Format
                    st.dataframe(filtered_df_adv[['Title', 'Author', 'Subject', 'Type', 'Language', 'Status', 'Format', 'Click Count', 'Annual Loan Count']])
                else:
                    st.info("No resources found matching your advanced criteria.")

                # --- Graphs for Librarians (Below Advanced Search Results) ---
                st.markdown("---")
                st.subheader("Top Resources by Usage Metrics (Overall Collection)")

                # Top 3 by Click Count
            top_3_clicks = df_resources.nlargest(3, 'Click Count')
            st.write("**Top 3 Resources by Click Count**")
            # Using Altair for potentially better visualization, though st.bar_chart is simpler
            chart_clicks = alt.Chart(top_3_clicks).mark_bar().encode(
                x=alt.X('Title', sort='-y'),
                y='Click Count',
                tooltip=['Title', 'Click Count']
            ).properties(height=300)
            st.altair_chart(chart_clicks, use_container_width=True)


            # Top 3 by Annual Loan Count
            top_3_loans = df_resources.nlargest(3, 'Annual Loan Count')
            st.write("**Top 3 Resources by Annual Loan Count**")
            chart_loans = alt.Chart(top_3_loans).mark_bar().encode(
                x=alt.X('Title', sort='-y'),
                y='Annual Loan Count',
                tooltip=['Title', 'Annual Loan Count']
            ).properties(height=300)
            st.altair_chart(chart_loans, use_container_width=True)