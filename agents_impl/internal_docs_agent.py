from agents import Agent
from agents import function_tool, ModelSettings
import os
from prompts.internal_docs_agent_prompt import INTERNAL_DOCS_AGENT_PROMPT
from configs.configs import INTERNAL_DOCS_AGENT_MODEL, INTERNAL_DOCS_AGENT_TEMPERATURE

# LangChain RAG Pipeline
try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_chroma import Chroma
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    from langchain.chains import RetrievalQA
    from langchain_openai import ChatOpenAI
    
    # Initialize components
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    
    # Load and process setup_phase.md
    def setup_rag_pipeline():
        persist_dir = "./chroma_db_islamic"
        
        # Define multiple files to include in vector DB
        doc_files = [
            {
                "paths": ["../docs/setup_phase.md", "docs/setup_phase.md", "./setup_phase.md"],
                "description": "Z-Inspection methodology and process steps"
            },
            {
                "paths": ["../docs/system_being_analyzed.md", "docs/system_being_analyzed.md", "./system_being_analyzed.md"],
                "description": "Project (under analysis) overview and system description"
            }
        ]
        
        # If chroma_db_fanar doesn't exist, clean up any persistent data first
        if not os.path.exists(persist_dir):
            print(f"🧹 No existing database found - cleaning up any persistent data...")
            
            # Clean up any other potential Chroma persistence locations
            cleanup_dirs = [
                "./chroma_data",
                "./db",
                "./vector_db", 
                "./.chroma",
                "./persist",
                "./.chromadb"
            ]
            
            import shutil
            for cleanup_dir in cleanup_dirs:
                if os.path.exists(cleanup_dir):
                    print(f"   🗑️ Cleaning up: {cleanup_dir}")
                    shutil.rmtree(cleanup_dir)
            
            # Also clean up any .db files or sqlite files that might be lingering
            import glob
            for pattern in ["*.db", "*.sqlite", "*.sqlite3", "./*.chroma*"]:
                for file in glob.glob(pattern):
                    try:
                        os.remove(file)
                        print(f"   🗑️ Removed file: {file}")
                    except:
                        pass
                        
            print(f"✅ Cleanup complete - starting fresh")
            
            # Create new database
            print(f"📖 Creating new vector database...")
            return create_new_database(doc_files, persist_dir)
        
        # Directory exists - try to load existing database
        else:
            print(f"📂 Loading existing vector database from {persist_dir} (current run)")
            try:
                # Try loading with different collection approaches
                vectorstore = None
                collection_count = 0
                
                # Approach 1: Try with specific collection name
                try:
                    vectorstore = Chroma(
                        persist_directory=persist_dir,
                        embedding_function=embeddings,
                        collection_name="z_inspection_docs"
                    )
                    collection_count = vectorstore._collection.count()
                    if collection_count > 0:
                        print(f"✅ Loaded existing database with collection 'z_inspection_docs': {collection_count} document chunks")
                    else:
                        print(f"⚠️ Collection 'z_inspection_docs' found but empty ({collection_count} chunks)")
                        vectorstore = None
                except Exception as e:
                    print(f"⚠️ Failed to load with collection name 'z_inspection_docs': {e}")
                    vectorstore = None
                
                # Approach 2: Try without specifying collection name (use default)
                if vectorstore is None or collection_count == 0:
                    try:
                        vectorstore = Chroma(
                            persist_directory=persist_dir,
                            embedding_function=embeddings
                        )
                        collection_count = vectorstore._collection.count()
                        if collection_count > 0:
                            print(f"✅ Loaded existing database with default collection: {collection_count} document chunks")
                        else:
                            print(f"⚠️ Default collection found but empty ({collection_count} chunks)")
                            vectorstore = None
                    except Exception as e:
                        print(f"⚠️ Failed to load with default collection: {e}")
                        vectorstore = None
                
                # If we have a valid vectorstore with documents, use it
                if vectorstore is not None and collection_count > 0:
                    # Show files in database
                    try:
                        results = vectorstore.get(limit=1000)  # Get all documents
                        unique_files = set()
                        if results and 'metadatas' in results:
                            for metadata in results['metadatas']:
                                if 'source' in metadata:
                                    unique_files.add(metadata['source'])
                        
                        print(f"📚 Database contains {len(unique_files)} files:")
                        for file_path in sorted(unique_files):
                            print(f"   - {file_path}")
                    except Exception as e:
                        print(f"⚠️ Could not list files in database: {e}")
                    
                    # Create QA chain
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=ChatOpenAI(model=INTERNAL_DOCS_AGENT_MODEL),
                        chain_type="stuff",
                        retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
                    )
                    
                    return qa_chain, vectorstore
                else:
                    print(f"❌ No valid documents found in existing database")
                    raise Exception("Empty or corrupted database")
                
            except Exception as e:
                print(f"⚠️ Failed to load existing database: {e}")
                print("🔄 Creating new database...")
                # Clean up corrupted database
                if os.path.exists(persist_dir):
                    import shutil
                    shutil.rmtree(persist_dir)
                
                # Create new database
                return create_new_database(doc_files, persist_dir)
    
    def create_new_database(doc_files, persist_dir):
        """Helper function to create a new vector database"""
        all_documents = []
        processed_files = []
        
        for doc_info in doc_files:
            file_found = False
            for path in doc_info["paths"]:
                if os.path.exists(path):
                    print(f"   📄 Found: {path}")
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                    
                    # Create document with metadata including file modification time
                    import time
                    file_mtime = os.path.getmtime(path)
                    
                    doc = Document(
                        page_content=content, 
                        metadata={
                            "source": path,
                            "description": doc_info["description"],
                            "filename": os.path.basename(path),
                            "last_modified": time.ctime(file_mtime),
                            "mtime": file_mtime,
                            "created_at": time.ctime()
                        }
                    )
                    all_documents.append(doc)
                    processed_files.append(path)
                    file_found = True
                    break
            
            if not file_found:
                print(f"   ⚠️ File not found for: {doc_info['description']}")
        
        if not all_documents:
            raise FileNotFoundError("No documentation files found")
        
        # Split all documents into chunks
        chunks = text_splitter.split_documents(all_documents)
        
        # Create vector store with simple, consistent collection name
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings,
            persist_directory=persist_dir,
            collection_name="z_inspection_docs"  # Fixed collection name
        )
        
        # Note: Newer Chroma versions auto-persist when persist_directory is specified
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model=INTERNAL_DOCS_AGENT_MODEL),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
        print(f"✅ Created new database:")
        print(f"   📊 {len(processed_files)} files processed")
        print(f"   📋 {len(chunks)} total chunks created")
        print(f"   🆔 Collection: z_inspection_docs")
        for file_path in processed_files:
            print(f"   - {file_path}")
        
        return qa_chain, vectorstore

    # Initialize RAG system
    qa_chain, vectorstore = setup_rag_pipeline()
    RAG_AVAILABLE = True
    
