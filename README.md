[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=Python&logoColor=yellow)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-7.2.5-DC382D?style=flat&logo=Redis&logoColor=white)](https://redis.io/)
[![Flake8](https://img.shields.io/badge/flake8-checked-blueviolet?style=flat)](https://flake8.pycqa.org/en/latest/)
[![isort](https://img.shields.io/badge/isort-checked-violet?style=flat)](https://pycqa.github.io/isort/)

# JornalY

### Table of contents:
- [Project Description](#Project-Description)
- [Getting Started](#Getting-Started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Project Description
***Built with Django 5, this web application offers robust functionality for managing users, posts, and social interactions. 
Key features include:***

**User Management**
 - User Creation: Users can create an account and log in.
 - Password Management: Users can change their passwords and recover their passwords via email.
 - User Profile: Each user has a profile page that displays all of their posts.

**Post Management**
 - Create Posts: Users can create new posts and attach images to them.
 - Edit Posts: Authors can edit the content of their own posts.
 - Comments: Users can add comments to posts.

**Social Features**
 - Subscriptions: Users can subscribe to and unsubscribe from other authors to follow their posts.

**Testing**
 - All features have been thoroughly tested to ensure reliability and functionality.


## Getting Started
**To get started with the project, follow these steps:**
1. Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/dev-lymar/JornalY.git
cd JornalY
```
2. Configure .env
```sh
replace env.example with your data
```
3. Set Up a Virtual Environment on your machine


4. Install the required dependencies:
 ```sh
pip install -r requirements.txt
```
5. Run migrations:
```sh
python manage.py migrate
```
6. Create a superuser:
```sh
python manage.py createsuperuser
```
7. Run the development server:
```sh
python manage.py runserver
```

## Usage

Once the development server is running, you can access the application at http://127.0.0.1:8000/. 
From there, you can create a user account, log in, create posts, follow other authors, and more.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. 
For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the LICENSE file for details.