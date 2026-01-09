from course_scraper import scrape_courses
import streamlit as st

url = "https://ucalendar.uwaterloo.ca/2324/COURSE/course-CS.html"
courses = scrape_courses(url)

# print(f"Total extracted: {len(courses)}")
# print(courses)

firstyear = []
secondyear = []
thirdyear = []
fourthyear = []

for c in courses:
    try:
        if c["code"][3] == "1":
            firstyear.append(c)
        elif c["code"][3] == "2":
            secondyear.append(c)
        elif c["code"][3] == "3":
            thirdyear.append(c)
        elif c["code"][3] == "4":
            fourthyear.append(c)
    except:
        pass


if "first_term" not in st.session_state:
    st.session_state.first_term = []
if "second_term" not in st.session_state:
    st.session_state.second_term = []
if "show_year" not in st.session_state:
    st.session_state.show_year = None
if "termAdding" not in st.session_state:
    st.session_state.termAdding = False
if "selected_year" not in st.session_state:
    st.session_state.selected_year = "First Year"



st.header("Course Terms")
col1, col2 = st.columns(2)
with col1:
    st.subheader("First Term Courses")
    for c in st.session_state.first_term:
        ratio = st.columns([6,2])
        with ratio[0]:
            st.write(f"{c['code']}-{c['title']}")
        with ratio[1]:
            removebutton = st.button("X" , key = f"rm1-{c['code']}")
            if removebutton:
                st.session_state.first_term.remove(c)
                st.rerun()



with col2:
    st.subheader("Second Term Courses")
    for c in st.session_state.second_term:
        ratio = st.columns([6,2])
        with ratio[0]:
            st.write(f"{c['code']}-{c['title']}")
        with ratio[1]:
            removebutton = st.button("X", key = f"rm2-{c['code']}")
            if removebutton:
                st.session_state.second_term.remove(c)
                st.rerun()

st.divider()

year = st.selectbox("Select Year", ["First Year", "Second Year", "Third Year", "Fourth Year"],key = "selected_year")

st.title("Waterloo Course Selector")
st.write("Helps you manage what course to take in your first and second term")
st.divider()

submit = st.button("Get List Of Courses")
#
if submit:
    st.session_state.termAdding = True
    st.session_state.show_year = st.session_state.selected_year

if st.session_state.termAdding == True:
    currentyear = []

    if st.session_state.show_year == "First Year":
        currentyear = firstyear
    elif st.session_state.show_year == "Second Year":
        currentyear = secondyear
    elif st.session_state.show_year == "Third Year":
        currentyear = thirdyear
    elif st.session_state.show_year == "Fourth Year":
        currentyear = fourthyear



    for c in currentyear:
        st.header(c["code"])
        st.subheader(c["title"])
        try:
            st.write(c["description"])
        except:
            st.write("No description available")
        bt1 = st.button("Add to Term 1", key=f"t1-{c['code']}")
        bt2 = st.button("Add to Term 2", key=f"t2-{c['code']}")

        if bt1:
            lengthofterm = len(st.session_state.first_term)
            if lengthofterm == 5:
                st.error("Sorry you cannot add anymore courses")
            else:
                if c not in st.session_state.first_term:
                    st.session_state.first_term.append(c)
                if c in st.session_state.second_term:
                    st.session_state.second_term.remove(c)
                st.rerun()

        if bt2:
            lengthofterm = len(st.session_state.second_term)
            if lengthofterm == 5:
                st.error("Sorry you cannot add anymore courses")
            else:
                if c not in st.session_state.second_term:
                    st.session_state.second_term.append(c)
                if c in st.session_state.first_term:
                    st.session_state.first_term.remove(c)
                st.rerun()

        st.divider()

