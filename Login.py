import streamlit as st
import hashlib
from pymongo import MongoClient
import pymongo

import glossary
import home
import myPortfolio
import portfolio
import prediction


def app():
    client = MongoClient(
        'mongodb+srv://dbShreya:vuh42u4cNDnSlmFm@cluster0.gttk9.mongodb.net/Cluster0?retryWrites=true&w=majority')

    db = client.userData

    people = db.people

    def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_hashes(password, hashed_text):
        if make_hashes(password) == hashed_text:
            return hashed_text
        return False

    def add_userdata(username, password, email):
        people.create_index([('Email', pymongo.DESCENDING)], unique=True)
        people.insert_one({'Username': username, 'Password': password, 'Email': email})

    def login_user(username, password, email):
        myquery = {"Username": username, "Password": password, 'Email': email}
        data = people.find_one(myquery)
        return data


    menu = ["Login", "SignUp"]
    #a, b = st.beta_columns(2)

    choice = st.radio("Login or Create a New Account", menu)

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
        st.subheader("Login Section")

        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')


        if st.checkbox("Login"):
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd), email)
            if result:
                st.success("Logged in as {}".format(username))
                st.subheader("Great! Now you can access the entire site.")

                SecuredPages = {"Home": home, "My Portfolio": myPortfolio, "Analysis": portfolio,
                                "Prediction": prediction, "Glossary": glossary}

                selection = st.sidebar.radio("Menu", list(SecuredPages.keys()))
                sec_page = SecuredPages[selection]
                sec_page.app()
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        email = st.text_input("Email")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')


        try:
            if st.button("Signup"):
                add_userdata(new_user, make_hashes(new_password), email)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login menu to login")

        except pymongo.errors.DuplicateKeyError:
            st.warning("This email-id is already in use. Create another one.")



