# import validators
# import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# # Streamlit APP Configuration
# st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
# st.title("🦜 LangChain: Summarize Text From YT or Website")
# st.subheader('Summarize URL')

# # Get the Groq API Key and URL (YT or website) to be summarized
# with st.sidebar:
#     groq_api_key = st.text_input("Groq API Key", value="", type="password")

# generic_url = st.text_input("URL", label_visibility="collapsed")

# # Check if the API Key and URL are provided
# if st.button("Summarize the Content from YT or Website"):
#     if not groq_api_key.strip() or not generic_url.strip():
#         st.error("Please provide both the Groq API Key and the URL to get started.")
#     elif not validators.url(generic_url):
#         st.error("Please enter a valid URL. It can be a YT video URL or a website URL.")
#     else:
#         try:
#             with st.spinner("Waiting..."):
#                 # Initialize the ChatGroq model with the provided API Key
#                 llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

#                 # Load the website or YT video data
#                 if "youtube.com" in generic_url:
#                     loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
#                 else:
#                     loader = UnstructuredURLLoader(
#                         urls=[generic_url],
#                         ssl_verify=False,
#                         headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
#                     )
#                 docs = loader.load()

#                 # Define the prompt template
#                 prompt_template = """
#                 Provide a summary of the following content in 300 words:
#                 Content:{text}
#                 """
#                 prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

#                 # Chain for Summarization
#                 chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
#                 output_summary = chain.run(docs)

#                 st.success(output_summary)
#         except Exception as e:
#             st.exception(f"Exception: {e}")

import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import io

# Streamlit APP Configuration
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

# Get the Groq API Key and URL (YT or website) to be summarized
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

# Check if the API Key and URL are provided
if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both the Groq API Key and the URL to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YT video URL or a website URL.")
    else:
        try:
            with st.spinner("Processing..."):
                # Initialize the ChatGroq model with the provided API Key
                llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

                # Load the website or YT video data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                    
                    # Display YouTube video thumbnail
                    video_id = generic_url.split("v=")[-1]
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                    st.image(thumbnail_url, caption="YouTube Video Thumbnail", use_column_width=True)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                    )
                    # Display a preview of the website content
                    st.markdown(f"**Website URL:** [Link]({generic_url})")
                    
                docs = loader.load()

                # Define the prompt template
                prompt_template = """
                Provide a summary of the following content in 300 words:
                Content:{text}
                """
                prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

                # Chain for Summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success("Summary generated successfully!")

                # Display the summary
                st.write(output_summary)

                # Provide option to download the summary
                summary_bytes = output_summary.encode()  # Convert the summary to bytes
                st.download_button(
                    label="Download Summary",
                    data=summary_bytes,
                    file_name="summary.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.exception(f"An error occurred: {e}")

# Additional styling for a better user experience
st.markdown("""
    <style>
    .css-1g6z4e0 {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

