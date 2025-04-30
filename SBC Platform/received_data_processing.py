# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

# Convert String to List
def data_processing(byte_data):
    string_data = byte_data.decode("utf-8").split(';')
    data = []
    for item in string_data:
        data.append(float(item))
    #print('Received Data: ', data)
    return data
