from langchain_text_splitters import RecursiveCharacterTextSplitter

#split the document into chunks using recursive character text splitter or normal text splitter
def split_document(document, chunk_size, chunk_overlap):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    print("textsplitter loaded successfully!!")
    chunks=text_splitter.split_documents([document])

    if chunks:
        print(f"Document split into {len(chunks)} chunks.")
    return chunks