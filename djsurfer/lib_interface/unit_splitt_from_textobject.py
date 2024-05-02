import os

def splitt_unit_from_textobject(path):
    """
    For text object which has many repeating substructure containing same pattern of text and data, you can
    use this function to splitt the substructure into singles text files, each of splitted text files has only
    unit pattern

    Args:
        input_path: file path for text object to be splitted
        output_path: file path to store the splitted unit
    """

    #open report file
    with open(input_path, "r") as file:
        content =file.read()

    #split report text into text blocks
    units = content.split('Test Results Report')  # blocks[0] is empty
    #print(units[1])

    for unit in units[1:]:
        #Todo:
        #write content unit to single file in output_path



if __name__ = '__main__':
    from pathlib import Path
    input_path = Path(__file__).parent/r'..\..\tests\demo_data\217312-0128-15_CELL_Testfile.txt'z
    output_path= Path(__file__).parent/r'..\..\tests\demo_data\txt_datapool\'
    splitt_unit_from_textobject(input_path, output_path)


