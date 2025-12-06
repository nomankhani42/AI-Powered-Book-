# Data Model: Initial Project Setup

This document defines the data models for the application.

## Entities

### Book

The collection of all course content in MDX format. This is not a database entity, but a collection of files.

### Chapter

A single MDX file representing a chapter of the book. This is also a file-based entity.

### DocumentChunk

A chunk of text from a chapter, used for ingestion into the vector database.

- **id**: `string` (UUID)
- **chapter_id**: `string` (The path to the chapter file)
- **content**: `string` (The text content of the chunk)
- **vector**: `float[]` (The vector embedding of the content)

### ChatSession

Represents a single chat session.

- **id**: `string` (UUID)
- **created_at**: `datetime`

### ChatMessage

Represents a single message in a chat session.

- **id**: `string` (UUID)
- **session_id**: `string` (Foreign key to ChatSession)
- **role**: `string` ("user" or "assistant")
- **content**: `string` (The message content)
- **created_at**: `datetime`
