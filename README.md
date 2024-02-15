### My Personal Blog

This repository contains the source code for a my personal webpage.

#### Technologies Used:
- **Python 3.11** 
- **Django Framework** 

#### Setup Instructions:
1. Clone the repository to your local machine:
   ```
   git clone https://github.com/BlackstarDamien/my-personal-blog.git
   ```

2. Install the required dependencies:
   ```
   make deps
   ```

3. Apply migrations to set up the database:
   ```
   make migrate
   ```

4. Run the development server:
   ```
   make run-server
   ```

5. Access the blog web page in your browser at `http://127.0.0.1:8000/`.

#### Project Structure:
- **/blog:** Contains the main Django app for the blog functionality.
- **/my_personal_blog:** Contains the Django project folder with settings.py, urls.py, and other project-level configurations.
- **/static:** Holds static files such as CSS, JavaScript, and images.
- **/manage.py:** Entry point for executing Django commands.
- **/requirements.txt:** Lists all dependencies required for the project.

#### License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.