import os
os.system('pip install -r requirements.txt')
os.system('sudo chmod +x ipscanner.py')
os.system('sudo mv ipscanner.py ipscanner')
os.system('sudo mv ipscanner.py /usr/bin')
print('Finished installation!')
