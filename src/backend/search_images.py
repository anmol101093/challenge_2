import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import Paths,target_height,target_width
import os

# Function to search for an image by depth
def search_image_by_depth(depth_min,depth_max):

    '''
    Accept Paramter: minimum & maiximu depth
    response : return the image frames between min & max depth from sqllite db. 
    '''

    db=os.path.join(os.getcwd(),'data','sql','images.db')
    print(db)
    engine = create_engine(f'sqlite:///{db}')
    query = f"SELECT * FROM images WHERE depth BETWEEN {depth_min} AND {depth_max}"
    result = pd.read_sql(query, engine)

    if not result.empty:
        depth=result['depth'].to_list()
        image_data = result.drop(columns='depth')
        return image_data,depth
    else:
        return None
