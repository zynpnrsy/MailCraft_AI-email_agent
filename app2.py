#gradio'ya bağlanan kod, approved-rejected yapısı burada  
import gradio as gr
from agents import reader_agent, classifier_agent, response_agent, critic_agent

def process_workflow(email_input):
    # 1. Reader Agent
    cleaned = reader_agent(email_input)
    
    # 2. Classifier Agent
    category = classifier_agent(cleaned)
    
    # 3. Response Agent
    draft_reply = response_agent(category, cleaned)
    
    # 4. Critic Agent
    critic_feedback = critic_agent(draft_reply)
    
    is_approved = "APPROVED" in critic_feedback.upper()
    # Return results and make action buttons visible
    return (
        cleaned, 
        category, 
        draft_reply, 
        critic_feedback, 
        gr.update(visible=True, variant="success" if is_approved else "secondary"), 
        gr.update(visible=True)
    )

def handle_approval(final_draft):
    # This is where you'd integrate an SMTP library to actually send the mail
    return f"### ✅ Success!\n**Status:** Email has been sent.\n\n**Final Content:**\n\n{final_draft}"

def handle_rejection():
    return "### ❌ Rejected\n**Status:** Draft discarded. No email was sent."

# Building the UI
with gr.Blocks(theme=gr.themes.Soft(), title="AI Email Assistant") as demo:
    gr.Markdown("#  **AI MULTI-AGENT E-MAIL ASSISTANT**")
    gr.Markdown("Powered by local **Ollama (Mistral)** model.")
    gr.Markdown("**by zeyneppinarsoy** ")

    with gr.Row():
        email_input = gr.Textbox(
            label="Incoming Email Content", 
            placeholder="Paste the email you received here...", 
            lines=6
        )
    
    analyze_btn = gr.Button("Run Agents & Generate Draft", variant="primary")
    
    gr.HTML("<hr>")
    
    with gr.Row():
        with gr.Column():
            out_cleaned = gr.Textbox(label="🔍 Reader Agent (Cleaned Text)", interactive=False)
            out_category = gr.Textbox(label="🏷️ Classifier Agent (Category)", interactive=False)
        
        with gr.Column():
            out_draft = gr.Textbox(label="✍️ Response Agent (Draft)", lines=5, interactive=True)
            out_critic = gr.Textbox(label="⚖️ Critic Agent (Review/Feedback)", lines=5, interactive=False)

    # Action Buttons (Hidden by default)
    with gr.Row():
        approve_btn = gr.Button("APPROVE & SEND", variant="success", visible=False)
        reject_btn = gr.Button("REJECT & DISCARD", variant="stop", visible=False)
    
    # Status Message Area
    status_output = gr.Markdown("")

    # Logic Mapping
    analyze_btn.click(
        fn=process_workflow,
        inputs=[email_input],
        outputs=[out_cleaned, out_category, out_draft, out_critic, approve_btn, reject_btn]
    )

    approve_btn.click(fn=handle_approval, inputs=[out_draft], outputs=[status_output])
    reject_btn.click(fn=handle_rejection, outputs=[status_output])
    
if __name__ == "__main__":
    demo.launch()
    
    
    
    """
    approve_btn.click(
        fn=handle_approval,
        inputs=[out_draft],
        outputs=[status_output]
    )

    reject_btn.click(
        fn=handle_rejection,
        outputs=[status_output]
    )
"""