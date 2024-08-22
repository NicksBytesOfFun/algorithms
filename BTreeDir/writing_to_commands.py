if __name__ == '__main__':
    file1 = open("dictionary.txt")
    file2 = open("commands.txt", 'w')
    lines = file1.readlines()
    for line in lines:
        file2.write("delete " + line.strip())
        file2.write("\n")
    file1.close()
    file2.close()
