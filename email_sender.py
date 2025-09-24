import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import openai
from pathlib import Path

def load_environment():
    """Load environment variables from .env file"""
    if not load_dotenv():
        print("Warning: .env file not found or couldn't be loaded")
    
    required_vars = [
        'SMTP_SERVER',
        'SMTP_PORT',
        'SENDER_EMAIL',
        'SENDER_PASSWORD',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with these variables")
        return False
    return True

def generate_ai_message(prompt, max_tokens=150):
    """Generate message using OpenAI's API"""
    try:
        # Initialize the client with minimal configuration
        client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            timeout=30.0  # Add a timeout to prevent hanging
        )
        
        # Make the API request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7  # Add temperature for more creative responses
        )
        
        # Extract and return the generated message
        if response and response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        return ""
    except Exception as e:
        print(f"Error generating AI message: {e}")
        return None

def send_email(recipient, subject, message, attachments=None):
    """Send an email with optional attachments"""
    try:
        print("\n🔄 Attempting to send email...")
        
        # Validate email addresses
        if '@' not in recipient or '.' not in recipient.split('@')[-1]:
            print("❌ Invalid recipient email address")
            return False
            
        # Get SMTP settings from environment
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '465'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            print("❌ Sender email or password not configured")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Add attachments if any
        if attachments:
            print(f"📎 Attaching {len(attachments)} file(s)...")
            for attachment_path in attachments:
                try:
                    if not os.path.exists(attachment_path):
                        print(f"   ❌ Attachment not found: {attachment_path}")
                        continue
                        
                    with open(attachment_path, 'rb') as f:
                        part = MIMEApplication(
                            f.read(),
                            Name=Path(attachment_path).name
                        )
                        part['Content-Disposition'] = f'attachment; filename="{Path(attachment_path).name}"'
                        msg.attach(part)
                        print(f"   ✅ Added: {Path(attachment_path).name}")
                except Exception as e:
                    print(f"   ❌ Could not attach {attachment_path}: {e}")
        
        # Create secure connection and send email
        print("🔗 Connecting to SMTP server...")
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            print("🔐 Logging in...")
            server.login(sender_email, sender_password)
            print("✉️  Sending message...")
            server.send_message(msg)
        
        print("\n✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        return False

def main():
    print("📧 Email Sender with AI Assistant")
    print("=" * 30)
    
    if not load_environment():
        print("\nPlease create a .env file with the following variables:")
        print("SMTP_SERVER=your_smtp_server")
        print("SMTP_PORT=your_smtp_port")
        print("SENDER_EMAIL=your_email@example.com")
        print("SENDER_PASSWORD=your_email_password")
        print("OPENAI_API_KEY=your_openai_api_key")
        return
    
    # Get recipient email
    while True:
        recipient = input("\n📨 Recipient's email address: ").strip()
        if '@' in recipient and '.' in recipient.split('@')[-1]:
            break
        print("Please enter a valid email address")
    
    # Get subject
    subject = input("📝 Email subject: ").strip()
    
    # Ask if user wants to generate message with AI
    use_ai = input("\n🤖 Would you like to generate the message with AI? (y/n): ").lower().strip() == 'y'
    
    if use_ai:
        prompt = input("\n💡 Enter a prompt to generate your email message: ")
        print("\nGenerating message with AI...")
        message = generate_ai_message(prompt)
        if not message:
            print("Failed to generate message with AI. Please enter your message manually.")
            message = input("\n✍️ Your message (press Enter twice to finish):\n")
        else:
            print("\nGenerated message:")
            print("-" * 50)
            print(message)
            print("-" * 50)
            
            edit = input("\nWould you like to edit this message? (y/n): ").lower().strip() == 'y'
            if edit:
                print("Enter your updated message (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == '':
                        if lines and lines[-1] == '':
                            break
                    lines.append(line)
                message = '\n'.join(lines[:-1])
    else:
        print("\n✍️ Enter your message (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == '':
                if lines and lines[-1] == '':
                    break
            lines.append(line)
        message = '\n'.join(lines[:-1])
    
    # Handle attachments
    attachments = []
    while True:
        attach = input("\n📎 Add an attachment? (y/n): ").lower().strip()
        if attach != 'y':
            break
        file_path = input("Enter file path: ").strip('"')
        if os.path.exists(file_path):
            attachments.append(file_path)
            print(f"Added: {file_path}")
        else:
            print("File not found. Please try again.")
    
    # Confirm before sending
    print("\n" + "=" * 50)
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print("-" * 50)
    print(message)
    if attachments:
        print("\nAttachments:")
        for att in attachments:
            print(f"- {att}")
    print("=" * 50)
    
    confirm = input("\nSend this email? (y/n): ").lower().strip()
    if confirm == 'y':
        send_email(recipient, subject, message, attachments if attachments else None)
    else:
        print("\nEmail not sent.")

if __name__ == "__main__":
    main()
