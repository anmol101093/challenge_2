import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import Paths, target_width,target_height,original_width


def load_data():

    '''
    Load the input csv file , reshape it width from 200 to 150  and load them in sqlite DB for 
    persistent storage and query on them.
    '''
    df=pd.read_csv(Paths.input_data)
    X=df.drop(labels='depth',axis=1)
    Y=df['depth']

    new_df, width,height=reshape_images(X,Y)
    load_db(new_df,width,height)

def reshape_images(X,Y):
    '''
    Accept Paramter: X- pixel data of each row
                     Y- depth at which image was taken 
    response : return the resized dataframe and new height & width.  
    '''

    # Calculate the necessary padding for each row
    padding_needed = target_width * target_height - original_width

    padded_images = []

    for index, row in X.iterrows():
        # Convert the row to a numpy array
        img = np.array(row)

        # Add padding to the end of the array
        padded_img = np.pad(img, (0, padding_needed), mode='constant', constant_values=0)

        # Reshape to the target height and width
        padded_img_reshaped = padded_img.reshape(target_height, target_width)

        # Flatten the padded image back to 1D and add to the list
        padded_images.append(padded_img_reshaped.flatten())

    # Convert the list of padded images back to a DataFrame
    padded_df = pd.DataFrame(padded_images)

    padded_df.dropna(inplace=True)


    #rename columns
    new_columns=[f'column_{i}' for i in range(target_width * target_height)]
    padded_df.columns=new_columns
    padded_df.insert(0,'depth',Y)

    return padded_df, target_width,target_height


def load_db(padded_df,target_width,target_height):

    '''
    Accept Paramter: resized dataframe, new width & height
    Load the resized dataframe into .db file in chunks. 
    '''
    # # Save the resized data to a database
    db=f'sqlite:///{Paths.db_data}'
    engine = create_engine(db)

    # Ensure the primary key constraint by creating the table manually
    with engine.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS images (
                depth FLOAT PRIMARY KEY,
                {}
            )
        '''.format(', '.join(f'column_{i} INTEGER' for i in range(target_width * target_height))))


    # Insert the DataFrame into the table in chunks
    chunk_size = 500  
    for i in range(0, len(padded_df), chunk_size):
        chunk = padded_df.iloc[i:i + chunk_size]
        chunk.to_sql('images', engine, if_exists='append', index=False, method='multi')



