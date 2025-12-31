import streamlit as st

# python streamlit_basics.py
# streamlit run test/streamlit_basics.py

st.title("Streamlit Intro")
st.write("this is where we'll learn streamlit")

name = st.text_input("what is your name")
if name :
    st.write(f"welcome, {name}! Ready to build something amazing")

age = st.slider("your age" ,18,100)

gender = st.radio("Gender" ,('male' , 'female' , 'Gmale' ))

interst = st.selectbox('interest in ' ,('cv','ml','both'))

if st.button("profile"):
    st.write(f"name : {name}, age : {age}, gender : {gender}, interest : {interst} ")


# all_profile = []

# my_profile = {
#             "name" : {name},
#             "age" : {age},
#             "gender" : {gender},
#             "interest" : {interst} 
#             }


# if st.button("all profile"):
#     all_profile.append(my_profile)
#     st.write(all_profile)


if "profiles" not in st.session_state:
    st.session_state.profiles = []


my_profile = {"name" : name,
            "age" :age,
            "gender" : gender,
            "interest" : interst
            }

if st.button("all profile 2"):
    st.session_state.profiles.append(my_profile)
    st.write(st.session_state.profiles)