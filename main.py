import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import db, create_document, get_documents

from schemas import Company, Contact, Deal, Project, Task

app = FastAPI(title="Task Manager & CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Task Manager & CRM Backend is running"}

# ---------- CRM ENDPOINTS ----------

@app.post("/api/companies")
def create_company(company: Company):
    try:
        inserted_id = create_document("company", company)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/companies")
def list_companies(limit: Optional[int] = 50):
    try:
        companies = get_documents("company", {}, limit)
        for c in companies:
            c["_id"] = str(c["_id"])  # serialize
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contacts")
def create_contact(contact: Contact):
    try:
        inserted_id = create_document("contact", contact)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contacts")
def list_contacts(limit: Optional[int] = 50):
    try:
        contacts = get_documents("contact", {}, limit)
        for c in contacts:
            c["_id"] = str(c["_id"])  # serialize
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/deals")
def create_deal(deal: Deal):
    try:
        inserted_id = create_document("deal", deal)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/deals")
def list_deals(limit: Optional[int] = 50):
    try:
        deals = get_documents("deal", {}, limit)
        for d in deals:
            d["_id"] = str(d["_id"])  # serialize
        return deals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- TASK MANAGEMENT ENDPOINTS ----------

@app.post("/api/projects")
def create_project(project: Project):
    try:
        inserted_id = create_document("project", project)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
def list_projects(limit: Optional[int] = 50):
    try:
        projects = get_documents("project", {}, limit)
        for p in projects:
            p["_id"] = str(p["_id"])  # serialize
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tasks")
def create_task(task: Task):
    try:
        inserted_id = create_document("task", task)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks")
def list_tasks(limit: Optional[int] = 50, status: Optional[str] = None):
    try:
        filter_dict = {"status": status} if status else {}
        tasks = get_documents("task", filter_dict, limit)
        for t in tasks:
            t["_id"] = str(t["_id"])  # serialize
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
