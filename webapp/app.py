import streamlit as st 

def main():
    if st.button("Click me"): 
        st.write("Hello World")
        state = 0
        if state == 1: 
            state = 0
            st.write(state)
        else: 
            state = 1
            st.write(state)

if __name__ == "__main__":
    main()
