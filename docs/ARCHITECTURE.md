# Architecture & Design Decisions

## Overview

This document outlines the architecture, design decisions, and implementation approaches for the Supabase haiku storage integration feature. The implementation follows modern Python development patterns with a focus on maintainability, testability, and scalability.

## 🏗️ Architecture Patterns

### Repository Pattern

**Purpose**: Isolates database operations from business logic, making it easy to swap data sources.

**Implementation**: `repository.py`
```python
class HaikuRepository:
    def __init__(self, supabase_client: Client, table_name: str = "haikus"):
        self.client = supabase_client
        self.table_name = table_name

    def save(self, haiku: Haiku) -> Haiku:
        # Database-specific implementation
```

**Benefits**:
- Clean separation of data access concerns
- Easy to mock for testing
- Database-agnostic business logic
- Single responsibility principle

### Service Layer Pattern

**Purpose**: Encapsulates business logic and provides a clean interface for the UI layer.

**Implementation**: `haiku_storage_service.py`
```python
class HaikuStorageService:
    def __init__(self, supabase_url: str, supabase_key: str):
        self._client: Optional[Client] = None
        self._repository: Optional[HaikuRepository] = None

    def save_haiku(self, subject: str, haiku_text: str, user_id: Optional[str] = None) -> Optional[Haiku]:
        # Business logic and error handling
```

**Benefits**:
- Centralized business rules
- Error handling and logging
- Caching and optimization
- Clean API for UI layer

### Data Models with Dataclasses

**Purpose**: Type-safe data structures with built-in serialization.

**Implementation**: `models.py`
```python
@dataclass
class Haiku:
    id: str
    subject: str
    haiku_text: str
    created_at: datetime
    user_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Haiku":
        # Deserialization logic

    def to_dict(self) -> Dict[str, Any]:
        # Serialization logic
```

**Benefits**:
- Type safety and IDE support
- Automatic serialization/deserialization
- Immutable data structures
- Clear data contracts

## 🎨 UI Architecture

### Streamlit Sidebar Integration

**Design Decision**: Use Streamlit's native sidebar for haiku history to maintain consistency with the framework.

**Implementation Approach**:
```python
with st.sidebar:
    st.markdown("### 🍃 Haiku History")

    # Search functionality
    search_query = st.text_input("Search by subject", key="search_query")

    # Display haikus
    if search_query:
        haikus = storage_service.search_haikus(search_query)
    else:
        haikus = storage_service.get_recent_haikus()

    for haiku in haikus:
        render_haiku_card(haiku)
```

**Key Features**:
- **Real-time Search**: Filter haikus by subject as you type
- **Auto-refresh**: Sidebar updates immediately after generation
- **Glassmorphism Design**: Consistent with main UI aesthetic
- **Responsive Cards**: Each haiku displayed in a styled card

### CSS Architecture

**Design Decision**: Use custom CSS with `!important` overrides to ensure consistent styling across themes.

**Implementation**:
```css
.stSidebar .haiku-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.8) 100%);
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(99, 102, 241, 0.2);
}
```

**Benefits**:
- Consistent visual design
- Theme-independent styling
- Modern glassmorphism effects
- Mobile-responsive design

## 🔄 Data Flow Architecture

### Auto-Save Implementation

**Design Decision**: Automatically save haikus after generation to provide seamless user experience.

**Flow**:
1. User generates haiku
2. Haiku displayed in main area
3. Auto-save triggered in background
4. Success message shown to user
5. Sidebar refreshed to show new haiku

**Implementation**:
```python
if submitted:
    poem = generate_poem(subject)
    st.session_state["generated_poem"] = poem

    # Auto-save with error handling
    if storage_service and storage_service.is_available():
        saved_haiku = storage_service.save_haiku(subject, poem)
        if saved_haiku:
            st.success("✨ Haiku saved to history!")
            st.rerun()  # Refresh sidebar
```

### Error Handling Strategy

**Design Decision**: Graceful degradation - app works with or without Supabase.

