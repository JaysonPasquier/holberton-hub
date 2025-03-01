import cloudinary
import cloudinary.uploader
import cloudinary.api

# Initialize Cloudinary with your credentials
def initialize_cloudinary():
    cloudinary.config(
        cloud_name = "dsvolcznm",
        api_key = "445719466135631",
        api_secret = "6e_FbbsVgoZi8SyybxHPfzgL8nE",
        secure = True
    )
