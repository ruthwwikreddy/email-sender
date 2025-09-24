import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from email_sender import send_email, generate_ai_message
from dotenv import load_dotenv

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender")
        self.root.geometry("700x700")
        
        # Load environment variables
        load_dotenv()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="Email Sender with AI", style='Header.TLabel')
        header.pack(pady=10)
        
        # Recipient
        recipient_frame = ttk.Frame(main_frame)
        recipient_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(recipient_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.recipient_var = tk.StringVar()
        recipient_entry = ttk.Entry(recipient_frame, textvariable=self.recipient_var, width=50)
        recipient_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Subject
        subject_frame = ttk.Frame(main_frame)
        subject_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(subject_frame, text="Subject:").pack(side=tk.LEFT, padx=5)
        self.subject_var = tk.StringVar()
        subject_entry = ttk.Entry(subject_frame, textvariable=self.subject_var, width=50)
        subject_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Message
        ttk.Label(main_frame, text="Message:").pack(anchor=tk.W, pady=(10, 0))
        self.message_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=15)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # AI Generation Frame
        ai_frame = ttk.Frame(main_frame)
        ai_frame.pack(fill=tk.X, pady=5)
        
        self.ai_prompt_var = tk.StringVar()
        ai_prompt_entry = ttk.Entry(ai_frame, textvariable=self.ai_prompt_var, width=50)
        ai_prompt_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ai_button = ttk.Button(ai_frame, text="Generate with AI", command=self.generate_ai_message)
        ai_button.pack(side=tk.LEFT, padx=5)
        
        # Attachments
        self.attachments = []
        
        attachment_frame = ttk.Frame(main_frame)
        attachment_frame.pack(fill=tk.X, pady=5)
        
        add_attachment_btn = ttk.Button(attachment_frame, text="Add Attachment", command=self.add_attachment)
        add_attachment_btn.pack(side=tk.LEFT, padx=5)
        
        self.attachment_list = tk.Listbox(attachment_frame, height=3, width=50)
        self.attachment_list.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        remove_attachment_btn = ttk.Button(attachment_frame, text="Remove", command=self.remove_attachment)
        remove_attachment_btn.pack(side=tk.LEFT, padx=5)
        
        # Send Button
        send_frame = ttk.Frame(main_frame)
        send_frame.pack(pady=10)
        
        send_btn = ttk.Button(send_frame, text="Send Email", command=self.send_email, style='Accent.TButton')
        send_btn.pack(pady=10, ipadx=20, ipady=5)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
    def add_attachment(self):
        file_paths = filedialog.askopenfilenames(title="Select files to attach")
        for file_path in file_paths:
            if file_path not in self.attachments:
                self.attachments.append(file_path)
                self.attachment_list.insert(tk.END, os.path.basename(file_path))
    
    def remove_attachment(self):
        try:
            selection = self.attachment_list.curselection()[0]
            del self.attachments[selection]
            self.attachment_list.delete(selection)
        except IndexError:
            pass
    
    def generate_ai_message(self):
        prompt = self.ai_prompt_var.get().strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt for the AI")
            return
            
        self.status_var.set("Generating message with AI...")
        self.root.update()
        
        try:
            message = generate_ai_message(prompt)
            if message:
                self.message_text.delete(1.0, tk.END)
                self.message_text.insert(tk.END, message)
                self.status_var.set("AI message generated successfully")
            else:
                messagebox.showerror("Error", "Failed to generate message. Please check your API key and internet connection.")
                self.status_var.set("Error generating message")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error: " + str(e))
    
    def send_email(self):
        recipient = self.recipient_var.get().strip()
        subject = self.subject_var.get().strip()
        message = self.message_text.get(1.0, tk.END).strip()
        
        if not recipient:
            messagebox.showerror("Error", "Please enter a recipient email address")
            return
            
        if not subject:
            if not messagebox.askyesno("No Subject", "The email has no subject. Send anyway?"):
                return
        
        if not message:
            if not messagebox.askyesno("Empty Message", "The email has no message. Send anyway?"):
                return
        
        self.status_var.set("Sending email...")
        self.root.update()
        
        try:
            success = send_email(recipient, subject, message, self.attachments)
            if success:
                messagebox.showinfo("Success", "Email sent successfully!")
                self.status_var.set("Email sent successfully")
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to send email. Please check your settings and try again.")
                self.status_var.set("Failed to send email")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error: " + str(e))
    
    def clear_form(self):
        self.recipient_var.set("")
        self.subject_var.set("")
        self.message_text.delete(1.0, tk.END)
        self.ai_prompt_var.set("")
        self.attachments = []
        self.attachment_list.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = EmailSenderApp(root)
    
    # Set window icon and style
    try:
        root.iconbitmap("icon.ico")  # You can add an icon file if desired
    except:
        pass  # Continue without icon if not found
    
    # Configure the style for the send button
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#0078d7')
    
    root.mainloop()

if __name__ == "__main__":
    main()
