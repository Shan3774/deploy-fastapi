from fastapi import FastAPI, HTTPException , Depends
from pydantic import BaseModel, Field
from typing import List, Annotated, Optional
from database import sessionLocal, engine
import models
from sqlalchemy.orm import Session

#create the app
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


#define question and choice classes
class ChoiceBase(BaseModel):
    choice_text:str = Field(..., description="choice content" )
    is_correct:bool = Field( default = False, description="Wether this choice is correct or not" )

class QuestionBase(BaseModel):
    question_text:str
    choices:List[ChoiceBase]


#open the database
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


#read root route
@app.get("/")
def read_root():
    return("hello worlds")


#get all quetions rout
@app.get("/questions")
def read_questions(db:db_dependency):
    result = db.query(models.Questions).all()
    if not result:
        raise HTTPException(status_code="404", detail="No Questions found")
    return result


#get single question by id route
@app.get("/questions/{question_id}")
def read_question(question_id:int, db:db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result


#get choices for a question route
@app.get("/choices/{question_id}")
def read_choices_per_question(question_id:int, db:db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="No choices found for this question id")
    return result


#create question route 
@app.post("/questions")
def create_question(question:QuestionBase, db:db_dependency):
    db_question = models.Questions(question_text = question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text = choice.choice_text, is_correct= choice.is_correct , question_id = db_question.id)
        db.add(db_choice)
        db.commit()
        



