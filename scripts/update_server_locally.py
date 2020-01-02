from distutils.dir_util import copy_tree

'''this script is used to copy project locally to my server'''

result = copy_tree("D:\\Projects\\denva\\src", "\\ds-lpd-server\\denva\\src")
print(result)