from .picture_metadata import picture_metadata
from .xmlwriter import xmlwriter

def xmlgenerator(caracteristics : dict, filename : str, trap_reference : str = '') -> int:

    metadata = picture_metadata(filename)
    xmlwriter(caracteristics, metadata, filename, trap_reference)
    
    return 0