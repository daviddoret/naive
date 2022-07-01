import sys, os

print('set_syspath.py')

package_path = os.path.abspath('..\\src\\naive')

sys.path.insert(0, package_path)

print(f'package_path: {package_path}')
print(f'sys.path: {sys.path}')
print(f'os.getcwd(): {os.getcwd()}')