**Implementation**:
```python
def get_storage_service() -> HaikuStorageService | None:
    """Create a haiku storage service if Supabase is configured."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        return None

    try:
        return HaikuStorageService(supabase_url, supabase_key)
    except Exception:
        return None
```

**Benefits**:
- No blocking errors for missing credentials
- App continues to work in degraded mode
- Clear user feedback about storage status
- Easy to debug configuration issues

## 🧪 Testing Architecture

### Test Data Management

**Design Decision**: Automatic cleanup of test data to prevent database pollution.

**Implementation**:
```python
@pytest.fixture(autouse=True)
def cleanup_test_data(self, storage_service, test_haiku_ids):
    """Automatically clean up test data after each test."""
    yield  # Run the test
    # Cleanup after test completes
    if test_haiku_ids and storage_service.is_available():
        for haiku_id in test_haiku_ids:
            storage_service.client.table("haikus").delete().eq("id", haiku_id).execute()
```

**Benefits**:
- Clean database state for each test
- No manual cleanup required
- Reliable test isolation
- Prevents test data pollution

### Test Categories

1. **Unit Tests** (`test_repository.py`, `test_haiku_storage_service.py`)
   - Mock external dependencies
   - Fast execution
   - Isolated testing

2. **Integration Tests** (`test_supabase_integration.py`)
   - Real Supabase database
   - End-to-end data flow
   - Automatic cleanup

3. **UI Tests** (`test_streamlit_app.py`)
   - Streamlit component testing
   - User interaction simulation
   - Mocked dependencies

## 🔧 Configuration Management

### Environment Variables

**Design Decision**: Use `.env` file for configuration with graceful fallbacks.

**Implementation**:
```python
# Load environment variables
load_dotenv()

# Check for required credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    return None  # Graceful degradation
```

**Benefits**:
- Easy configuration management
- Secure credential handling
- Environment-specific settings
- Clear error messages

### Database Schema Design

**Design Decision**: Simple, extensible schema with proper indexing.

**SQL Schema**:
```sql
CREATE TABLE haikus (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  subject TEXT NOT NULL,
  haiku_text TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  user_id UUID
);

CREATE INDEX idx_haikus_created_at ON haikus(created_at DESC);
CREATE INDEX idx_haikus_subject ON haikus(subject);
```

**Benefits**:
- Fast chronological queries
- Efficient subject search
- Future-ready for user authentication
- Simple data model

## 🚀 Performance Considerations

### Lazy Loading

**Implementation**: Repository and service instances are created only when needed.

```python
@property
def repository(self) -> HaikuRepository:
    if self._repository is None:
        self._repository = HaikuRepository(self.client)
    return self._repository
```

### Connection Pooling

**Implementation**: Supabase client handles connection pooling automatically.

### Caching Strategy

**Implementation**: Service layer caches repository instances to avoid recreation.

## 🔒 Security Considerations

### API Key Management

- Environment variables for sensitive data
- No hardcoded credentials
- Graceful handling of missing keys

### Data Validation

- Input sanitization in service layer
- Type checking with dataclasses
- SQL injection prevention via Supabase client

### Error Handling

- No sensitive information in error messages
- Proper logging for debugging
- User-friendly error messages

## 📈 Scalability Considerations

### Database Scaling

- Supabase handles database scaling automatically
- Proper indexing for query performance
- Connection pooling for concurrent users

### Code Organization

- Modular architecture for easy maintenance
- Clear separation of concerns
- Testable components

### Future Enhancements

- User authentication ready (user_id field)
- Easy to add new data fields
- Repository pattern allows database migration

## 🎯 Key Design Decisions Summary

1. **Repository Pattern**: Clean data access layer
2. **Service Layer**: Business logic encapsulation
3. **Graceful Degradation**: Works with/without Supabase
4. **Auto-cleanup Tests**: No database pollution
5. **Glassmorphism UI**: Consistent modern design
6. **Type Safety**: Dataclasses for data models
7. **Error Handling**: User-friendly error messages
8. **Configuration**: Environment-based setup

This architecture provides a solid foundation for the haiku storage feature while maintaining code quality, testability, and user experience.
