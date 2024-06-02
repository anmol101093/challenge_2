"""
This module contains Fast API routes for handling search image based on depth min & max.
 
Routes:
    - POST /search_images : extracting images from database for min & max depth.
"""
 
from fastapi import APIRouter, Request
from model.model import SearchModel,Status
from src.backend.search_images import search_image_by_depth
from src.backend.load_images import load_data
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from io import BytesIO
import numpy as np
router = APIRouter()
from fastapi.responses import StreamingResponse
from config import target_height,target_width
 
@router.post(
    "/search_images",
    status_code=200,
    tags=["depth min ", "depth max"],
    description="extracting images from database for min & max depth",
)
async def getImages(request_state: Request, request:SearchModel):
    """
 
    Parameters:
        - depth min (int): minimum depth
        - depth max (int): maximum depth
 
    Returns:
        dict: return list of images between min & max depth
    """
    depth_min=request.depth_min
    depth_max=request.depth_max
    images,depth=search_image_by_depth(depth_min,depth_max)
    if len(images)>0:
        images=images.reset_index(drop=True)

        # custom color map
        colors = ["blue", "green", "yellow", "orange", "red"]
        custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

        # Create subplots for multiple images
        num_images = images.shape[0]
    
        _, axes = plt.subplots(num_images, 3, figsize=(10, 5 * num_images))

        for idx, ax in enumerate(axes.flat):
            if idx < num_images:
                image_data = images.values[idx].reshape(target_height,target_width)  # Reshape each row
                ax.imshow(image_data, cmap=custom_cmap)
                ax.set_title(f'Image - {depth[idx]}')
            else:
                ax.axis('off')  # Hide unused subplots
            
    
        plt.tight_layout()

        # Save plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
    
        return StreamingResponse(buf, media_type="image/png")
        
    else:
        return {"status": Status.failure, "response": f"No image found for the min dpeth-{depth_min} & max depth - {depth_max} range specified"}


@router.post(
    "/save_images",
    status_code=200,
    description="saving images to database",
)
async def saveImages(request_state: Request):
    load_data()
    return {"status": Status.success, "response": "data has been loaded to the sqlite db"}