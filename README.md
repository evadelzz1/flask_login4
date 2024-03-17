# flask-mysql-auth-system

Flask MySQL Authentication Tutorial: Login, Register, Logout, and Dashboard

### Install

      git clone https://github.com/evadelzz1/flask_login4.git

      cd ./flask_login4/

      python -m venv .venv
      
      source .venv/bin/activate

      pip install -r requirements.txt

      mysql -u root -p

            mysql> source ./db.sql
      
      python app.py

      python app_orig.py


### Reference
      v1.py : original
      v2.py : try ~ except ~
      v3.py : with
      v4.py : save object in session store
      v5.py : split file (config, class, db)

- [Flask MySQL Authentication Tutorial: Login, Register, Logout, and Dashboard](https://www.youtube.com/watch?v=aV8YSefG1fw)
- [github](https://github.com/kritimyantra/flask-mysql-auth-system)
- [Flask-WTF](https://velog.io/@2jinu/Flask-Flask-WTF)
- [Flask-Doc](https://flask-docs-kr.readthedocs.io)
- [wtforms Definition](https://wtforms.readthedocs.io/en/3.1.x/)


### mysql Install

      brew services list

      brew install mysql

      mysql.server start

      mysql_secure_installation

      mysql -u root -p

      create user scott@'%' identified by 'tiger';

      grant all privileges on *.* to scott@'%';

      flush privileges;

      mysql.server stop

      # remove mysql

            brew services stop mysql
            brew uninstall mysql
            rm -rf /opt/homebrew/var/mysql

            sudo rm -rf /usr/local/var/mysql
            sudo rm -rf /usr/local/bin/mysql*
            sudo rm -rf /usr/local/Cellar/mysql


[TroubleShoot] no such file libmysqlclient.2x.dylib

- https://jakpentest.tistory.com/entry/TroubleShoot-libmysqlclient22dylib-no-such-file

      ImportError: dlopen(/Users/way2bit/Desktop/lippsalabs/python/flask_login4/.venv/lib/python3.11/site-packages/MySQLdb/_mysql.cpython-311-darwin.so, 0x0002): Library not loaded: /usr/local/opt/mysql/lib/libmysqlclient.22.dylib

      pip uninstall mysqlclient
      pip install --no-cache mysqlclient
