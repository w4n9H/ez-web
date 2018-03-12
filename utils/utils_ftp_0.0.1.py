# !/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import ftplib


class FtpUtils(object):
    def __init__(self, host, user, passwd):
        try:
            self.ftp = ftplib.FTP(host)
            self.ftp.login(user, passwd)
        except Exception, e:
            print e

    def ftp_dir(self, d=None):
        self.ftp.dir(d)

    def mk_dir(self, dir_name):
        try:
            self.ftp.mkd(dir_name)
        except Exception, e:
            print "create %s failed: %s" % (dir_name, str(e))
            return False
        return True

    def ftp_upload(self, filepath):
        bufsize = 8192
        file_handler = open(filepath, 'rb')
        file_name = os.path.split(filepath)[-1]
        try:
            self.ftp.storbinary('STOR %s' % file_name, file_handler, bufsize)
            return True
        except ftplib.error_perm as error:
            raise Exception('upload failed : {}'.format(error))
        finally:
            file_handler.close()

    def ftp_download(self, remotefilepath, localfilepath):
        bufsize = 8192
        file_handler = open(localfilepath, 'wb').write()
        try:
            self.ftp.retrbinary("RETR %s" % remotefilepath, file_handler, bufsize)
            return True
        except ftplib.error_perm as error:
            raise Exception('download failed : {}'.format(error))
        finally:
            file_handler.close()

    def ftp_quit(self):
        self.ftp.quit()

