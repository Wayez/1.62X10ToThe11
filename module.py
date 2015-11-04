from pymongo import MongoClient
import re;

#ayy lmao
# hi wayez
# FUNCTIONS TO MONGO

# KATHY
# authenticate
# newUser
# changePassword

# WAYEZ
# makePost
# getPost

# WINTON
# getPoster
# getAllPosts

# JERRY
# addToPost
# removePost

## two collections dbs: logins and posts
## two mongo dbs: logins and posts

#Winton: I think one db is ok?

connection = MongoClient()
database = connection['database']

def sanitize(input):
    return re.sub('"', "  ", input)

def authenticate(username, password):
    username = sanitize(username)
    connection = MongoClient() 
    cursors = database.logins.find({username: password})
    for document in cursors:
        return True;
    return False;
    #returns a boolean that describes whether the user has succesfully logged in.

def newUser(username,password):
    username = sanitize(username)
    ans = database.logins.find({username:True})
    for r in ans:
        return False
    d = {username:password}
    database.logins.insert(d)
    connection = MongoClient()
    db = connection['logins']
    check = db.logins.find({'username':username}).count()
    if check != 0:
        return False
    ans = db.users.insert({'username':username} ,{'password':password})
    return True
    connection.close() 

def changePassword(username, oldPassword, newPassword):
    newPassword = sanitize(newPassword);
    username = sanitize(username);
    if(authenticate(username,oldPassword)):
       conn = sqlite3.connect("myDataBase.db")
       c = conn.cursor()
       c.execute('update logins set password = "%s" where username = "%s";' % (encrypt(username,newPassword), username))
       conn.commit()
       db = connection['logins']
       db.logins.update(
           {'username': username},
           {
               'username': username,
               'password': newPassword
           },
       )
       return True
    return False

def makePost(username, title, contents):
    username = sanitize(username)
    title = sanitize(title)
    contents = sanitize(contents)
    connection = MongoClient()
    
    cursors = database.logins.find({'title': title})
    for document in cursors:
        return False;
    else:
    
        newpost = {'username': username, 'title': title, 'contents': contents}
        database.posts.insert(newpost)

   	#db.data.insert([{'username':username, 'title':title, 'contents':contents, 'lastPoster':username}])
        return True;
    #adds a post to the databes from username with title = title and contents = contents
    #returns a boolean representing if the operation was successful
    #operation will be unsuccessful if a post with the same title already exists

def getPost(title):
    title = sanitize(title)
    ans = database.posts.find({'title': title})
    newlist = list(ans)
    for r in newlist:
        return r.get('contents')
    #returns the content of post with title = title
    #may only be useful for debugging

def getPoster(title):
    title = sanitize(title)
    ans = database.posts.find({'title': title})
    newlist = list(ans)
    for r in newlist:
        return r.get('username')
    #returns the original poster of a story

def getAllPosts():
    ans = database.posts.find()
    return ans
    #returns the cursor that points to all the contents of the posts collection in the database

def addToPost(username,title, content):
    title = sanitize(title)
    content = sanitize(content)
    conn = MongoClient()
    dbase = conn['posts']
    newContent = " "+getPost(title)+content
    ans = dbase.posts.find({'username':username,'title':title})
    for r in ans:
        return False
    dbase.data.update({'lastPoster':username, 'title': title})
    dbase.posts.update({'contents': newContent, 'title': title})
    return True;
    #adds content to content of original post and returns a boolean representing wether or not the operation was successful

def removePost(title):
    title = sanitize(title)
    conn = MongoClient()
    dbase = conn['posts']
    dbase.posts.remove({'title':title})
    return True;

    #removes post with tile=title from database if it exists and username = admin
    #returns false if operation failed
