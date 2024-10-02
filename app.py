import streamlit as st
import requests
import groq
import traceback

def generate_email(api_key, industry, recipient_role, personal_details,objective,recipient_name,max_tokens,temperature):
    # Initialize the client using the API key
    client= groq.Groq(api_key=api_key)
    
    # Create a prompt for generating an email
    try:
        prompt = f"""
        You are an expert email writer, tasked with generating a professional and personalized cold email. 
        The email should aim to engage a {recipient_role} working in the {industry} industry. 

        - The purpose of the email is to {objective}. 
        - Use a polite and professional tone, focusing on providing value to the recipient.
        - Keep the email concise, clear, and persuasive. Avoid overly formal language but maintain professionalism.
        - Include the following details about the sender or company: {personal_details}.
        - The email should have a compelling subject line and end with a strong call to action.
        - The email should feel personal, not generic.
        - the email is written to a person name {recipient_name}, analyze the name and address with sir/maam depeding on the name

        Generate an email with the following structure:
        1. Subject line: A short and engaging subject line relevant to the {industry}.
        2. Introduction: A brief and friendly introduction that explains why the sender is reaching out.
        3. Body: Highlight key points, such as how the sender’s offer or product can benefit the recipient or solve a relevant pain point for their industry.
        4. Conclusion: Politely invite the recipient to continue the conversation or take a specific action.
        5. Sign-off: Include a polite and professional closing.
        """

        system_prompt = """
        You are EmailGenie, an AI expert in crafting professional cold emails. 
        Your task is to generate concise, personalized emails that clearly convey value. 
        Maintain a polite and professional tone, and structure the email with a subject, intro, body, and call to action.
        """

        
        response = client.chat.completions.create(
            messages=[
                {
                "role": "system",
                "content": system_prompt,  
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            max_tokens=int(max_tokens),
            temperature=float(temperature),
        )

        generated_email = response.choices[0].message.content
        return generated_email
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return error_message
    

st.set_page_config(
        page_title= "EmailGenie",
        page_icon= "🧞‍♂️")

def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;  /* Green */
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    
    st.title("EmailGenie 🧞‍♂️: AI-Powered Email Generator ✉️")
    st.write("Craft personalized cold outreach emails effortlessly.")

    # User input fields arranged in two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        api_key = st.text_input("Enter your Groq API Key:")
        industry = st.text_input("Enter your industry:")
        recipient_role = st.text_input("Enter the recipient's role:")
        recipient_name = st.text_input("Enter the name of the recipient:")

    with col2:
        objective = st.text_area("Enter the objective of writing this email:")
        personal_details = st.text_area("Enter personal or company details:")
        temperature = st.slider("Select Temperature:", min_value=0.0, max_value=2.0, value=1.0)
        max_tokens = st.slider("Select Max Tokens:", min_value=200, max_value=500, value=300)

    # Button to generate the email
    if st.button("Generate Email"):
        if api_key and industry and recipient_role and personal_details and objective and recipient_name:
            email = generate_email(api_key, industry, recipient_role, personal_details, objective, recipient_name, max_tokens, temperature)
            st.subheader("Generated Email:")
            st.write(email)
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
