import xml.etree.ElementTree as ET
from pathlib import Path

def xmlwriter(caracteristics : dict, picture_metadata : dict, filename : str, trap_reference : str):
    
    # Checks of values
    
    if 'cast' not in caracteristics:
        caracteristics['cast'] = 'UNDEFINED'
    if 'wingsspacing' not in caracteristics:
        caracteristics['wingsspacing'] = 'UNDEFINED'
    if trap_reference == '':
        trap_reference = 'UNDEFINED'
    if 'DateTime' not in picture_metadata:
        picture_metadata['DateTime'] = 'UNDEFINED'
    
    # Pre-processing of DateTimeOriginal
    
    datetime = picture_metadata['DateTime']
    xmldate = datetime[:10]
    xmltime = datetime[11:]
    
    # Generating the output name
    
    outputname = Path(filename.removeprefix("Footage/")).stem + '.xml'
    
    # XML Formatting, filling and saving
    
    # Main label
    data = ET.Element('data')
    
    # Label for each picture
    picture = ET.SubElement(data, 'picture')
    
    # Labels for the caracteristics
    caracteristics = ET.SubElement(picture, 'item')
    
    cast = ET.SubElement(caracteristics, 'cast') # If determined
    hornetlength = ET.SubElement(caracteristics, 'hornetlength')
    abdomenshape = ET.SubElement(caracteristics, 'abdomenshape')
    wingsspacing = ET.SubElement(caracteristics, 'wingsspacing') # If determined
    
    # Labels for the metadata contained in the picture
    metadata = ET.SubElement(picture, 'item')
    
    date = ET.SubElement(metadata, 'date')
    time = ET.SubElement(metadata, 'time')
    trapreference = ET.SubElement(metadata, 'trapreference') # If given
    # Value for the picture name
    
    picture.text = filename
    
    # Values for the caracteristics
    cast.text = caracteristics['cast']
    hornetlength.text = caracteristics['hornetlength']
    abdomenshape.text = caracteristics['abdomenshape']
    wingsspacing.text = caracteristics['wingsspacing']
    
    # Values for the metadata contained in the picture
    date.text = xmldate
    time.text = xmltime
    trapreference.text = trap_reference
    
    # create a new XML file with the results
    mydata = ET.tostring(data)
    print(mydata)
    myfile = open("Results/" + outputname, "w+")
    myfile.write(str(mydata))
    myfile.close()
    
    return 0