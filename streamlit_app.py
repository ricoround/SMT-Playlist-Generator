import streamlit as st

# Variable to control the navigation
page = st.session_state.get("page", 1)

# Landing page
def landing_page():
    st.title("Welcome to Running Recommender")
    st.write("Generate a personalized running playlist for optimal running performance.")
    st.image("running.jpeg", width=400)
    
    # Go to the next page when the button is clicked
    if st.button("Get Started"):
        st.session_state.page = 2

# User input page
def user_input_page():
    st.title("Tell us about yourself")
    
    # Create a form for user inputs
    with st.form("user_info_form"):
        running_experience = st.radio("How much running experience do you have?", ["Beginner", "Advanced"], captions = ["Don't really run regularly", "Run quite frequently"])
        options = st.multiselect("What are your favourite genres? (multiple genres possible)", ["Pop", "Rock", "Electronic/Dance", "Hip-Hop/Rap", "Indie", "Alternative", "Country", "Jazz", "Classical", "Reggae", "Latin", "R&B/Soul", "Metal", "Blues", "Folk", "Punk", "K-Pop", "Ambient", "Trance"])
        warming_up_time = st.slider('How many minutes would you like your warming up to be?', 0, 30, 10)
        workout_time = st.slider('How many minutes would you like your workout to be?', 0, 120, 25)
        cooldown_time = st.slider('How many minutes would you like your cooldown to be?', 0, 30, 5)
        workout_pace = st.slider('What pace (min/km) do you want you workout to be?', 2.0, 10.0, 5.5)

        # When the form is submitted
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.page = 3

def generated_playlist_page():
    st.title("Generated playlist")
    st.write("Your playlist has been generated")

# Show the appropriate page based on user interaction
if page == 1:
    landing_page()
elif page == 2:
    user_input_page()
elif page == 3:
    generated_playlist_page()