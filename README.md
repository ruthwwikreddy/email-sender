# Email Sender with AI Assistant

A powerful Python application that lets you send emails with AI-generated messages using OpenAI's API. Perfect for automating emails with a personal touch!

## Features

- Send emails to any recipient with custom subjects and messages
- Generate email content using OpenAI's GPT-3.5
- Attach multiple files to your emails
- Beautiful command-line interface
- Secure configuration using environment variables
- Supports Gmail App Passwords for enhanced security

## Quick Start

### Prerequisites

- Python 3.7 or higher
- An email account with SMTP access (Gmail recommended)
- [Optional] OpenAI API key for AI message generation

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/email-sender.git
   cd email-sender
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your email and API credentials.

## Gmail Setup (Recommended)

1. Go to your [Google Account Settings](https://myaccount.google.com/)
2. Enable **2-Step Verification**
3. Create an **App Password**:
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" as the app and "Other (Custom name)" as the device
   - Name it "Python Email Sender"
   - Copy the generated 16-character password
4. Use this password in your `.env` file for `SENDER_PASSWORD`

## Configuration

Edit the `.env` file with your details:

```plaintext
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password  # 16-char App Password for Gmail

# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Command Line Interface

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the command-line application**:
   ```bash
   python email_sender.py
   ```

3. **Follow the interactive prompts**:
   - Enter recipient's email address
   - Add a subject line
   - Choose to generate a message with AI or write your own
   - Optionally attach files
   - Review and send the email

### Graphical User Interface (GUI)

1. **Make sure you have all dependencies installed**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the GUI application**:
   ```bash
   python email_gui.py
   ```

3. **Using the GUI**:
   - Enter the recipient's email address in the "To" field
   - Add a subject line
   - Write your message or use the AI to generate one
   - Click "Add Attachment" to attach files if needed
   - Click "Send Email" to send your message

#### AI Message Generation
   - Type a prompt in the text field at the bottom
   - Click "Generate with AI" to create a message based on your prompt
   - The generated message will appear in the message area

## Example Workflow

```bash
$ python email_sender.py
Email Sender with AI Assistant
==============================

Recipient's email address: example@example.com
Email subject: Let's Collaborate!

Would you like to generate the message with AI? (y/n): y

Enter a prompt to generate your email message: 
Write a professional email to a potential collaborator about working together on a new project

[AI generates the message...]

Add an attachment? (y/n): n

[Review and send the email...]
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure you're using an App Password (not your regular password)
   - Make sure 2-Step Verification is enabled

2. **Module Not Found**
   - Make sure you've activated the virtual environment
   - Run `pip install -r requirements.txt`

3. **SMTP Connection Issues**
   - Check your internet connection
   - Verify SMTP server and port settings
   - Try allowing less secure apps in your email settings (not recommended)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Uses [OpenAI's API](https://platform.openai.com/) for AI message generation
- Built with Python's built-in `smtplib` and `email` libraries
- Environment management with `python-dotenv`