except Exception as e:
    print(f"RAG setup failed: {e}")
    RAG_AVAILABLE = False
    
    # Fallback to simple file reading - try multiple paths
    setup_phase_docs = "Z-Inspection documentation not available."
    fallback_paths = ["docs/setup_phase.md", "../docs/setup_phase.md", "./setup_phase.md"]
    
    for path in fallback_paths:
        try:
            with open(path, "r") as file:
                setup_phase_docs = file.read()
                print(f"✅ Loaded fallback documentation from: {path}")
                break
        except FileNotFoundError:
            continue
    
    if setup_phase_docs == "Z-Inspection documentation not available.":
        print("⚠️ No documentation files found for fallback")

@function_tool
async def search_internal_docs(query: str) -> str:
    """Search internal documentation using RAG or fallback to full text."""
    if RAG_AVAILABLE:
        try:
            result = qa_chain.invoke(query)
            return result
        except Exception as e:
            return f"RAG search failed: {e}. Using fallback."
    
    return setup_phase_docs

@function_tool
async def get_database_info() -> str:
    """Get information about the vector database contents."""
    if not RAG_AVAILABLE:
        return "Vector database not available. Using fallback text search."
    
    try:
        # Get database stats
        collection_count = vectorstore._collection.count()
        
        # Get all documents to analyze
        results = vectorstore.get(limit=1000)
        
        files_info = {}
        if results and 'metadatas' in results:
            for metadata in results['metadatas']:
                source = metadata.get('source', 'unknown')
                description = metadata.get('description', 'No description')
                filename = metadata.get('filename', os.path.basename(source))
                last_modified = metadata.get('last_modified', 'Unknown')
                
                if source not in files_info:
                    files_info[source] = {
                        'filename': filename,
                        'description': description,
                        'last_modified': last_modified,
                        'chunks': 0
                    }
                files_info[source]['chunks'] += 1
        
        # Format response
        response = f"📊 **Vector Database Information**\n\n"
        response += f"**Total chunks:** {collection_count}\n"
        response += f"**Number of files:** {len(files_info)}\n\n"
        
        if files_info:
            response += "**Files in database:**\n"
            for source, info in files_info.items():
                response += f"- **{info['filename']}** ({info['chunks']} chunks)\n"
                response += f"  *{info['description']}*\n"
                response += f"  *Last modified: {info['last_modified']}*\n\n"
        
        return response
        
    except Exception as e:
        return f"Error getting database info: {e}"


internal_docs_agent = Agent(
    name="Internal Docs Agent",
    model=INTERNAL_DOCS_AGENT_MODEL,
    instructions=INTERNAL_DOCS_AGENT_PROMPT,
    tools=[search_internal_docs, get_database_info],
    model_settings=ModelSettings(
        temperature=INTERNAL_DOCS_AGENT_TEMPERATURE,
    ),
)
