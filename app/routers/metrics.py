from fastapi import APIRouter,Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.data_handler import save_user_data, get_user_data, analyze_user_data

router = APIRouter()

@router.post("/submit_data")
async def submit_data(request: Request, db: Session = Depends(get_db)):
    try:
         data = await request.json()
         user_id = data['user_id']
         user_metrics = data['metrics']
         save_user_data(user_id, user_metrics, db)
         return JSONResponse(content={"message": "Data received successfully!"}, status_code=201)
    except Exception as e:
         raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get_feedback/{user_id}")
async def get_feedback(user_id: str, db: Session = Depends(get_db)):
     try:
         user_metrics_df = get_user_data(user_id, db)
         if user_metrics_df is None:
             raise HTTPException(status_code=404, detail="No data found for this user.")
         feedback = analyze_user_data(user_metrics_df)
         return JSONResponse(content=feedback, status_code=200)
     except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))