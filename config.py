from pathlib import Path

class Paths:
    """ data class to initialize path variables"""
    root: Path= Path(__file__).parent
    input_data: Path=root /"data"/"input"/"Challenge2.csv"
    db_data: Path=root /"data"/"sql"/"images.db"

#image parameters
target_width=150
original_width=200
target_height=(original_width//target_width)+1