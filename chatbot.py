import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# ============================================
# KNOWLEDGE BASE - Company Support Info
# ============================================
KNOWLEDGE_BASE = """
Company: SuchiTechCorp Customer Support

Q: What are your support hours?
A: We provide 24/7 customer support via email and chat.

Q: How do I reset my password?
A: Go to login page → Click "Forgot Password" → Enter email → Follow reset link in email.

Q: What payment methods do you accept?
A: We accept credit cards (Visa, Mastercard, Amex), PayPal, and bank transfers.

Q: How long does shipping take?
A: Standard shipping takes 5-7 business days. Express shipping takes 2-3 days.

Q: What is your return policy?
A: 30-day money-back guarantee on all products. No questions asked.

Q: Do you offer discounts for bulk orders?
A: Yes, 10% off on orders over $500, 15% off on orders over $1000.

Q: How can I contact support?
A: Email: support@suchitechcorp.com | Chat: Available on website | Phone: 1-800-SUCHITECHCORP

Q: Do you ship internationally?
A: Yes, we ship to 50+ countries. International shipping takes 10-14 business days.

Q: What is your pricing?
A: Basic Plan: $9.99/month | Pro Plan: $29.99/month | Enterprise: Custom pricing

Q: Can I cancel my subscription anytime?
A: Yes, cancel anytime with no penalties or cancellation fees.
"""

# ============================================
# CHATBOT FUNCTION
# ============================================
def chat_with_bedrock(user_message):
    """
    Send user message to Claude via AWS Bedrock
    Claude will use the knowledge base to answer
    
    Args:
        user_message (str): The customer's question
    
    Returns:
        str: Claude's response
    """
    
    try:
        # Create prompt that includes knowledge base context
        prompt = f"""You are a helpful and friendly customer support chatbot for SuchiTechCorp.
         Customer Support

Your job is to answer customer questions using the knowledge base provided below.

=== KNOWLEDGE BASE START ===
{KNOWLEDGE_BASE}
=== KNOWLEDGE BASE END ===

Customer Question: {user_message}

Instructions:
1. Answer based ONLY on the knowledge base provided
2. If the answer is in the knowledge base, provide it clearly and friendly
3. If you don't have the answer, say: "I don't have that information. Please contact support at support@SuchiTechcorp.com or call 1-800-SUCHITECHCORP"
4. Keep answers short and helpful (2-3 sentences max)
5. Be friendly and professional

Answer:"""

        # Call Claude through AWS Bedrock
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # Using Claude 3 Sonnet
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-06-01",
                "max_tokens": 500,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        # Parse response from Bedrock
        result = json.loads(response['body'].read())
        assistant_message = result['content'][0]['text']
        
        return assistant_message.strip()
    
    except Exception as e:
        return f"Error: {str(e)}. Please make sure AWS credentials are configured correctly."

# ============================================
# INTERACTIVE CHATBOT - Run Locally
# ============================================
def main():
    """
    Main function to run the chatbot interactively
    """
    print("\n" + "="*60)
    print("🤖 Welcome to SuchiTechCorp Customer Support Chatbot!")
    print("="*60)
    print("I can help you with:")
    print("  • Support hours")
    print("  • Password reset")
    print("  • Shipping info")
    print("  • Returns & refunds")
    print("  • Pricing & billing")
    print("\nType 'quit' or 'exit' to end the chat")
    print("="*60 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🤖 Bot: Thank you for using SuchiTechCorp Support! Have a great day!")
                print("="*60 + "\n")
                break
            
            # Skip empty input
            if not user_input:
                print("Please enter a question.\n")
                continue
            
            # Get response from chatbot
            print("\n🤖 Bot: ", end="", flush=True)
            response = chat_with_bedrock(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! Thanks for reaching out to SuchiTechCorp Support.")
            print("="*60 + "\n")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again.\n")

# ============================================
# FUNCTION TO TEST WITH SPECIFIC QUESTIONS
# ============================================
def test_chatbot():
    """
    Test the chatbot with predefined questions
    Useful for debugging and demonstrating capabilities
    """
    test_questions = [
        "What are your support hours?",
        "How do I reset my password?",
        "How long does shipping take?",
        "What is your return policy?",
        "Do you offer bulk discounts?",
        "Can I cancel anytime?",
        "What's your phone number?",
        "Do you ship to India?",
    ]
    
    print("\n" + "="*60)
    print("🧪 Testing Chatbot with Sample Questions")
    print("="*60 + "\n")
    
    for question in test_questions:
        print(f"Q: {question}")
        response = chat_with_bedrock(question)
        print(f"A: {response}\n")
    
    print("="*60 + "\n")

# ============================================
# ENTRY POINT
# ============================================
if __name__ == "__main__":
    import sys
    
    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_chatbot()
    else:
        # Run interactive chatbot
        main()