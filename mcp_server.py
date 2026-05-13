from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# A tool to read a doc
@mcp.tool(
    name="read_doc_content",
    description="Read the full content of a document by its filename. Use this when the user asks about a specific document."
)

def read_doc_content(doc_id: str = Field(description="The filename of the document, e.g. 'deposition.md' or 'report.pdf'")):
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")
    return docs[doc_id]

# A tool to edit a doc
@mcp.tool(
    name="edit_doc_content", 
    description="Edit a document by replacing specific text. Use this when the user wants to update or change content within a document."
)

def edit_doc_content(
    doc_id: str = Field(description="The filename of the document to be edited"),
    old_str: str = Field(description="The exact text currently in the document that needs to be replaced. Must match the document content exactly, including capitalisation."),
    new_str: str = Field(description="The new text to substitute in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")
    if old_str not in docs[doc_id]:
        raise ValueError(f"Text '{old_str}' not found in {doc_id}")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str, 1)
    return docs[doc_id]



# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
