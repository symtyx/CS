def getauthors (filename1,filename2):
    authors = ''

    everything = filename1.read()
    words = everthing.split()
    
    for index in range(len(words)):
         if words[index] == "AUTHORS":
             start_index = index
        elif words[index] == "TITLE":
        end_index = index
             return authors
