import os
import google.generativeai as genai
from dotenv import load_dotenv

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_outreach_message(founder_name, company_name, linkedin, website, about):
    prompt = f"""
    You're a professional assistant writing outreach messages.

    Founder: {founder_name}
    Company: {company_name}
    LinkedIn: {linkedin}
    Website: {website}
    About: {about}

    Create a friendly, professional outreach message:
    - Greet the founder by name.
    - Mention one impressive aspect about the company based on the description provided.
    - Include a compliment about the founder's work.

    Thi is the format: 
    `Hi {founder_name},
    So I had a quick look (yes I do check profiles) at {company_name}.I like [insert impressive aspect here].
    I also like [insert compliment about the founder's work here].

    $4k for a 2-month project. Past clients and testimonial from scale-up Tally.xyz (their customer hold $80B+ in assets).

    Our secret? 

    — lean startup builders 
    — prototyping, AI, full stack, design, user testing
    — CTO with 25+ years experience  
    — top 0.1% talent pipeline via #1 university in Kenya

    1 week free trial available for Startup Grind. Book in discovery: https://app.usemotion.com/meet/simonsallstrom/discovery `
    Make it sound natural and engaging. Avoid being too formal or robotic.
    Always maintain the formatting and structure of the message.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating outreach message: {str(e)}")
        return "Error generating message"
