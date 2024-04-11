# PICO-LIBRARY API DOCUMENTATION

## Overview

This API provides endpoints for managing subjects, books, comments, bookshelves, resources, languages, publishers, bookmarks, and user profiles. It utilizes JWT-based authentication for secure access.

## Authentication

To authenticate and obtain a JWT token, use the following endpoint:


- **Endpoint:** `/auth/login`
- **Method:** POST
- **Description:** Authenticate user credentials and generate a JWT token.
- **Parameters:**
  - `email` (required): User's email address
  - `password` (required): User's password
- **Response:**
  - `token`: JWT token for accessing protected endpoints


---

### Logout
- **Endpoint:** `/api/v1/auth/logout`
- **Method:** POST
- **Description:** Invalidate JWT token.

### Refresh Token
- **Endpoint:** `/api/v1/auth/refresh`
- **Method:** POST
- **Description:** Refresh JWT token.

### Register
- **Endpoint:** `/api/v1/auth/register`
- **Method:** POST
- **Description:** Register a new user.
- **Request Body:**
  - `email`: User email
  - `password`: User password

### Change Password
- **Endpoint:** `/api/v1/auth/change_password`
- **Method:** POST
- **Description:** Change user password.
- **Request Body:**
  - `old_password`: User's current password
  - `new_password`: User's new password


---

# API Endpoints

## Books

### Get All Books
- **Endpoint:** `/api/v1/books/`
- **Method:** GET
- **Description:** Retrieve all books.

### Get Book by ID
- **Endpoint:** `/api/v1/books/<book_id>`
- **Method:** GET
- **Description:** Retrieve a specific book by its ID.

### Create Book
- **Endpoint:** `/api/v1/books/`
- **Method:** POST
- **Description:** Create a new book.
- **Request Body:** JSON object containing book details.

### Update Book
- **Endpoint:** `/api/v1/books/<book_id>`
- **Method:** PUT
- **Description:** Update an existing book by its ID.
- **Request Body:** JSON object containing updated book details.

### Delete Book
- **Endpoint:** `/api/v1/books/<book_id>`
- **Method:** DELETE
- **Description:** Delete a book by its ID.

---

## Book Recommendations

### Get Book Recommendations
- **Endpoint:** `/api/v1/books/recommendations`
- **Method:** GET
- **Description:** Retrieve recommended books based on user preferences or system algorithms.

---

## Book Search

### Search Books
- **Endpoint:** `/api/v1/books/search`
- **Method:** GET
- **Description:** Search for books by title, author, or other criteria.

---



---

## Subjects

### Get Subjects

- **Endpoint:** `/subjects/`
- **Method:** GET
- **Description:** Retrieve a list of subjects.
- **Parameters:**
  - `page` (optional): Page number (default: 1)
  - `per_page` (optional): Number of items per page (default: 10, options: 5, 10, 25, 50, 100)

### Create Subject

- **Endpoint:** `/subjects/`
- **Method:** POST
- **Description:** Create a new subject.
- **Parameters:**
  - `name` (required): Name of the subject
  - `score` (optional): Score of the subject

### Get Subject

- **Endpoint:** `/subjects/{subject_id}`
- **Method:** GET
- **Description:** Retrieve details of a specific subject.
- **Parameters:**
  - `subject_id` (required): ID of the subject

### Delete Subject

- **Endpoint:** `/subjects/{subject_id}`
- **Method:** DELETE
- **Description:** Delete a specific subject.
- **Parameters:**
  - `subject_id` (required): ID of the subject

### Update Subject

- **Endpoint:** `/subjects/{subject_id}`
- **Method:** PUT
- **Description:** Update details of a specific subject.
- **Parameters:**
  - `subject_id` (required): ID of the subject
  - `name` (optional): New name of the subject
  - `score` (optional): New score of the subject

---

## Comments

### Get All Comments
- **Endpoint:** `/api/v1/comments/`
- **Method:** GET
- **Description:** Retrieve all comments.

### Get Comment by ID
- **Endpoint:** `/api/v1/comments/<comment_id>`
- **Method:** GET
- **Description:** Retrieve a specific comment by its ID.

### Create Comment
- **Endpoint:** `/api/v1/comments/`
- **Method:** POST
- **Description:** Create a new comment.
- **Request Body:** JSON object containing comment details.

### Update Comment
- **Endpoint:** `/api/v1/comments/<comment_id>`
- **Method:** PUT
- **Description:** Update an existing comment by its ID.
- **Request Body:** JSON object containing updated comment details.

### Delete Comment
- **Endpoint:** `/api/v1/comments/<comment_id>`
- **Method:** DELETE
- **Description:** Delete a comment by its ID.

---

## Bookshelves

### Get All Bookshelves
- **Endpoint:** `/api/v1/bookshelves/`
- **Method:** GET
- **Description:** Retrieve all bookshelves.

### Get Bookshelf by ID
- **Endpoint:** `/api/v1/bookshelves/<bookshelf_id>`
- **Method:** GET
- **Description:** Retrieve a specific bookshelf by its ID.

### Create Bookshelf
- **Endpoint:** `/api/v1/bookshelves/`
- **Method:** POST
- **Description:** Create a new bookshelf.
- **Request Body:** JSON object containing bookshelf details.

