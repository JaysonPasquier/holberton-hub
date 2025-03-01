# Holberton Hub - Job Platform

A Django-based platform for posting projects/jobs and finding collaborators.

## Features

- User Authentication and Profiles
- Create and Manage Job Postings
- Apply to Jobs
- Accept/Reject Applications
- Responsive Design with Bootstrap

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd holberton-hub-new-version
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## Project Structure

- `holberton_hub/` - Main project settings
- `users/` - User authentication and profile management
- `jobs/` - Job posting, application, and management

## License

This project is licensed under the MIT License.
