import tkinter as tk
from tkinter import scrolledtext, messagebox
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from playwright.sync_api import sync_playwright

# Load LLaMA 3 
MODEL_NAME = "meta-llama/Llama-3-7b-hf"

print("Loading model... (first time will be slow)")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_test_script(test_action, test_data):
    prompt = f"""
    You are an automation testing assistant.
    Tester wants to: {test_action}
    Test data: {test_data}
    Generate Python Playwright code to perform this action.
    """
    result = generator(prompt, max_length=300)[0]["generated_text"]
    return result

def run_script(script_code):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            exec(script_code, {"page": page})
            browser.close()
    except Exception as e:
        messagebox.showerror("Error", f"Test failed: {e}")

def on_run():
    test_action = action_entry.get("1.0", tk.END).strip()
    test_data = data_entry.get("1.0", tk.END).strip()

    if not test_action or not test_data:
        messagebox.showwarning("Missing Input", "Please provide both test action and test data.")
        return

    script = generate_test_script(test_action, test_data)
    script_output.delete("1.0", tk.END)
    script_output.insert(tk.END, script)

    run_script(script)

# UI Setup
root = tk.Tk()
root.title("AI Test Automation App")

tk.Label(root, text="Test Action:").pack(anchor="w")
action_entry = scrolledtext.ScrolledText(root, width=60, height=4)
action_entry.pack(padx=5, pady=5)

tk.Label(root, text="Test Data (JSON format):").pack(anchor="w")
data_entry = scrolledtext.ScrolledText(root, width=60, height=4)
data_entry.pack(padx=5, pady=5)

run_button = tk.Button(root, text="Generate & Run Test", command=on_run, bg="lightblue")
run_button.pack(pady=10)

tk.Label(root, text="Generated Script:").pack(anchor="w")
script_output = scrolledtext.ScrolledText(root, width=80, height=15)
script_output.pack(padx=5, pady=5)

root.mainloop()
