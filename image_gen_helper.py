import os
import base64
from io import BytesIO
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_pipeline_image(explanation: str, output_path: str = "generated_pipeline.png") -> str:
    """
    Generate ByteByteGo-style architecture image using OpenAI DALL·E 3 model.
    Saves to output_path and returns file path.
    """

    if not client.api_key:
        raise RuntimeError("OPENAI_API_KEY not configured in your .env file.")

    prompt = f"""
Create a clean, colorful ByteByteGo-style architecture diagram.
Include sections: Problem, Requirements, Data Flow, Trade-offs.
Show Azure Blob → Databricks → Bronze/Silver/Gold → Synapse → Power BI.
Make it infographic style (short labels). Use icons and arrows.

Context summary:
{explanation}
"""

    # 🔁 Using DALL·E 3 instead (more widely available)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1,
    )

    # Prefer URL if b64_json is not available
    print("DEBUG IMAGE RESPONSE:", response)  # Add this line
    if not hasattr(response, "data") or not response.data:
        raise RuntimeError(f"OpenAI returned no image data. Full response: {response}")
    image_info = response.data[0]

    if hasattr(image_info, "b64_json") and image_info.b64_json:
        image_bytes = base64.b64decode(image_info.b64_json)
    elif hasattr(image_info, "url") and image_info.url:
        # Streamlit will load from URL directly
        return image_info.url
    else:
        raise RuntimeError("Image generation failed. API returned no usable image data.")

    # Save locally (if b64 provided)
    output_file = Path(output_path)
    output_file.write_bytes(image_bytes)
    return str(output_file)
