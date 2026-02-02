import asyncio
from ai_content.providers.google.imagen import GoogleImagenProvider
from ai_content.config import configure

async def main():
    # Ensure config is loaded (to get env vars)
    configure('configs/default.yaml')
    
    provider = GoogleImagenProvider()
    print("Generating image with Imagen...")
    try:
        result = await provider.generate(
            prompt="A futuristic city with neon lights, cinematic, 8k",
            aspect_ratio="16:9",
            output_path="output/image/city.png",
            use_gemini=True
        )
        
        if result.success:
            print(f"Success! Saved to {result.file_path}")
        else:
            print(f"Failed: {result.error}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
