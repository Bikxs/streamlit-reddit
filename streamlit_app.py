import streamlit as st
from google.cloud import firestore

CREDENTIALS_FILE = "firebase-adminsdk.json"

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json(CREDENTIALS_FILE)


def new_post():
    # Create a container for the modal
    modal = st.empty()
    # Display the form when the button is clicked
    with modal:
        st.subheader("New Post Form")
        title = st.text_input("Post title")
        url = st.text_input("Post URL")
        content = st.text_input("Content")
        submit = st.button("Submit")

    # Check if the "Submit" button is clicked
    if title and url and content and submit:
        modal.empty()  # Close the modal
        doc_ref = db.collection("posts").document(f"{title}")
        # And then uploading some data to that reference
        doc_ref.set({
            "title": title,
            "url": url,
            "content": content
        })
        st.success(f"Post {title} created")


def material_card(post):
    card_style = f"""
        background-color: #fff;
        padding: 1rem;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    """
    st.markdown(
        f"""
        <div style="{card_style}">
            <h2>{post['title']}</h2>
            <p>{post['content']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

#render the streamlit app

st.title("Reddit Clone")
st.subheader("Totorial app that uses Streamlit, Streamlit sharing, and Firestore")
if st.button("New Post"):
    new_post()

posts_ref = db.collection("posts")
for doc in posts_ref.stream():
    material_card(doc.to_dict())
