#gradio üzerinden email ve password girilen dashboard 
import gradio as gr
import re 
from agents import reader_agent, classifier_agent, response_agent, critic_agent
from gmail_service import get_latest_email, send_gmail

# Global değişkenler (Session bazlı basit saklama)
session_data = {"sender": "", "subject": ""}

def extract_metadata(email_text):
    import re

    # -----------------------------
    # ORDER NUMBER EXTRACTION
    # -----------------------------
    order_regex = r"(?:#\s*|order\s*(?:id|number|no)?\s*[:\-]?\s*)([A-Z0-9\-]+)"
    order_match = re.search(order_regex, email_text, re.IGNORECASE)
    order_no = order_match.group(1) if order_match else "Unknown_Order_No"

    # -----------------------------
    # USERNAME EXTRACTION (LABELED)
    # -----------------------------
    user_label_regex = r"(?:username|user|customer)[\s:]*([A-Za-z\s]+)"
    user_match = re.search(user_label_regex, email_text, re.IGNORECASE)

    if user_match:
        username = user_match.group(1).strip()

    else:
        # -----------------------------
        # SIGNATURE FALLBACK
        # -----------------------------
        lines = [line.strip() for line in email_text.split("\n") if line.strip()]

        if lines:
            possible_name = lines[-1]

            # Accept as name if:
            # - 1 to 3 words
            # - No email symbols
            # - No numbers
            # - Not too long
            if (
                1 <= len(possible_name.split()) <= 3
                and not any(char in possible_name for char in ".@:/0123456789")
                and len(possible_name) < 40
            ):
                username = possible_name
            else:
                username = "Dear Customer"
        else:
            username = "Dear Customer"

    return {
        "order_no": order_no,
        "username": username
    }
def fetch_and_analyze(email_addr, app_pass):
    global session_data

    sender, subject, body = get_latest_email(email_addr, app_pass)

    if "Error" in body:
        return body, "", "", "", "", gr.update(visible=False)

    session_data["sender"] = sender
    session_data["subject"] = subject

    # -------------------------
    # REGEX METADATA EXTRACTION
    # -------------------------
    metadata = extract_metadata(body)

    # -------------------------
    # AGENT PIPELINE
    # -------------------------
    reader_result = reader_agent(body)

    try:
        cleaned = reader_result.replace("CLEANED:", "").strip()
    except:
        cleaned = reader_result.strip()

    category = classifier_agent(cleaned)
    reply = response_agent(category, cleaned, metadata)
    review = critic_agent(reply)

    return (
        f"FROM: {sender}\nSUBJECT: {subject}\n\n{body}",
        cleaned,
        category,
        reply,
        review,
        gr.update(visible=True)
    )

def send_final_email(email_addr, app_pass, draft_text):
    send_gmail(email_addr, app_pass, session_data["sender"], session_data["subject"], draft_text)
    return "### ✅ SUCCESS: Email sent successfully!"

# Görsel Tasarım
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("<h1 style='text-align: center;'>📧 AI GMAIL DASHBOARD by zeyneppinarsoy</h1>")
    
    with gr.Accordion("⚙️ Gmail Connection Settings", open=True):
        with gr.Row():
            email_input = gr.Textbox(label="Your Gmail Address", placeholder="example@gmail.com")
            pass_input = gr.Textbox(label="App Password", type="password", placeholder="16-character code")

    fetch_btn = gr.Button("📩 FETCH & PROCESS LATEST EMAIL", variant="primary")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Incoming Mail")
            original_display = gr.Textbox(label="Full Content", lines=12, interactive=False)
            
        with gr.Column(scale=1):
            gr.Markdown("### 🤖 Agent Analysis")
            out_cleaned = gr.Textbox(label="Reader Agent (Summary)")
            out_category = gr.Textbox(label="Classifier Agent (Category)")
            out_critic = gr.Textbox(label="Critic Agent (Feedback)", lines=4)

    gr.Markdown("---")
    gr.Markdown("### ✍️ Final Draft & Action")
    out_draft = gr.Textbox(label="Editable AI Response", lines=6, interactive=True)
    
    send_btn = gr.Button("🚀 APPROVE & SEND TO SENDER", variant="success", visible=False)
    status_msg = gr.Markdown("")

    # Logic
    fetch_btn.click(
        fn=fetch_and_analyze,
        inputs=[email_input, pass_input],
        outputs=[original_display, out_cleaned, out_category, out_draft, out_critic, send_btn]
    )

    send_btn.click(
        fn=send_final_email,
        inputs=[email_input, pass_input, out_draft],
        outputs=[status_msg]
    )

if __name__ == "__main__":
    demo.launch()