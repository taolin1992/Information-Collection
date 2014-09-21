Used to collect stored books information of e-libraries.

Double-click on the "start.bat" to start collection and restart at any time after a network interruption.

To change the target e-library, please replace the old domain name with the new one ("db.lib.bua.edu.cn" for example) at 2 places:<br/>1.The second line in "start.bat":  python dlut.py * r1.txt r2.txt db.lib.bua.edu.cn<br/>2.The main() function definition in "dlut.py":   domain_name='db.lib.bua.edu.cn'

For more information, please visit Tao Lin's <a href="http://ta0lin.info/?page_id=19">homepage<a />.