### Update Bookshelf
- **Endpoint:** `/api/v1/bookshelves/<bookshelf_id>`
- **Method:** PUT
- **Description:** Update an existing bookshelf by its ID.
- **Request Body:** JSON object containing updated bookshelf details.

### Delete Bookshelf
- **Endpoint:** `/api/v1/bookshelves/<bookshelf_id>`
- **Method:** DELETE
- **Description:** Delete a bookshelf by its ID.

### Get Books in Bookshelf
- **Endpoint:** `/api/v1/bookshelves/<bookshelf_id>/books`
- **Method:** GET
- **Description:** Retrieve all books in a specific bookshelf by its ID.

### Add Book to Bookshelf
- **Endpoint:** `/api/v1/bookshelves/<bookshelf_id>/books/<book_id>`
- **Method:** POST
- **Description:** Add a book to a specific bookshelf.
- **Parameters:** `bookshelf_id` - The ID of the bookshelf; `book_id` - The ID of the book to add.

### Remove Book from Bookshelf
- **Endpoint:** `/api/v1/bookshelves/<bookshelf_id>/books/<book_id>`
- **Method:** DELETE
- **Description:** Remove a book from a specific bookshelf.
- **Parameters:** `bookshelf_id` - The ID of the bookshelf; `book_id` - The ID of the book to remove.

---

## Resources

### Get All Resources
- **Endpoint:** `/api/v1/resources/`
- **Method:** GET
- **Description:** Retrieve all resources.

### Get Resource by ID
- **Endpoint:** `/api/v1/resources/resource/<resource_id>`
- **Method:** GET
- **Description:** Retrieve a specific resource by its ID.

### Create Resource
- **Endpoint:** `/api/v1/resources/`
- **Method:** POST
- **Description:** Create a new resource.
- **Request Body:** JSON object containing resource details.

### Update Resource
- **Endpoint:** `/api/v1/resources/resource/<resource_id>`
- **Method:** PUT
- **Description:** Update an existing resource by its ID.
- **Request Body:** JSON object containing updated resource details.

### Delete Resource
- **Endpoint:** `/api/v1/resources/resource/<resource_id>`
- **Method:** DELETE
- **Description:** Delete a resource by its ID.

---

## Languages

### Get All Languages
- **Endpoint:** `/api/v1/languages/`
- **Method:** GET
- **Description:** Retrieve all languages.

### Get Language by ID
- **Endpoint:** `/api/v1/languages/<language_id>`
- **Method:** GET
- **Description:** Retrieve a specific language by its ID.

### Create Language
- **Endpoint:** `/api/v1/languages/`
- **Method:** POST
- **Description:** Create a new language.
- **Request Body:** JSON object containing language details.

### Update Language
- **Endpoint:** `/api/v1/languages/<language_id>`
- **Method:** PUT
- **Description:** Update an existing language by its ID.
- **Request Body:** JSON object containing updated language details.

### Delete Language
- **Endpoint:** `/api/v1/languages/<language_id>`
- **Method:** DELETE
- **Description:** Delete a language by its ID.

---

## Publishers

### Get All Publishers
- **Endpoint:** `/api/v1/publishers/`
- **Method:** GET
- **Description:** Retrieve all publishers.

### Get Publisher by ID
- **Endpoint:** `/api/v1/publishers/<publisher_id>`
- **Method:** GET
- **Description:** Retrieve a specific publisher by its ID.

### Create Publisher
- **Endpoint:** `/api/v1/publishers/`
- **Method:** POST
- **Description:** Create a new publisher.
- **Request Body:** JSON object containing publisher details.

### Update Publisher
- **Endpoint:** `/api/v1/publishers/<publisher_id>`
- **Method:** PUT
- **Description:** Update an existing publisher by its ID.
- **Request Body:** JSON object containing updated publisher details.

### Delete Publisher
- **Endpoint:** `/api/v1/publishers/<publisher_id>`
- **Method:** DELETE
- **Description:** Delete a publisher by its ID.

---

## Bookmarks

### Get All Bookmarks
- **Endpoint:** `/api/v1/bookmarks/`
- **Method:** GET
- **Description:** Retrieve all bookmarks.

### Get Bookmark by ID
- **Endpoint:** `/api/v1/bookmarks/<bookmark_id>`
- **Method:** GET
- **Description:** Retrieve a specific bookmark by its ID.

### Create Bookmark
- **Endpoint:** `/api/v1/bookmarks/`
- **Method:** POST
- **Description:** Create a new bookmark.
- **Request Body:** JSON object containing bookmark details.

### Update Bookmark
- **Endpoint:** `/api/v1/bookmarks/<bookmark_id>`
- **Method:** PUT
- **Description:** Update an existing bookmark by its ID.
- **Request Body:** JSON object containing updated bookmark details.

### Delete Bookmark
- **Endpoint:** `/api/v1/bookmarks/<bookmark_id>`
- **Method:** DELETE
- **Description:** Delete a bookmark by its ID.

---

## User Profiles

### Get User Profile
- **Endpoint:** `/api/v1/user/profile`
- **Method:** GET
- **Description:** Retrieve the profile of the authenticated user.

### Update User Profile
- **Endpoint:** `/api/v1/user/profile`
- **Method:** PUT
- **Description:** Update the profile of the authenticated user.
- **Request Body:** JSON object containing updated user profile details.

---

