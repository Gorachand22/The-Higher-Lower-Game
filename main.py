import streamlit as st
from numpy.random import choice
from db import data

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0 
if 'H' not in st.session_state or 'L' not in st.session_state:
    st.session_state.H = None
    st.session_state.L = None

def compare(choice1, choice2):
    """
    Compares two choices based on their follower count and returns the choice with the higher follower count.
    Parameters:
        choice1 (dict): The first choice to compare.
        choice2 (dict): The second choice to compare.
    Returns:
        dict: The choice with the higher follower count.
    """
    if choice1['follower_count'] > choice2['follower_count']:
        return choice1
    else:
        return choice2

def starting_game():
    """
    Initializes the game by randomly selecting two elements from the given data and assigning them to the high and low elements of the session state.
    Parameters:
        None
    Returns:
        None
    """
    if st.session_state.H is None or st.session_state.L is None:
        # Initial random selection
        A = choice(data, 2, replace=False)
        st.session_state.H = A[0].copy()
        st.session_state.L = A[1].copy()

def game():
    """
    This function represents a Higher Lower game.
    
    It displays a welcome message and the game logo.
    
    It sets up three columns using the st.columns() function.
    
    In the first column, it displays the details of the higher option, including name, description, and country.
    
    In the second column, it displays a VS image.
    
    In the third column, it displays the details of the lower option, including name, description, and country.
    
    If the lower option is the same as the higher option, it selects a new lower option from the data.
    
    It prompts the user to choose between 'Higher' or 'Lower'.
    
    If the user clicks the 'Play' button, it compares the chosen option with the correct option.
    
    If the user's choice matches the correct option, it updates the score, swaps the positions for the next round, displays a success message, waits for 2 seconds, clears the success message, and refreshes the page.
    
    If the user's choice does not match the correct option, it displays an error message and shows the current score.
    """
    st.write("Welcome To Higher Lower Game")
    st.image('images/logo.png', width= 300)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write(f"Higher: name- {st.session_state.H['name']}, description- {st.session_state.H['description']}, country- {st.session_state.H['country']}")
        st.image(st.session_state.H['image'],width= 150)
    with col2:
        st.image('images/VS.png',width=100)
    with col3:
        st.write(f"Lower: name- {st.session_state.L['name']}, description- {st.session_state.L['description']}, country- {st.session_state.L['country']}")
        st.image(st.session_state.L['image'],width= 150)

    if st.session_state.L == st.session_state.H:
        st.session_state.L = choice(data, 1, replace=False)[0].copy()
        
    ask = st.radio("Choose Your Choice:", options=['Higher', 'Lower'])
    submit_button = st.button("Play")
    
    if submit_button:
        get = compare(st.session_state.H, st.session_state.L)
        if (ask == 'Higher' and get['name'] == st.session_state.H['name']) or \
           (ask == 'Lower' and get['name'] == st.session_state.L['name']):
            
            # Create an empty placeholder for the success message
            success_placeholder = st.empty()
            
            st.session_state.score += 1
            # Swap the positions for the next round
            st.session_state.L, st.session_state.H = choice(data, 1, replace=False)[0], st.session_state.L
            success_placeholder.success("You are correct")
            
            # Use time.sleep to keep the success message for a specific duration (e.g., 2 seconds)
            import time
            time.sleep(2)
            
            # Clear the success message and refresh the page
            success_placeholder.empty()
            st.experimental_rerun()

        else:
            st.error("You are wrong")
            st.warning(f"Your score is {st.session_state.score}")

# Main Streamlit app
st.title("🔼Higher Lower Game🔽")

# Add instructions in the sidebar
st.sidebar.header("Instructions")
st.sidebar.markdown("Welcome to the Higher Lower Game!")
st.sidebar.markdown("Your goal is to guess which of two options has more instagram followers.")
st.sidebar.markdown("Follow these steps to play:")
st.sidebar.markdown("1. Choose 'Higher' or 'Lower' based on your guess.")
st.sidebar.markdown("2. Click the 'Play' button to submit your guess.")
st.sidebar.markdown("3. If your guess is correct, the success message will appear.")
st.sidebar.markdown("4. The positions will be swapped, and a new round will begin.")
st.sidebar.markdown("5. Keep playing and try to maximize your score!")

def play():
    """
    Executes the play function.

    This function is responsible for starting and running the game. It calls the starting_game function to initialize the game and then proceeds to the main game loop by calling the game function.

    Parameters:
    None

    Returns:
    None
    """
    starting_game()
    game()

play()
