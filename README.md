# Django Comments System
___

[Link](https://sergey-ch-comments.onrender.com/) to deployed project (on Render)  

## Project Description

This project is a Django-based comments management system with file attachments and HTML formatting support. It provides a robust system for managing user comments with secure file handling, nested replies, and XSS protection.

### Key Features
- File attachments support (images and text files)
- Nested comments system
- HTML formatting with security sanitization
- Pagination and sorting functionality
- Automatic image resizing
- XSS protection

## Prerequisites
Before running the project, ensure you have:
- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sergey-Chalyi/django_CommentsSite.git
   cd django_CommentsSite
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure media settings in settings.py:
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```


5. Apply database migrations:
   ```bash
   cd base
   python manage.py migrate
   ```

## Running the Project
1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application:
   - Comments List: `http://localhost:8000/comments/`
   - Add Comment: `http://localhost:8000/comments-create/`

## Documentation

### Models

#### Comment Model
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| user_name | CharField | User's name | Required |
| email | EmailField | User's email | Required, validated |
| text | TextField | Comment content | Required, HTML sanitized |
| attachment | FileField | File attachment | Optional, validated |
| parent_comment | ForeignKey | Reference to parent comment | Optional |
| time_created | DateTimeField | Creation timestamp | Auto-generated |

### File Attachments

#### Text Files
| Parameter | Value |
|-----------|-------|
| Format | .txt only |
| Max Size | 100KB |

#### Images
| Parameter | Value |
|-----------|-------|
| Formats | JPG, JPEG, PNG, GIF |
| Max Dimensions | 320x240px |
| Optimization | Quality 95%, auto-resize |

### HTML Formatting
Allowed HTML tags:

| Tag | Attributes |
|-----|------------|
| a | href, title |
| code | none |
| i | none |
| strong | none |


Supports sorting by:

| Parameter | Description |
|-----------|-------------|
| sort_by | Field to sort by (default: time_created) |
| order | Sort order (asc/desc, default: desc) |

## Development

### Requirements
```
Django==5.1.3
Pillow==11.0.0
bleach==6.2.0
lxml==5.3.0
```

### Security Features
- Email validation
- File type validation
- File size limits
- Image dimension restrictions
- HTML sanitization
- XSS protection
- CSRF protection

## Contact
Email: ch.sergey.rb@gmail.com
