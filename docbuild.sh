#!/bin/bash
# Generate DocString HTML

cd Documentation/
sphinx-apidoc -f -o . ../​
make html

#End of bash

