from bottle import route, static_file, redirect, request, response, template
from urlparse import urlparse
import os, base64, AssocLookUp, pyodbc, crypto, codecs


###########################################  Static Routings for www webapp  ###########################################
@route('/www/<filename>')
def server_static(filename):
    return static_file(filename, root=r'D:\webapps\www')

@route('/www/source/<filename>')
def static_source(filename):
    response.set_header('Content-Type','text/plain')
    return static_file(filename, root=r'D:\webapps\www\source')

@route('/www/images/<filepath:path>')
def static_images(filepath):
    return static_file(filepath, root=r'D:\webapps\www\images')

@route('/www/vids/<filepath:path>')
def static_vids(filepath):
    return static_file(filepath, root=r'D:\webapps\www\vids')

@route('/www/audio/<filepath:path>')
def static_audio(filepath):
    return static_file(filepath, root=r'D:\webapps\www\audio')

@route('/www/files/<filepath:path>')
def static_files(filepath):
    return static_file(filepath, root=r'D:\webapps\www\files')

@route('/www/shared/<filepath:path>')
def static_shared(filepath):
    return static_file(filepath, root=r'D:\webapps\www\shared')


###############################################  Routes for Viewable Directories  ###############################################
@route('/www/images/index')
def showImages():
    return showListings()

@route('/www/vids/index')
def showVids():
    return showListings()

@route('/www/files/index')
def showFiles():
    return showListings()

@route('/www/audio/index')
def showAudio():
    return showListings()

@route('/www/shared/index')
def showShared():
    return showListings()

#############################################  Dynamic Routings for www webapp  ##########################################

@route('/www/AssocInfo', method='POST')
def AssocInfo():
    # Get encrypted password and decrypt it
    pw_encrypted = open(r'D:\webapps\_server\pyodbc\pw', 'r').read()
    key = codecs.escape_decode(open(r'D:\webapps\_server\pyodbc\key', 'r').read())[0]
    pw = crypto.decrypt_with_key(key, pw_encrypted)
    userid = 'ma17151'
    
    querystr = request.POST.get('qryParameter', '').strip()
    cnxn_string = 'DSN=DSNOGW01;UID=' + userid + ';PWD=' + pw

    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    # Get the resultset
    resultset = AssocLookUp.getResultset(querystr, cursor)

    # Get column name of the resultset
    column_name_list = [tuple[0] for tuple in cursor.description]
    
    cursor.close()
    cnxn.close()

    output = template(r'D:\webapps\_templates\make_table.tpl', rows=resultset, column_names=column_name_list)
    return output

@route('/www/AssocInfoAdHoc', method='POST')
def AssocInfoAdHoc():
    # Get encrypted password and decrypt it
    pw_encrypted = open(r'D:\webapps\_server\pyodbc\pw', 'r').read()
    key = codecs.escape_decode(open(r'D:\webapps\_server\pyodbc\key', 'r').read())[0]
    pw = crypto.decrypt_with_key(key, pw_encrypted)
    userid = 'ma17151'
    
    querystr = request.POST.get('sqlString', '').strip()
    cnxn_string = 'DSN=DSNOGW01;UID=' + userid + ';PWD=' + pw

    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    cursor.execute(querystr)
    cnxn.commit()
    resultset = cursor.fetchall()

    # Get column name of the resultset
    column_name_list = [tuple[0] for tuple in cursor.description]
    
    cursor.close()
    cnxn.close()

    # Send the response/result as Excel output
    response.content_type = 'application/vnd.ms-excel'
    output = template(r'D:\webapps\_templates\make_table.tpl', rows=resultset, column_names=column_name_list)
    return output

@route('/www/CMQ_Adhoc', method='POST')
def CMQ_Adhoc():
    # Get password and "de-fuzzy" it
    pw_file = open(r'D:\webapps\_server\pyodbc\pw.txt', 'r')
    pw = base64.b64decode(pw_file.read())
    userid = 'rb10'
    pw_file.close()
    
    querystr = request.POST.get('sqlString', '').strip()
    cnxn_string = 'DSN=CMQ_PROD;UID=' + userid + ';PWD=' + pw

    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    cursor.execute(querystr)
    cnxn.commit()
    resultset = cursor.fetchall()

    # Get column name of the resultset
    column_name_list = [tuple[0] for tuple in cursor.description]
    
    cursor.close()
    cnxn.close()

    # Send the response/result as Excel output
    response.content_type = 'application/vnd.ms-excel'
    output = template(r'D:\webapps\_templates\make_table.tpl', rows=resultset, column_names=column_name_list)
    return output

