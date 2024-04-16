# PICO-LIBRARY API DOCUMENTATION

## Overview

This API provides endpoints for managing subjects, books, comments, bookshelves, resources, languages, publishers, bookmarks, and user profiles. It utilizes JWT-based authentication for secure access.

## Authentication

To authenticate and obtain a JWT token, use the following endpoint:

- **Endpoint:** `/api/v1/auth/login`
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
- **Method:** PUT
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

## Subjects

### Get Subjects

- **Endpoint:** `/api/v1/subjects/`
- **Method:** GET
- **Description:** Retrieve a list of subjects.

### Create Subject

- **Endpoint:** `/api/v1/subjects/`
- **Method:** POST
- **Description:** Create a new subject.
- **Request Body:** JSON object containing subject details.

### Get Subject

- **Endpoint:** `/api/v1/subjects/{subject_id}`
- **Method:** GET
- **Description:** Retrieve details of a specific subject.

### Delete Subject

- **Endpoint:** `/api/v1/subjects/{subject_id}`
- **Method:** DELETE
- **Description:** Delete a specific subject.

### Update Subject

- **Endpoint:** `/api/v1/subjects/{subject_id}`
- **Method:** PUT
- **Description:** Update details of a specific subject.

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
- **Description:** Update an existing language by its

 ID.
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

