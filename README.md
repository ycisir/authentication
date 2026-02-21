# custom authentication function based
A custom function based authentication system build using Django.

### prerequisites
- uv package manager
- python3.12


### local dev setup
```
git clone https://github.com/ycisir/custom-auth-fbv.git
cd custom-auth-fbv
uv sync 
uv run manage.py makemigrations 
uv run manage.py migrate 
uv run manage.py runserver
```