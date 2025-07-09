import cloudinary
import cloudinary.uploader


# ✅ Configure Cloudinary only once
cloudinary.config(
    cloud_name="dojwvvreb",
    api_key="936771169143842",
    api_secret="EtLPKlw-W2B0qA7msUlN4lDMH3E",
   
)

# ✅ Upload function - make it async
async def upload_file_to_cloudinary(file_obj):
    try:
        # Read file content as bytes
        file_content = await file_obj.read()
        
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(file_content)
        print("File uploaded successfully:", response)
        return response["secure_url"]
    except Exception as e:
        print("Error uploading file to Cloudinary:", e)
        return None
