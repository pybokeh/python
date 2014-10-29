from letsqlite import LET

let = LET(r'D:\webapps\tpms\server\db\tpms')
let.getConnection()
let.processLetFiles()
let.close()
