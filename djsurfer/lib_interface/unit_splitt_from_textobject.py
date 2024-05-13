import os

def split_unit_from_textobject(input_path,output_path):
    """
    For text object which has many repeating substructure containing same pattern of text and data, you can
    use this function to split the substructure into singles text files, each of splitted text files has only
    unit pattern

    Args:
        input_path: path of source file for text object to be splitted
        output_path: file path to store the splitted unit
    """

    # get only input file name from path 'paht/input_file"
    file_name = os.path.basename(input_path)
    #get the input file name without .txt
    input_file_name = os.path.splitext(file_name)[0]
    #print(f'Input file name ist {input_file_name}')

    #open report file
    with open(input_path, "r") as file:
        content =file.read()

    #split report text into text blocks
    units = content.split('Test Results Report')  # units[0] is empty

    for i, unit in enumerate(units[1:]):
        #remove all empty rows and rows beginning with ====
        unit_lines = [line.strip() for line in unit.split('\n') if line.strip() and not line.startswith(' ===')]

        #write the content of each unit into single file in output_path
        if unit_lines:
            #use input file name plus index for output file names to store each single unit
            #linked output path and file name together
            output_file_name = '{}\{}'.format(output_path, f'{input_file_name}_split_{i+1}.txt')
            with open(output_file_name,'w') as file:
                file.write('\n'.join(unit_lines))

    return None


if __name__ == '__main__':
    from pathlib import Path
    #input_path = Path(Path.home, 'Documents\\Python Scripts\\PythonProject_DJSurfer','tests\\demo_data\\217312-0128-15_CELL_Testfile.txt')
    input_path = r'C:\Users\yax3si\Documents\Python Scripts\PythonProject_DJSurfer\tests\demo_data\217312-0128-15_CELL_Testfile.txt'
    output_path= Path(r'C:\Users\yax3si\Documents\Python Scripts\PythonProject_DJSurfer\tests\demo_data', "txt_datapool")
    split_unit_from_textobject(input_path, output_path)