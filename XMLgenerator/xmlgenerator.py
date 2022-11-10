from .picture_metadata import picture_metadata
from .xmlwriter import xmlwriter

def xmlgenerator(caracteristics : dict, filename : str):

    metadata = picture_metadata(filename)
    xmlwriter(caracteristics, metadata, filename, '')
    
    return 0