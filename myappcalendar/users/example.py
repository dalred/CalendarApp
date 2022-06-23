# Todo
string_ = '1sssssdaadsasasdsad3wqewqewe4ssss2'
string_list = []
for i in range(len(string_) - 1, -1, -1):
    string_list.append(string_[i])
string_new = ''.join(string_list)
print(string_new)
print(string_[::-1])
