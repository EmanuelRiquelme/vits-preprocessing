import argparse
parser = argparse.ArgumentParser(description='Create training and testing files.')
parser.add_argument('--train_size', type=int, default= 90, help='Percentage of data for training')
parser.add_argument('--test_size', type=int, default= 10, help='Percentage of data for testing')
parser.add_argument('--data_dir', type=str, default='dataset', help='Directory that contains the data')

def write_file(txt_file,lines):
    f = open(txt_file, 'w+')
    f.write(lines)
    f.close()

def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

def get_data_split(name_file,train_size,test_size):
    total_size = count_lines(name_file)
    train_size = int(total_size*train_size/100)
    test_size  = total_size-train_size
    return train_size,test_size

def write_list_to_file(file_path, my_list):
    with open(file_path, 'w') as file:
        for item in my_list:
            file.write(str(item) + '\n')
def get_lines(name_file):
    with open(name_file, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

if __name__ == '__main__':
    args = parser.parse_args()
    name_file = f'{args.data_dir}/data.txt'
    test_file = f'{args.data_dir}/test.txt'
    train_file = f'{args.data_dir}/train.txt'
    train_size,test_size =  get_data_split(name_file,args.train_size,args.test_size)
    list_data = get_lines(name_file)
    test_data = list_data[:test_size]
    write_list_to_file(test_file,test_data)
    train_data = list_data[-train_size:]
    write_list_to_file(train_file,train_data)
    print('Data split succesfully!')
