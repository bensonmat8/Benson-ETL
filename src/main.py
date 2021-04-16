import logging

from database import Database

logging.basicConfig(filename='simple_log.log', level="DEBUG")
logger = logging.getLogger(__name__)


class EtlScript:
    def __init__(self):
        self.database_conn = Database("acme")
        # Changing directory structure from
        # './file_name' to '../file_name'
        # as source data is outside main.py folder
        self.header_file = "../headers.txt"
        self.data_file = "../data.csv"
        self.out_file = "../output.csv"

    def load_file_to_database(self, file_path: str):
        self.database_conn.load_file(file_path)

    def column_test(self, header, data):
        '''For now, the the test criteria is to check if 
        the num. of columns in header and num. of columns 
        in the first row of data match. If there are 
        more criterias, it can be added here'''
        test = data.split('\n',1)[0].split('|')
        return len(header) == len(test)

    def run(self):
        # Bringing the header
        with open(self.header_file,'r') as f1:
            header = f1.read().split('\n')

        # Considering edge case where the user
        # might have left few empty lines at the 
        # begining or end of the file
        while header[-1] == '':
            header.pop()
        while header[0] == '':
            header.pop(0) #Pop 0th item
        
        column_name = '|'.join(x for x in header)
        
        # Bringing the data
        with open(self.data_file, 'r') as f2:
            data = f2.read()
        
        # Testing if the num. of columns in header
        # matches the num. of columns in the
        # data file.
        if not self.column_test(header, data):
            # Just logging and returning -1 for now, ideally 
            # emails and messages would be triggered here
            logger.critical(f"Num. of columns do not match in {self.header_file} & {self.data_file}")
            return -1
        
        # Merging column_name and data
        final_data = column_name + '\n' + data
        
        with open(self.out_file, 'w') as f3:
            f3.write(final_data)
        
        # Loading the data to database
        self.load_file_to_database(self.out_file)

if __name__ == "__main__":
    EtlScript().run()
