from flask import Flask, request, url_for, redirect
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
sequence=""

level="-2"

@app.route("/")
def hello():
    return "Sequence is\t"+sequence+" and level is"+level

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    senderNumber = request.form.get('From')

    global level
    global sequence
        
    # chat level store so we know which level it is. by default level will be 0 and every time a user exits it will set level value to zero


    resp = MessagingResponse()
    
    if level == "-2":
        helpMe = msg.find("help")
        need = msg.find("need")
        if  msg  ==  "hello" or msg == "hi" or msg =="hy" :        
            resp.message("Hey !! \nHow are you doing ?")
            return str(resp)
        elif "fine" in msg  or "good" in msg or "great" in msg  :
            resp.message("Really Glad to know so. How may i help you ?")
            return str(resp)
        
        elif "no" in msg or "nope" in msg :
            resp.message("Alright !! Let me know if you need any help")
            return str(resp)
        elif "help" in msg or "yes" in msg or "yah" in msg or "need" in msg :
            level="-1"
            # resp.message("Yah sure")
            # return str(resp) ,redirect(url_for('sms_reply'))
            return redirect(url_for('sms_reply'))
        else:
            resp.message("Hey are You alright?, Do You need help ?")   
            return str(resp) 
    
    if level=="-1":
        resp.message("*Quotes*\n0. To Exit\n1. Choose Your Space\n2. Type Your Business Activity\n3. Type Your Timing\n*Dear User Choose Your Option*")
        # resp.message("test")
        level="0"
        sequence=""
        return str(resp)   
    
    if level == "0":
        if msg == "0":
            level="-2"
            resp.message("Bye !! Have A great day. Cheers !!")
            return str(resp)
        if msg == "1":
            sequence +=  "1"
            level="1"
            resp.message("*Please Choose Your Space*\nPress 1 for Executive Office (55,000)\nPress 2 for Manager Office (40,000)\nPress 3 for HR Office (30,000)\nPress 4 for Team Room (18,000) Per Person\nPress 5 for Dedicated Floor\nPress 00 for Going Back\nPress M for Main Screen\nValue of sequence here is\t"+sequence)
            return str(resp)
        elif msg == "2":
            sequence +=  "2"
            resp.message("*Type Your Business Activity*\n\n*This Feature is under development, heading back to previous level.*\n")
            level="-1"
            return str(resp)
        elif msg == "3":
            sequence +=  "3"
            level="1"
            resp.message("*Please Type Your Office Timing*\n1. Clout INN\n2. Clock OUT\n")
            return str(resp)
        else:
            resp.message("Please Enter Appropriate Option\n\n*Quotes*\n1. Choose Your Space\n2. Type Your Business Activity\n3. Type Your Timing\n\n*Dear User Choose Your Option*")
            sequence=""
            level="-1"
            return str(resp)
        
    if level == "1":
        lastPosition=sequence[-1]
        sequence+=lastPosition
        if lastPosition =="1":
            if msg == "1":
                resp.message("You have successfully applied for executive\n\nThank you for your interaction")
                sequence=""
                level="-2"
                return str(resp)  
            elif msg == "2":
                resp.message("You have successfully applied for Manager\n\nThank you for your interaction")
                sequence=""
                level="-2"
                return str(resp)  
            elif msg == "3":
                resp.message("You have successfully applied for HR\n\nThank you for your interaction")
                level="-2"
                sequence=""
                return str(resp)  
            elif msg == "4":
                resp.message("You have successfully applied for Team Room\n\nThank you for your interaction")
                level="-2"
                sequence=""
                return str(resp)  
            elif msg == "5":
                resp.message("You have successfully applied for Dedicated floor\n\nThank you for your interaction")
                level="-2"
                sequence=""
                return str(resp)  
            elif msg == "00":
                # resp.message("Going back to previous Menu\n\n*Please Choose Your Space*\nPress 1 for Executive Office (55,000)\nPress 2 for Manager Office (40,000)\nPress 3 for HR Office (30,000)\nPress 4 for Team Room (18,000) Per Person\nPress 5 for Dedicated Floor\nPress 00 for Back\nType M for Main Screen\n")
                resp.message("Going back to previous Menu\n\nENTER ANY KEY TO GET MENU\n")
                level="-1"
                sequence[-1]
                return str(resp)  
            elif msg == "M" or msg == "m":
                level="-1"
                sequence=""
                return redirect(url_for('sms_reply'))
            else:
                level="1"
                sequence=sequence[:-1]
                resp.message("*Unfortunately It was not suitable option*.\n\n*Please Choose Your Space*\nPress 1 for Executive Office (55,000)\nPress 2 for Manager Office (40,000)\nPress 3 for HR Office (30,000)\nPress 4 for Team Room (18,000) Per Person\nPress 5 for Dedicated Floor\nPress 00 for Back\nType M for Main Screen\nValue of sequence here is\t"+sequence)
                
                return str(resp)
        elif lastPosition== "2":
            resp.message("*We Reached Deadend, Driving You Back to Main Menu !!*")
            level="-1"
            sequence=""
            return str(resp)
        elif lastPosition == "3":
            if msg == "1":
                resp.message("You have Successfully Set Your Clock INN Timing.")
                sequence=""
                level="-1"
                return str(resp)  
            elif msg == "2":
                resp.message("You have Successfully Set Your Clock OUT Timing.")
                sequence=""
                level="-1"
                return str(resp)
            else:
                level="1"
                sequence=sequence[:-1]
                resp.message("*Unfortunately It was not suitable option*.\n\n*Please Type Your Office Timing*\n1. Clout INN\n2. Clock OUT\n")
                return str(resp)

    return str(resp)
            
        





if __name__ == "__main__":
    app.run(debug=True)