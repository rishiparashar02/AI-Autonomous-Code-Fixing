import groq
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_patch(bug_description, code_snippet):
    """
    Generates a patch suggestion using Groq API.
    
    Args:
        bug_description (str): Description of the bug.
        code_snippet (str): The original code snippet.
    
    Returns:
        str: The suggested corrected code, or None if error.
    """
    try:
        # Get API key from environment
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            logger.error("Groq API key not found in environment variables")
            return None
        
        client = groq.Groq(api_key=api_key)
        
        prompt = f"""
Bug Description: {bug_description}

Original Code:
{code_snippet}

Please provide the corrected version of this code that fixes the bug. Output only the corrected code, no explanations or additional text.
"""
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        corrected_code = response.choices[0].message.content.strip()
        logger.info("Successfully generated patch suggestion")
        return corrected_code
        
    except groq.GroqError as e:
        logger.error(f"Groq API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in patch generation: {e}")
        return None