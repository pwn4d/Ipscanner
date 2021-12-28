# IP Scanner

This is a python script for randomly finding IPs and then scanning selected ports on them

## Installation



```bash
python3 setup.py
```

## Usage

```python
python3 ipscanner
```
To randomly generate IPs and scan the first 1000 ports
```python
python3 ipscanner -s 
```
To List All Successfully Found IPs along with the open ports found on those IPs
```python
python3 ipscanner -p 80,21,22
```
To scan custom ports

IP ranges coming soon...

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)