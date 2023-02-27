def test_mop():
    import os
    index=1
    test_dir='test'
    output_dir='output'
    print ('\n')
    files_count=len(os.listdir(test_dir))
    for filename_test in os.listdir(test_dir):
        if index < 10:
            indx='0'+str(index)
        else:
            indx=str(index)
        if filename_test.endswith('.txt'):
            print ('Comparing: ('+indx+'/'+str(files_count)+')',filename_test)
            assert file_dump('./'+test_dir+'/'+filename_test)==file_dump('./'+output_dir+'/'+filename_test)
        else:
            print ('Comparing: ('+indx+'/'+str(files_count)+') Not txt. Skipping file',filename_test)
        index+=1

def file_dump(file):
    with open(file, 'r') as stream:
        text = stream.read()
        return (text)
