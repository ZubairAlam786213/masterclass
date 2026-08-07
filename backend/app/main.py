from fastapi import FastAPI
app = FastAPI()



@app.get("/")
def root():
    return { "hello" : "Welcome to the masterclass" }



@app.get("/name/{user_name}")
def info(user_name:str):
    return { "hello" : f"Welcome to the masterclass {user_name}" }



from pydantic import BaseModel,EmailStr

class UserData(BaseModel):
    name : str
    email : EmailStr


@app.post("/user")
def user_data(data:UserData):
    return {"result" : f"hello this is post mapping we got the name {data.name}"}




from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI, HTTPException, status
from email.mime.text import MIMEText
import smtplib
import os
class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

# @app.post("/api/contact", status_code=status.HTTP_200_OK)
# def send_portfolio_email(payload: ContactRequest):
#     # Retrieve securely injected variables from Render's dashboard environment
#     smtp_host = os.environ.get("SMTP_HOST")
#     smtp_user = os.environ.get("SMTP_USER")
#     smtp_pass = os.environ.get("SMTP_PASS")

#     target_email = os.environ.get("MY_PERSONAL_EMAIL")
#     print({
#         "SMTP_HOST": os.getenv("SMTP_HOST"),
#         "SMTP_USER": os.getenv("SMTP_USER"),
#         "SMTP_PASS": "***" if os.getenv("SMTP_PASS") else None,
#         "MY_PERSONAL_EMAIL": os.getenv("MY_PERSONAL_EMAIL"),
#         })
#     if not all([smtp_host, smtp_user, smtp_pass, target_email]):
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="SMTP server environment variables are missing on the host platform."
#         )

#     # Format email formatting strings
#     body_content = f"New Portfolio Message!\n\nName: {payload.name}\nEmail: {payload.email}\n\nMessage:\n{payload.message}"
    
#     msg = MIMEText(body_content)
#     msg["Subject"] = f"💼 Portfolio: Message from {payload.name}"
#     msg["From"] = smtp_user
#     msg["To"] = target_email

#     try:
#         # Establish secure SSL pipeline via Port 465 (Safe for Render)
#         with smtplib.SMTP_SSL(smtp_host, 465,timeout=10) as server:
#             server.login(smtp_user, smtp_pass)
#             server.send_message(msg)
#         print("connected fine")
#         return {"success": True, "message": "Your message was transmitted successfully!"}
        
#     except smtplib.SMTPAuthenticationError:
#         raise HTTPException(status_code=401, detail="Authentication failed. Check your SMTP user/password.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to route email: {str(e)}")

import os
import httpx
from fastapi import FastAPI, HTTPException, status

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
target_email = os.environ.get("MY_PERSONAL_EMAIL")

@app.post("/api/contact", status_code=status.HTTP_200_OK)
async def send_portfolio_email(payload: ContactRequest):
    if not RESEND_API_KEY or not target_email:
        raise HTTPException(
            status_code=500,
            detail="Email service environment variables are missing."
        )

    body_content = f"New Portfolio Message!\n\nName: {payload.name}\nEmail: {payload.email}\n\nMessage:\n{payload.message}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
                json={
                    "from": "Portfolio <onboarding@resend.dev>",  # or your verified domain
                    "to": [target_email],
                    "reply_to": payload.email,
                    "subject": f"💼 Portfolio: Message from {payload.name}",
                    "text": body_content,
                },
            )
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"Email provider error: {response.text}")

        return {"success": True, "message": "Your message was transmitted successfully!"}

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Failed to route email: {str(e)}")