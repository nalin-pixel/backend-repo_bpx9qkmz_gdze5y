"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# CRM ENTITIES

class Company(BaseModel):
    name: str = Field(..., description="Company name")
    website: Optional[str] = Field(None, description="Company website")
    industry: Optional[str] = Field(None, description="Industry")
    size: Optional[str] = Field(None, description="Company size (e.g., 11-50)")
    phone: Optional[str] = Field(None, description="Main phone number")
    address: Optional[str] = Field(None, description="Address")
    notes: Optional[str] = Field(None, description="Internal notes")

class Contact(BaseModel):
    name: str = Field(..., description="Full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    title: Optional[str] = Field(None, description="Job title")
    company_id: Optional[str] = Field(None, description="Related company id")
    tags: List[str] = Field(default_factory=list, description="Tags")
    status: str = Field("active", description="Status")
    notes: Optional[str] = Field(None, description="Notes")

class Deal(BaseModel):
    title: str = Field(..., description="Deal title")
    value: float = Field(0.0, ge=0, description="Deal value")
    stage: str = Field("new", description="Pipeline stage")
    contact_id: Optional[str] = Field(None, description="Primary contact id")
    company_id: Optional[str] = Field(None, description="Company id")
    probability: Optional[int] = Field(50, ge=0, le=100, description="Win probability (%)")
    close_date: Optional[date] = Field(None, description="Expected close date")

# TASK/PROJECT MANAGEMENT

class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    owner_id: Optional[str] = Field(None, description="Owner user id")
    members: List[str] = Field(default_factory=list, description="Member user ids")
    status: str = Field("active", description="Project status")
    progress: int = Field(0, ge=0, le=100, description="Progress %")
    due_date: Optional[date] = Field(None, description="Due date")
    tags: List[str] = Field(default_factory=list, description="Tags")

class Task(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: str = Field("todo", description="todo | in_progress | done")
    priority: str = Field("medium", description="low | medium | high | urgent")
    assignee_id: Optional[str] = Field(None, description="Assignee user id")
    project_id: Optional[str] = Field(None, description="Related project id")
    due_date: Optional[date] = Field(None, description="Due date")
    labels: List[str] = Field(default_factory=list, description="Labels")
