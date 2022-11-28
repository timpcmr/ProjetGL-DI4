from PIL import Image
from PIL.ExifTags import TAGS

def picture_metadata(filename : str) -> dict:
    """Lis les métadonnées d'une image

    Args:
        filename (str): Chemin d'accès à l'image

    Returns:
        dict: Dictioanire contenant les métadonnées de l'image
    """
    # read the image data using PIL
    image = Image.open(filename)
    
    # extract EXIF data
    exifdata = image.getexif()
    
    metadata = dict()
    
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        
        metadata[tag] = data
    
    image.close()
    
    return metadata