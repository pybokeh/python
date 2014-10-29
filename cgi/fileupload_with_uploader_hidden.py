import cgi, os
import cgitb; cgitb.enable()

http_referer = os.environ['HTTP_REFERER']
host = os.environ['HTTP_HOST']
www_index = http_referer.find('www')

url_suffix = http_referer[www_index+3:]
file = "c:\\_tomcat\\webapps\\www"+url_suffix.replace("/","\\")
index = file.rfind("\\")
file_location = file[:index+1]

index2 = http_referer.rfind("/")
home = http_referer[:index2+1]

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

# Generator to buffer file chunks
def fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk
      
# A nested FieldStorage instance holds the file
fileitem = form["upfile"]

# Test if the file was uploaded
if fileitem.filename:

   # strip leading path from file name to avoid directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   f = open(file_location + fn, 'wb', 10000)

   # Read the file in chunks
   for chunk in fbuffer(fileitem.file):
      f.write(chunk)
   f.close()
   message = 'The file "' + fn + '" was uploaded successfully.'

else:
   message = 'No file was uploaded'

index_file = open(file_location+"\\index.html",'w')
index_file.write("<html>\n<META http-equiv=\"Refresh\">\n")

for filename in os.listdir(file_location):
    if os.path.isfile(file_location+filename) and filename != "index.html" and filename != "_FileUpload.html":
        index_file.write("<A HREF=\""+filename+"\">"+filename+"</A><br>\n")

index_file.write("</html>\n")
index_file.close()

print """\
Content-Type: text/html\n
<html><body>
<p>%s</p>
<p>The file was uploaded to: %s</p>
""" % (message,home)
print "<p>Click <A HREF=\""+home+"\"> here</A> to access uploaded file(s).</p></body></html>"
