#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Minimal test app to verify Gradio works
"""

import gradio as gr

def hello(name):
    return f"Hello {name}! Gradio is working!"

# Create simple interface
demo = gr.Interface(
    fn=hello,
    inputs=gr.Textbox(label="Your Name"),
    outputs=gr.Textbox(label="Greeting"),
    title="3MF Tools - Connection Test"
)

if __name__ == "__main__":
    print("Starting test app...")
    print("If this works, the main app should too!")
    demo.launch(
        share=False,
        inbrowser=True
    )