@route('/www/upload', method='POST')
def upload():
    # Get the URL that the FileUpload.html is located at (ex: http://localhost/denso/images/FileUpload.html)
    requestURL = request.environ.get('HTTP_REFERER')
    url_parser = urlparse(requestURL)

    # Get just the URL suffix (ex: /www/images/FileUpload.html)
    url_suffix = url_parser.path
    
    # Now map the URL suffix to the server webapp directory
    request_path = "d:\\webapps"+url_suffix.replace("/","\\")  # Since server is on Windoze, need to convert to backslash

    # But we don't need the "FileUpload.html" in the path, so exclude it from the path by finding the right-most backslash
    index = request_path.rfind("\\")
    root_path = request_path[:index+1]

    # Get the file item from the FileUpload.html form
    fileitem = request.POST.get('upfile', '')

    # upload the file to the server at the designated path
    return upload(fileitem, root_path)

@route('/www/showpwd', method='POST')
def showPWD():
    pwd = request.POST.get('fuzzypwd', '').strip()  # Get encrypted password from the HTML form
    key = codecs.escape_decode(open(r'D:\webapps\_server\pyodbc\key', 'r').read())[0] # Get the encryption key
    mypwd = crypto.decrypt_with_key(key, pwd)
    return "Your password is: ", mypwd

@route('/www/encodepwd', method='POST')
def encodePWD():
    pwd = request.POST.get('password', '').strip()
    key = codecs.escape_decode(open(r'D:\webapps\_server\pyodbc\key', 'r').read())[0] # Get the encryption key
    mypwd = crypto.encrypt_with_key(key, pwd)
    return "Your encrypted password is: ", mypwd
    
###############################  Helper Functions  ############################
# Generator to buffer file chunks during file upload
def fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk

# Main file upload function
def upload(filenm, path):

    try: # Windows needs stdio set for binary mode.
        import msvcrt
        msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
        msvcrt.setmode (1, os.O_BINARY) # stdout = 1
    except ImportError:
        pass

    fileitem = filenm
    root_path = path

    # Test if the file was uploaded
    if fileitem.filename:

        # strip leading path from file name to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        f = open(root_path + fn, 'wb', 10000)

        # Read the file in chunks
        for chunk in fbuffer(fileitem.file):
            f.write(chunk)
        f.close()
        return 'The file "' + fn + '" was uploaded successfully'

    else:
        return 'No file was uploaded'

def showListings():
    """This function allows a directory's contents to be listed"""

    url_suffix = request.urlparts[2] # /www/images/index

    # But exclude "index" from the url suffix
    index = url_suffix.rfind("/")
    url_path = url_suffix[:index+1] # now we have only /www/images/

    server_path = "d:\\webapps"+url_path.replace("/","\\")  # replace forward slash with back slash since we're on Windoze
                                                            # now we have d:\webapps\www\images\
    filelist = []
    for filename in os.listdir(server_path):
        if os.path.isfile(server_path+filename):  # if the path is a file type, then append to the file list
            filelist.append(filename)

    output = template(r'D:\webapps\_templates\create_index.tpl', files=filelist)

    return output

def showListingsWithOutFileUpload():
    """This function allows a directory's contents to be listed except for FileUpload.html file"""

    url_suffix = request.urlparts[2] # /www/images/index

    # But exclude "index" from the url suffix
    index = url_suffix.rfind("/")
    url_path = url_suffix[:index+1] # now we have only /www/images/

    server_path = "d:\\webapps"+url_path.replace("/","\\")  # replace forward slash with back slash since we're on Windoze
                                                            # now we have d:\webapps\www\images\
    filelist = []
    for filename in os.listdir(server_path):
        if os.path.isfile(server_path+filename):  # if the path is a file type, then append to the file list
            if filename != '_FileUpload.html':
                filelist.append(filename)

    output = template(r'D:\webapps\_templates\create_index.tpl', files=filelist)

    return output
