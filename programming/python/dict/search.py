# # response['Labels']をlabelに格納し、label['Name]に'Cat'か'Dog'があったらlabel['Name']の値をanimal_typesに格納する
# animal_types = [label['Name'] for label in response['Labels'] if 'Cat' in label['Name'] or 'Dog' in label['Name']]


d = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

print('key1' in d.keys())
# True

print('val1' in d.values())
# True

print(d.get('key1'))
# val1

print(d.get('key4'))
# None

