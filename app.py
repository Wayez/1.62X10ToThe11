from flask import Flask, render_template, request, session, redirect, url_for, Markup
import sqlite3
import module
import random

app = Flask(__name__)

@app.route("/home",methods=['GET','POST'])
@app.route("/home/",methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        button = request.form['button']
        if button == "Create Account":
            newUser = request.form['newUser']
            newPass = request.form['newPass']
            newPassC = request.form['newPassC']
            #password match check
            if (newPass == newPassC):
                #username and password lengths check
                if len(newUser)<4:
                    return render_template('home.html',error2="Username must be longer than 4 characters")
                if len(newPass)<4:
                    return render_template('home.html',error2="Password must be longer than 4 characters")
                #account created successfully
                if  module.newUser(newUser,newPass):
                    return render_template('home.html',success="Account created!")
                #username taken error
                else:
                    return render_template('home.html',error2="Username taken")            
            else:
                return render_template('home.html',error2="Passwords do not match!")
        #Login
        #if credentials valid, log them in with session
        if button == "Login":
            uname = request.form['username']
            pword = request.form['password']
            if module.authenticate(uname,pword):
                if 'n' not in session:
                    session['n'] = uname
                    return redirect(url_for('home'))
                #else renders login w/ error message
            else:
                return render_template("home.html",error="Invalid Username or Password")

@app.route('/about')
def about():
    return render_template("about.html");


@app.route('/logout', methods=['GET','POST'])
def logoff():
    #remove the username from the session if it's there
    session.pop('n', None)
    return redirect(url_for('home'))



@app.route("/newStory", methods=['GET','POST'])
def nStory():
    if request.method=="GET":
        return render_template("new.html")
    else:
        username=session['n']
        button=request.form['button']
        title=request.form['sTitle']
        line=request.form['entry']
        #valid input check
        error=""
        if len(title) == 0:
            error+="Nothing submitted for title.\n"
        if len(line) == 0:
            error+=" Nothing submitted for content."
        if len(error) > 0:
            return render_template("new.html", error=error)
        #add default period at end of submission
        #line=punctCheck(line)
        if line[-1] != ".":
            if line[-1] !="?":
                if line[-1] !="!":
                    line+="."       
#redirect to newly created story
        if button=="Submit":
            module.makePost(username, title, line)
            return redirect('/story/%s' %title)
        #redirect home
        if button=="Cancel":
            return redirect(url_for('home'))
        else:
            return render_template("new.html")



@app.route("/story/<title>",methods=['GET','POST'])
def story(title=""):
    poster=module.getPoster(title)
    line=module.getPost(title)
    exists = True
    if 'n' in session:
        delete=''
        #show admin option for delete a story
        if session['n'] == "Admin" and module.getPost(title) is not None:
            delete = '<input type="submit" name="button" value="Delete Story">'
            delete = Markup(delete)
        if request.method == "GET":
            if module.getPost(title) is None:
                exists = False
                return render_template("story.html", title="Post does not exist!", exists=exists);
            else:
                return render_template("story.html", title=title, poster=poster,line=line, delete=delete,exists=exists)
        else:
            newLine = request.form['newLine']
            #newLine = punctCheck(newLine)
            button = request.form['button']
            #add to story
            if button == "Add to Story":
                if len(newLine) == 0:
                    error="Nothing submitted for content"
                    return render_template("story.html", title=title, poster=poster,line=line, delete=delete, error=error, exists=exists)
                #puncuation check
                if newLine[-1] != ".":
                    if newLine[-1] !="?":
                        if newLine[-1] !="!":
                            newLine+="."                        
                if(module.addToPost(session['n'],title," " + newLine)):
                    line = module.getPost(title)
                    return render_template("story.html", title=title, poster=poster,line=line, delete=delete,exists=exists) 
                #consecutive contribution error
                else:
                    return render_template("story.html",title=title,poster=poster, line=line,delete=delete,error="You cannot write two sentences in a row!",exists=exists)
            #deletes story
            else:
                module.removePost(title)
                return redirect(url_for('stories'))
    else:
        return render_template("story.html")

@app.route("/stories")
def stories():
    #generates html for displaying the title as a link
    str=""
    stories=module.getAllPosts()
    for item in stories:
        str+="<h1> <a href='story/%s'> %s</a> </h1>" %(item[1], item[1])
        #str+="<h2> Posted by: %s </h2>" %item[0]
        str+="<h3> %s </h3>" %item[2] + "<hr>"

    str= Markup(str)

    return render_template("stories.html", link=str) 

@app.route("/random")
def randomStory():
    everything=module.getAllPosts()
    number=random.randint(0,len(everything)-1)
    title=everything[number][1]
    str='<meta http-equiv="refresh" content="0; /story/%s" />' % title
    lin=Markup(str)
    return render_template("forward.html", link=lin)

@app.route("/pword", methods=['GET','POST'])
def passChange():
    if request.method=="GET":
        return render_template("passChange.html")
    else:
        button=request.form['button']
        if button=="Change Password":
            username=session['n']
            oldpass=request.form['oldPass']
            newpass=request.form['newPass']
            newpassc=request.form['newPassC']
            if len(newpass)<4:
                return render_template("passChange.html",error = "New password too short. Must be at least 4 characters")
            if newpass != newpassc:
                return render_template("passChange.html",error = "New passwords do not match")
            if module.changePassword(username,oldpass,newpass):
                return render_template("passChange.html", success="Password changed")
            else:
                return render_template("passChange.html", error="Wrong Current Password")            
        else:
            return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True
    app.secret_key="c720minusboying"
    app.run(host='0.0.0.0', port=5000)







